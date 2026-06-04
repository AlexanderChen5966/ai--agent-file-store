# Figma UI 元素 → Flutter 元件對應表

## 版面結構

| Figma 元素 | Flutter 對應 | 說明 |
|-----------|-------------|------|
| Frame（垂直排列） | `Column` | `crossAxisAlignment: CrossAxisAlignment.start` |
| Frame（水平排列） | `Row` | `mainAxisAlignment` 依設計調整 |
| Frame（重疊） | `Stack` | 絕對定位用 `Positioned` |
| Auto Layout（填滿） | `Expanded` / `Flexible` | |
| Auto Layout（間距） | `SpacerWidget` | 12 或 16 |
| Grid | `GridView.builder` 或 `Wrap` | |
| Scroll（垂直） | `SingleChildScrollView` | `physics: ClampingScrollPhysics()` |
| Scroll（水平） | `SingleChildScrollView(scrollDirection: Axis.horizontal)` | |

---

## 容器 / 卡片

| Figma 元素 | Flutter 對應 | 範例 |
|-----------|-------------|------|
| 白色圓角卡片 | `CustomCard` | `import 'package:b2b_manager/page/common/widgets/custom_card.dart'` |
| 灰底容器 | `Container(color: SLColor.primaryBackground)` | |
| 邊框容器 | `Container(decoration: BoxDecoration(border: Border.all(color: SLColor.border), borderRadius: ...))` | |
| 陰影卡片 | `CustomCard` | 已內建陰影 |
| 分隔線 | `Divider(color: SLColor.border, height: 1)` | |

---

## 文字

| Figma 文字樣式 | Flutter 對應 |
|--------------|-------------|
| 大標題（20px+, Bold） | `SLText.title(text: '')` |
| 副標題（18px） | `SLText.medium(text: '')` |
| 內文（15px） | `SLText.body(text: '')` |
| 小字（12-14px） | `SLText(text: '', fontSize: 14)` |
| 灰色說明文字 | `SLText(text: '', color: SLColor.textGray)` |

---

## 按鈕

| Figma 按鈕樣式 | Flutter 元件 | import |
|--------------|-------------|--------|
| 藍底白字（主要操作） | `PositiveButton` | `custom_button.dart` |
| 白底藍框（次要操作） | `NegativeButton` | `custom_button.dart` |
| 紅色/橘色（刪除） | `PositiveButton(backgroundColor: SLColor.deleteButton)` | |
| 純 Icon 按鈕 | `BuildIconBtn` | `custom_button.dart` |
| 文字連結按鈕 | `BuildTextBtn` | `custom_button.dart` |
| 黃底按鈕 | `PositiveButton(backgroundColor: SLColor.secondaryButton, textColor: SLColor.text)` | |

---

## 輸入欄位

| Figma 元素 | Flutter 對應 | 說明 |
|-----------|-------------|------|
| 搜尋欄位 | `SearchInputWithButton` | `import 'package:b2b_manager/page/common/widgets/search_input_with_button.dart'` |
| 一般 TextField | `TextField` 或 `TextFormField` | 使用 `InputDecoration(border: OutlineInputBorder(...))` |
| 日期選擇 | `BuildDateSingleSelector` | `import 'package:b2b_manager/page/common/widgets/build_date_single_selector.dart'` |
| 月份選擇 | `MonthSelector` | `import 'package:b2b_manager/page/common/widgets/month_selector.dart'` |

---

## 下拉選單

| Figma 元素 | Flutter 元件 | import |
|-----------|-------------|--------|
| 單選下拉 | `MultiSelectDropDown(selectionType: SelectionType.single)` | `package:multi_dropdown/multiselect_dropdown.dart` |
| 多選下拉 | `MultiSelectDropDown(selectionType: SelectionType.multi)` | `package:multi_dropdown/multiselect_dropdown.dart` |
| 原生下拉 | `BuildPrimitiveDropdownMenu` | `build_primitive_dropdown_menu.dart` |

