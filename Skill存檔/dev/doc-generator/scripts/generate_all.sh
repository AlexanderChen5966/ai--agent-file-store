#!/bin/bash
set -euo pipefail

# =========================
# Washcar build pipeline
# - Creates/uses .venv
# - Installs Python deps with the SAME interpreter
# - Installs Graphviz + PlantUML
# - Fixes WeasyPrint native deps on macOS (glib/pango/cairo...)
# =========================

fail_count=0

run_step() {
  local title="$1"; shift
  echo "----------------------------------------"
  echo "$title"
  if "$@"; then
    echo "✅ $title"
  else
    local code=$?
    echo "❌ $title (exit=$code)"
    fail_count=$((fail_count+1))
  fi
}

ensure_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "❌ Missing command: $cmd"
    return 1
  fi
  return 0
}

echo "========================================"
echo "Environment check"
echo "OSTYPE: ${OSTYPE:-unknown}"
echo "========================================"

# --- Go to script dir ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Working directory: $SCRIPT_DIR"
cd "$SCRIPT_DIR"

# --- 1) Python / venv ---
if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ Error: python3 not found"
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Creating venv: .venv"
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source ".venv/bin/activate"

PYTHON="$(command -v python)"
PIP="$PYTHON -m pip"

echo "Using python: $PYTHON"
"$PYTHON" -V
$PIP install -U pip setuptools wheel >/dev/null

install_python_pkg() {
  local import_name="$1"
  local pip_name="$2"
  if ! "$PYTHON" -c "import ${import_name}" >/dev/null 2>&1; then
    echo "Installing python pkg: ${pip_name} (import ${import_name})"
    $PIP install -U "${pip_name}"
  else
    echo "Python pkg OK: ${pip_name}"
  fi
}

# --- 2) Native dependencies ---
if [[ "${OSTYPE}" == darwin* ]]; then
  # macOS: WeasyPrint needs glib/pango/cairo etc.
  if ! command -v brew >/dev/null 2>&1; then
    echo "❌ Homebrew not found. Please install Homebrew first."
    exit 1
  fi

  echo "Installing native deps via brew (graphviz + plantuml + weasyprint deps)..."
  brew update
  brew install graphviz plantuml glib pango cairo gdk-pixbuf libffi

  BREW_PREFIX="$(brew --prefix)"
  export DYLD_FALLBACK_LIBRARY_PATH="$BREW_PREFIX/lib:/usr/lib"
  echo "DYLD_FALLBACK_LIBRARY_PATH=$DYLD_FALLBACK_LIBRARY_PATH"

elif [[ "${OSTYPE}" == linux-gnu* ]]; then
  if command -v apt-get >/dev/null 2>&1; then
    echo "Installing native deps via apt-get (graphviz + plantuml + java)..."
    sudo apt-get update
    sudo apt-get install -y graphviz plantuml default-jre
  else
    echo "❌ apt-get not found. Please install graphviz/plantuml manually."
    exit 1
  fi
else
  echo "❌ Unsupported OS: ${OSTYPE}"
  exit 1
fi

# --- 3) Python dependencies ---
# API PDF
install_python_pkg "markdown" "markdown"
install_python_pkg "jinja2" "jinja2"
install_python_pkg "weasyprint" "weasyprint"

# ERD / image resize helpers
install_python_pkg "graphviz" "graphviz"
install_python_pkg "PIL" "pillow"

# --- 4) Sanity checks ---
ensure_cmd dot || { echo "❌ Graphviz dot missing"; exit 1; }
ensure_cmd plantuml || { echo "❌ plantuml missing"; exit 1; }

echo "WeasyPrint import test..."
"$PYTHON" -c "from weasyprint import HTML; print('weasy ok')" >/dev/null

# --- 5) Execution ---
run_step "1. Generating Postman Collection..." "$PYTHON" api_to_postman.py
run_step "2. Generating API PDF..." "$PYTHON" convert_api_pdf.py
run_step "3. Generating DB Schema PNG..." "$PYTHON" dbml_to_png.py
run_step "4. Generating api flow chart PNG..." "$PYTHON" convert_api_to_uml_flow.py

echo "----------------------------------------"
if [ "$fail_count" -eq 0 ]; then
  echo "✅ All tasks completed successfully."
else
  echo "⚠️ Completed with ${fail_count} failure(s). Check logs above."
  exit 1
fi
