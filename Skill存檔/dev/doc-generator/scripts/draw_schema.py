#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

from graphviz import Digraph

MD_FILE = Path("ORDER_TRADE_INVOICE_DB_SCHEME.md")
OUT_PNG = Path("delivery_doc/washcar_database_schema2.png")
OUT_PNG.parent.mkdir(parents=True, exist_ok=True)

RANKDIR = "TB"
SPLINES = "curved"   # if dot errors, use "spline"
ENGINE = "dot"
FONT_TABLE = "Menlo"
FONT_UI = "Helvetica"

FORCE_SIZE = False
TARGET_W, TARGET_H = 1076, 1342
RESIZE_MODE = "contain"
ALLOW_UPSCALE = True

CREATE_TABLE_RE = re.compile(
    r"CREATE\s+TABLE\s+`(?P<name>[^`]+)`\s*\((?P<body>.*?)\)\s*ENGINE=",
    re.IGNORECASE | re.DOTALL,
    )
COL_LINE_RE = re.compile(r"^\s*`(?P<col>[^`]+)`\s+(?P<rest>.+)$")
PK_RE = re.compile(r"^\s*PRIMARY\s+KEY\s*\((?P<cols>.+?)\)\s*,?\s*$", re.IGNORECASE)
UK_RE = re.compile(r"^\s*UNIQUE\s+KEY\s+`[^`]+`\s*\((?P<cols>.+?)\)\s*,?\s*$", re.IGNORECASE)
BACKTICK_COL_RE = re.compile(r"`([^`]+)`")


@dataclass
class Column:
    name: str
    col_type: str
    not_null: bool = False
    auto_inc: bool = False


@dataclass
class Table:
    name: str
    columns: Dict[str, Column] = field(default_factory=dict)
    pk: List[str] = field(default_factory=list)
    uniques: List[List[str]] = field(default_factory=list)

    def col_count(self) -> int:
        return len(self.columns)

    def has_cols(self, cols: Tuple[str, ...]) -> bool:
        return all(c in self.columns for c in cols)

    def unique_single_cols(self) -> Set[str]:
        out = set(self.pk)
        for u in self.uniques:
            if len(u) == 1:
                out.add(u[0])
        return out

    def unique_sets(self) -> List[Tuple[str, ...]]:
        sets: List[Tuple[str, ...]] = []
        if self.pk:
            sets.append(tuple(self.pk))
        for u in self.uniques:
            sets.append(tuple(u))
        return sets


@dataclass(frozen=True)
class Relation:
    parent_table: str
    parent_cols: Tuple[str, ...]
    child_table: str
    child_cols: Tuple[str, ...]
    kind: str  # "FK" | "NK" | "COMPOSITE"


def parse_one_table(name: str, body: str) -> Table:
    t = Table(name=name)

    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            continue

        m_pk = PK_RE.match(raw)
        if m_pk:
            t.pk = BACKTICK_COL_RE.findall(m_pk.group("cols"))
            continue

        m_uk = UK_RE.match(raw)
        if m_uk:
            cols = BACKTICK_COL_RE.findall(m_uk.group("cols"))
            if cols:
                t.uniques.append(cols)
            continue

        m_col = COL_LINE_RE.match(raw)
        if m_col:
            col = m_col.group("col")
            rest = m_col.group("rest").rstrip(",")
            parts = rest.split()
            if not parts:
                continue
            col_type = parts[0]
            up = rest.upper()

            t.columns[col] = Column(
                name=col,
                col_type=col_type,
                not_null=("NOT NULL" in up),
                auto_inc=("AUTO_INCREMENT" in up),
            )

    return t


def parse_schema_from_markdown(md_text: str) -> Dict[str, Table]:
    tables: Dict[str, Table] = {}
    for m in CREATE_TABLE_RE.finditer(md_text):
        name = m.group("name")
        body = m.group("body")
        tables[name] = parse_one_table(name, body)
    return tables


def infer_relations(tables: Dict[str, Table]) -> Set[Relation]:
    rels: Set[Relation] = set()

    unique_col_index: Dict[str, List[str]] = {}
    for tn, t in tables.items():
        for c in t.unique_single_cols():
            unique_col_index.setdefault(c, []).append(tn)

    def best_parent(candidates: List[str]) -> Optional[str]:
        if not candidates:
            return None
        return sorted(candidates, key=lambda x: tables[x].col_count(), reverse=True)[0]

    # xxx_id -> xxx.id
    for child_tn, child in tables.items():
        for c in child.columns.keys():
            if c.endswith("_id") and len(c) > 3:
                base = c[:-3]
                if base in tables and "id" in tables[base].columns:
                    rels.add(Relation(base, ("id",), child_tn, (c,), "FK"))

    # same-name unique business key
    for child_tn, child in tables.items():
        for c in child.columns.keys():
            candidates = [t for t in unique_col_index.get(c, []) if t != child_tn]
            if candidates:
                parent = best_parent(candidates)
                if parent:
                    rels.add(Relation(parent, (c,), child_tn, (c,), "FK"))

    # *_code natural keys
    for child_tn, child in tables.items():
        for c in child.columns.keys():
            if c.endswith("_code"):
                base = c[:-5]
                if base in tables and c in tables[base].columns:
                    rels.add(Relation(base, (c,), child_tn, (c,), "NK"))

    # composite inference
    for parent_tn, parent in tables.items():
        for u in parent.unique_sets():
            if len(u) < 2:
                continue
            for child_tn, child in tables.items():
                if child_tn == parent_tn:
                    continue
                if child.has_cols(u):
                    if child.col_count() <= len(u):
                        continue
                    rels.add(Relation(parent_tn, u, child_tn, u, "COMPOSITE"))

    priority = {"FK": 3, "COMPOSITE": 2, "NK": 1}
    best: Dict[Tuple, Relation] = {}
    for r in rels:
        k = (r.parent_table, r.parent_cols, r.child_table, r.child_cols)
        if k not in best or priority[r.kind] > priority[best[k].kind]:
            best[k] = r
    return set(best.values())


