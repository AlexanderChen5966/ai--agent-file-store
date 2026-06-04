---
name: figma-to-flutter
description: "Convert Figma screenshots into Flutter UI code for the B2B Manager project (山隆 B2B 智慧平台). Use when the user provides a Figma screenshot and wants to generate Flutter widget or page code. Enforces project conventions: SLColor, SLText, SpacerWidget, HookConsumerWidget, Riverpod, and flutter_screenutil (.w/.h/.sp). Triggers: 截圖轉代碼, 把這個設計做成Flutter, 依照截圖生成UI, Figma截圖, 幫我實作這個畫面, 依照設計稿."
---

# Figma → Flutter（B2B Manager）

## 工作流程

### Step 1：分析截圖

收到截圖後，立即識別：
- **版面結構**：Column / Row / Stack / GridView
- **UI 元件清單**：按鈕、輸入框、表格、下拉選單、標籤、圖表
- **區塊劃分**：Header / 搜尋列 / 主體 / Pagination

若截圖模糊或資訊不足，向用戶提問（最多 2 個問題，合併一次問完）。

### Step 2：確認必要資訊

在生成代碼前，確認以下（若截圖已清楚則跳過）：

```
1. 元件/頁面名稱？（用於命名 class 和檔案）
2. 放在哪個功能目錄？（lib/page/[功能]/widgets/ 或 lib/page/[功能]/）
3. 需要狀態管理嗎？（純顯示 → ConsumerWidget；有互動 → HookConsumerWidget）
```

### Step 3：生成代碼

依照以下規則輸出完整 Flutter 代碼：

#### 核心規範（必須遵守）

1. **顏色** → 優先使用 `SLColor.*`；若 Figma 顏色不在 SLColor 中，新增至 `lib/util/effect/color_style.dart` 並使用新變數，禁止 hardcode HEX
2. **文字** → 使用 `SLText` / `SLText.title` / `SLText.body`（fontFamily: NotoSansTC）
3. **尺寸** → 依情況判斷（見下方「響應式尺寸判斷規則」）
4. **間距** → `SpacerWidget(width: spacerSmallSize)` 或 `SpacerWidget(height: spacerMediumSize)`（常數，不加 `.w/.h`）
5. **圓角** → `kAppRadius = 8`（常數，不加 `.w`）
6. **按鈕** → `PositiveButton` / `NegativeButton` / `BuildIconBtn`（禁止直接用 ElevatedButton）
7. **Widget 類型** → 有狀態/互動：`HookConsumerWidget`；純顯示：`ConsumerWidget`

#### 響應式尺寸判斷規則

**使用 `.w` / `.h` / `.sp`（需要隨螢幕縮放）：**
- 版面容器寬高（如 `width: 300.w`）
- 自訂的 padding / margin（如 `EdgeInsets.all(16.w)`）
- 圖示尺寸（最小 `20.w`）
- 字體（最小 `12.sp`，需要縮放時才加）
- 需要在不同解析度正確比例呈現的元素

**不使用 `.w` / `.h`（固定像素）：**
- 表格容器高度（必須固定 px，如 `SizedBox(height: 600)`，加 `.h` 會導致小螢幕顯示列數不足）
- `SpacerWidget` 的 `spacerSmallSize` / `spacerMediumSize`（已是常數，加 `.h` 反而錯誤）
- `kAppRadius = 8`（常數，不加 `.w`）
- 使用 `const` 的 Widget 內部（`const` 與 screenutil 不相容，使用 screenutil 必須移除 `const`）
- 固定高度的系統元件（如 `AppBar`、`Divider`）

詳細色彩、元件、Riverpod 規範請參考：
- **[b2b-conventions.md](references/b2b-conventions.md)**：色彩系統（含新增規則）、文字樣式、常用元件 API
- **[component-mapping.md](references/component-mapping.md)**：Figma UI 元素 → Flutter 元件對應表

詳細色彩、元件、Riverpod 規範請參考：
- **[b2b-conventions.md](references/b2b-conventions.md)**：色彩系統、文字樣式、常用元件 API
- **[component-mapping.md](references/component-mapping.md)**：Figma UI 元素 → Flutter 元件對應表

#### 標準 Widget 結構

**純顯示（ConsumerWidget）：**
```dart
import 'package:b2b_manager/util/effect/color_style.dart';
import 'package:b2b_manager/util/effect/radius_style.dart';
import 'package:b2b_manager/util/view/sl_text.dart';
import 'package:b2b_manager/util/view/spacer_util.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

class MyWidget extends ConsumerWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Container(
      width: 300.w,
      padding: EdgeInsets.symmetric(horizontal: 16.w, vertical: 12.h),
      decoration: BoxDecoration(
        color: SLColor.cardBg,
        borderRadius: BorderRadius.circular(kAppRadius),
        border: Border.all(color: SLColor.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SLText.title(text: '標題'),
          SpacerWidget(height: spacerSmallSize),
          SLText.body(text: '內容說明'),
        ],
      ),
    );
  }
}
```

**有互動（HookConsumerWidget）：**
```dart
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

class MyInteractiveWidget extends HookConsumerWidget {
  const MyInteractiveWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isExpanded = useState(false);
    // ref.watch() 監聽 Provider 變化
    // ref.read() 一次性讀取（在事件回呼中使用）
    return ...;
  }
}
```

### Step 4：輸出格式

每次輸出必須包含：
1. **檔案路徑**（如 `lib/page/order/widgets/order_search_bar.dart`）
2. **完整代碼**（含所有 import）
3. **使用方式**（一行範例說明父 Widget 如何引用）
4. **注意事項**（如需 build_runner、需新增路由、需新增 Provider 等）

---

## 截圖品質提示

若截圖模糊或缺少設計規格，主動建議：
> 「可以在 Figma 右側開啟 Inspect 面板一起截圖，能看到精確的顏色 HEX 和間距數值，生成結果會更準確。」