### MultiSelectDropDown 範例
```dart
import 'package:multi_dropdown/multiselect_dropdown.dart';

MultiSelectDropDown<String>(
  options: [
    ValueItem(label: '選項一', value: '1'),
    ValueItem(label: '選項二', value: '2'),
  ],
  selectionType: SelectionType.single,
  onOptionSelected: (options) {},
  hint: '請選擇',
  chipConfig: ChipConfig(wrapType: WrapType.scroll),
)
```

---

## 標籤（Tag / Badge）

| Figma 樣式 | Flutter 對應 | 說明 |
|-----------|-------------|------|
| 狀態標籤（綠/橘/藍） | `BuildTagBox` | `import 'package:b2b_manager/page/common/widgets/build_tag_box.dart'` |
| Chip 選項 | `ChoiceChip` 或 `FilterChip` | 搭配 `SLColor.b2bChipLabel` |
| 已選中 Chip | | 搭配 `SLColor.b2bSelectedChipLabel`, `SLColor.b2bChipSelectedLabelText` |
| 未選中 Chip | | 搭配 `SLColor.b2bChipLabel`, `SLColor.b2bChipLabelText` |

---

## 表格

| Figma 元素 | Flutter 元件 | 說明 |
|-----------|-------------|------|
| 一般資料表格 | `DataTable2` | `import 'package:data_table_2/data_table_2.dart'` |
| 分頁表格（同步） | `PaginatedDataTable2` | 搭配 `DataTableSource` |
| 分頁表格（非同步 API） | `AsyncPaginatedDataTable2` | 搭配 `AsyncDataTableSource` |

### 表格規範
```dart
// ⚠️ 表格容器高度用固定 px（不加 .h）
SizedBox(
  height: 600, // 固定像素，確保顯示 10 列
  child: DataTable2(
    headingRowColor: WidgetStateProperty.all(SLColor.tableHeader),
    columns: [
      DataColumn2(label: Text('欄位'), size: ColumnSize.M),
    ],
    rows: [...],
    fixedLeftColumns: 1, // 固定左側欄
  ),
)
```

---

## 圖表

| Figma 圖表類型 | Flutter 元件 | import |
|--------------|-------------|--------|
| 折線圖 | `LineChart` | `package:fl_chart/fl_chart.dart` |
| 圓餅圖 | `PieChart` | `package:fl_chart/fl_chart.dart` |
| 長條圖 | `BarChart` | `package:fl_chart/fl_chart.dart` |

---

## 對話框

| Figma 元素 | Flutter 元件 | import |
|-----------|-------------|--------|
| 確認對話框 | `CustomDialog` | `import 'package:b2b_manager/page/common/widgets/custom_dialog.dart'` |
| 篩選對話框 | `FilterListDialog` | `import 'package:filter_list/filter_list.dart'` |
| 側邊抽屜 | `CustomDrawer` | `import 'package:b2b_manager/page/common/widgets/custom_drawer.dart'` |

---

## 載入狀態

| 狀態 | Flutter 元件 | import |
|------|-------------|--------|
| 骨架載入 | `ShimmerLoading` | `import 'package:b2b_manager/page/common/widgets/shimmer_loading.dart'` |
| 全頁載入遮罩 | `context.loaderOverlay.show()` | `package:loader_overlay/loader_overlay.dart` |
| 空資料 | `NoDataWidget` | `import 'package:b2b_manager/page/common/widgets/no_data_widget.dart'` |

---

## Tab Bar

```dart
import 'package:b2b_manager/page/common/widgets/tab_bar_manager_widget.dart';

TabBarManagerWidget(
  tabs: ['標籤一', '標籤二', '標籤三'],
  children: [Widget1(), Widget2(), Widget3()],
)
```

---

## Icon 使用規則

```dart
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

// Font Awesome（品牌、特殊圖示）
FaIcon(FontAwesomeIcons.user, size: 20.w, color: SLColor.iconColor)

// Material Icons（一般 UI 圖示）
Icon(Icons.search, size: 20.w, color: SLColor.iconColor)
```