EDGE_COLORS = [
    "#0072B2", "#D55E00", "#009E73", "#CC79A7",
    "#E69F00", "#56B4E9", "#F0E442", "#999999",
]


def safe_node_id(name: str) -> str:
    nid = re.sub(r"\W+", "_", name)
    if not nid:
        nid = "t"
    if nid[0].isdigit():
        nid = "t_" + nid
    return nid


def safe_port_id(name: str) -> str:
    pid = re.sub(r"\W+", "_", name)
    if not pid:
        pid = "c"
    if pid[0].isdigit():
        pid = "c_" + pid
    return pid


def build_layout_hints(dot: Digraph, node_ids: Dict[str, str], rels: Set[Relation]) -> None:
    in_deg: Dict[str, int] = {t: 0 for t in node_ids}
    out_deg: Dict[str, int] = {t: 0 for t in node_ids}

    for r in rels:
        out_deg[r.parent_table] = out_deg.get(r.parent_table, 0) + 1
        in_deg[r.child_table] = in_deg.get(r.child_table, 0) + 1

    deg = {t: in_deg.get(t, 0) + out_deg.get(t, 0) for t in node_ids}
    hub = max(deg.keys(), key=lambda t: deg[t]) if deg else None

    roots = sorted([t for t in node_ids if in_deg.get(t, 0) == 0 and out_deg.get(t, 0) > 0])
    leaves = sorted([t for t in node_ids if out_deg.get(t, 0) == 0 and in_deg.get(t, 0) > 0])
    mids = sorted([t for t in node_ids if t not in roots and t not in leaves and t != hub])

    if roots:
        with dot.subgraph(name="rank_roots") as s:
            s.attr(rank="same")
            for t in roots:
                s.node(node_ids[t])
        for a, b in zip(roots, roots[1:]):
            dot.edge(node_ids[a], node_ids[b], style="invis", weight="20")

    if hub:
        with dot.subgraph(name="rank_hub") as s:
            s.attr(rank="same")
            s.node(node_ids[hub])

    if mids:
        with dot.subgraph(name="rank_mids") as s:
            s.attr(rank="same")
            for t in mids[:4]:
                s.node(node_ids[t])
        for a, b in zip(mids[:4], mids[1:4]):
            dot.edge(node_ids[a], node_ids[b], style="invis", weight="10")

    if leaves:
        with dot.subgraph(name="rank_leaves") as s:
            s.attr(rank="same")
            for t in leaves:
                s.node(node_ids[t])
        for a, b in zip(leaves, leaves[1:]):
            dot.edge(node_ids[a], node_ids[b], style="invis", weight="20")

    if hub:
        if roots:
            dot.edge(node_ids[roots[0]], node_ids[hub], style="invis", weight="30")
        if leaves:
            dot.edge(node_ids[hub], node_ids[leaves[0]], style="invis", weight="30")


def build_erd_graph(tables: Dict[str, Table], rels: Set[Relation], out_png: Path) -> Path:
    dot = Digraph("ERD", engine=ENGINE, format="png")
    dot.attr(
        rankdir=RANKDIR,
        splines=SPLINES,
        overlap="false",
        concentrate="false",
        nodesep="0.8",
        ranksep="1.0",
        pad="0.35",
        bgcolor="white",
    )
    dot.attr("node", shape="plaintext", fontname=FONT_UI)

    node_id: Dict[str, str] = {tn: safe_node_id(tn) for tn in tables.keys()}

    fk_cols: Set[Tuple[str, str]] = set()
    for r in rels:
        for cc in r.child_cols:
            fk_cols.add((r.child_table, cc))

    col_port: Dict[Tuple[str, str], str] = {}

    for tname, t in tables.items():
        nid = node_id[tname]
        pk_set = set(t.pk)

        ordered: List[str] = []
        for pk in t.pk:
            if pk in t.columns:
                ordered.append(pk)
        for c in t.columns.keys():
            if c not in ordered:
                ordered.append(c)

        rows: List[str] = []
        rows.append(
            f'<TR><TD BGCOLOR="#24537d" ALIGN="CENTER">'
            f'<FONT COLOR="white"><B>{tname}</B></FONT></TD></TR>'
        )

        for c in ordered:
            col = t.columns[c]
            pid = safe_port_id(c)
            col_port[(tname, c)] = pid

            is_pk = c in pk_set
            is_fk = (tname, c) in fk_cols

            if is_pk and is_fk:
                bg = "#E7F5FF"
                prefix = "★↳ "
            elif is_pk:
                bg = "#EEF6FF"
                prefix = "★ "
            elif is_fk:
                bg = "#FFF4E5"
                prefix = "↳FK "
            else:
                bg = "white"
                prefix = ""

            rows.append(
                f'<TR><TD PORT="{pid}" ALIGN="LEFT" BGCOLOR="{bg}">'
                f'<FONT FACE="{FONT_TABLE}" POINT-SIZE="10">'
                f'{prefix}{c} : {col.col_type}'
                f"</FONT></TD></TR>"
            )

        html = (
            '<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">'
            + "".join(rows)
            + "</TABLE>>"
        )
        dot.node(nid, label=html)

    build_layout_hints(dot, node_id, rels)

    tail_side, head_side = "e", "w"  # hit columns precisely from right->left
    rel_list = sorted(list(rels), key=lambda r: (r.kind, r.parent_table, r.child_table, r.parent_cols, r.child_cols))

    for i, r in enumerate(rel_list):
        color = EDGE_COLORS[i % len(EDGE_COLORS)]
        if r.kind == "FK":
            style, penwidth = "solid", "1.4"
        elif r.kind == "COMPOSITE":
            style, penwidth = "solid", "1.2"
        else:
            style, penwidth = "dashed", "1.1"

        p0, c0 = r.parent_cols[0], r.child_cols[0]
        p_pid = col_port.get((r.parent_table, p0))
        c_pid = col_port.get((r.child_table, c0))
        if not p_pid or not c_pid:
            continue

        tail = f"{node_id[r.parent_table]}:{p_pid}:{tail_side}"
        head = f"{node_id[r.child_table]}:{c_pid}:{head_side}"

        label = ",".join(r.child_cols) if len(r.child_cols) > 1 else ""
        minlen = "2" if (r.kind != "NK" or len(r.child_cols) > 1) else "1"

        dot.edge(
            tail,
            head,
            arrowhead="vee",
            arrowsize="0.8",
            color=color,
            penwidth=penwidth,
            style=style,
            constraint="true",
            minlen=minlen,
            label=label,
            fontsize="9",
        )

    stem = str(out_png.with_suffix(""))
    dot.render(stem, cleanup=True)
    return out_png


def to_fixed_png(src_png: Path, dst_png: Path, w: int, h: int, mode: str, allow_upscale: bool):
    from PIL import Image
    img = Image.open(src_png).convert("RGBA")
    iw, ih = img.size

    if mode == "contain":
        scale = min(w / iw, h / ih)
        if not allow_upscale:
            scale = min(scale, 1.0)
        nw, nh = max(1, int(round(iw * scale))), max(1, int(round(ih * scale)))
        img2 = img.resize((nw, nh), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (w, h), (255, 255, 255, 255))
        canvas.paste(img2, ((w - nw) // 2, (h - nh) // 2), img2)
    elif mode == "cover":
        scale = max(w / iw, h / ih)
        nw, nh = max(1, int(round(iw * scale))), max(1, int(round(ih * scale)))
        img2 = img.resize((nw, nh), Image.Resampling.LANCZOS)
        left, top = (nw - w) // 2, (nh - h) // 2
        canvas = img2.crop((left, top, left + w, top + h))
    else:
        raise ValueError("mode must be 'contain' or 'cover'")

    canvas.convert("RGB").save(dst_png, "PNG")


def main():
    if not MD_FILE.exists():
        print(f"❌ Not found: {MD_FILE.resolve()}")
        return

    md_text = MD_FILE.read_text(encoding="utf-8", errors="replace")
    tables = parse_schema_from_markdown(md_text)
    if not tables:
        print("❌ No CREATE TABLE blocks found. Need: CREATE TABLE `xxx` (...) ENGINE=...")
        return

    rels = infer_relations(tables)
    build_erd_graph(tables, rels, OUT_PNG)

    raw_keep = OUT_PNG.with_name(OUT_PNG.stem + "_raw.png")
    shutil.copy2(OUT_PNG, raw_keep)

    if FORCE_SIZE:
        to_fixed_png(raw_keep, OUT_PNG, TARGET_W, TARGET_H, RESIZE_MODE, ALLOW_UPSCALE)

    print(f"✅ ERD PNG: {OUT_PNG.resolve()}")
    print(f"🗂️ Raw PNG: {raw_keep.resolve()}")
    print(f"Tables: {len(tables)} | Relations: {len(rels)}")
    if SPLINES == "curved":
        print("ℹ️ If dot errors on 'curved', set SPLINES='spline'.")


if __name__ == "__main__":
    main()
