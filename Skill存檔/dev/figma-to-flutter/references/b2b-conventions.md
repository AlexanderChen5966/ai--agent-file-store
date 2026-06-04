# B2B Manager Flutter 開發規範

## 色彩系統（SLColor）

```dart
import 'package:b2b_manager/util/effect/color_style.dart';
```

### 找不到對應顏色時：新增至 SLColor

當 Figma 設計中的顏色在 SLColor 中找不到對應，**新增至 `lib/util/effect/color_style.dart`**，不可 hardcode HEX：

```dart
// lib/util/effect/color_style.dart
@immutable
class SLColor {
  // 依用途分組，加在對應的區塊後面
  static const myNewColor = Color(0xFFXXXXXX); // 說明用途
}
```

**命名規範：**
- camelCase
- 按用途命名，不按顏色命名（`orderStatusPending` ✅，`lightOrange` ❌）
- 若是某功能專用，加前綴（`orderXxx`、`driverXxx`）

| 用途 | 變數名 | HEX |
|------|--------|-----|
| 主色（按鈕/Header） | `SLColor.primaryButton` | `#009CDE` |
| 主色 Hover | `SLColor.primaryButtonHover` | `#0170A3` |
| 主色 Pressed | `SLColor.primaryButtonPressed` | `#065E86` |
| 白色 | `SLColor.white` | `#FFFFFF` |
| 主要文字 | `SLColor.text` | `#343434` |
| 次要文字（灰） | `SLColor.textGray` | `rgba(119,125,139,1)` |
| Icon 色 | `SLColor.iconColor` | `#726B66` |
| 頁面背景 | `SLColor.primaryBackground` | `#EBEDFO` |
| 卡片背景 | `SLColor.cardBg` | `#FFFFFF` |
| 表格 Header | `SLColor.tableHeader` | `#FCD757`（黃） |
| 邊框 | `SLColor.border` | `#B4B0AD` |
| Disable 邊框 | `SLColor.disableBorder` | `#C4C1BF` |
| 刪除按鈕 | `SLColor.deleteButton` | `#D95303` |
| 次要按鈕（黃） | `SLColor.secondaryButton` | `#FCD757` |
| Disable 按鈕 | `SLColor.disableButton` | `#E8E6E6` |
| Disable 文字 | `SLColor.disableButtonText` | `#95908C` |
| 成功 | `SLColor.systemConfirm` | `#2AA328` |
| 錯誤 | `SLColor.systemError` | `#FC5555` |
| 資訊 | `SLColor.systemInfo` | `#236DB1` |
| 關閉 | `SLColor.systemClose` | `#C4C1BF` |

### Tag 色彩
```dart
SLColor.tagActive / SLColor.tagActiveBg       // 啟用：深綠 / 淺綠背景
SLColor.tagInvited / SLColor.tagInvitedBg     // 邀請中：深藍 / 淺藍背景
SLColor.tagInactive / SLColor.tagInactiveBg   // 停用：深橘 / 淺橘背景
SLColor.tagRejected / SLColor.tagRejectedBg   // 拒絕：深棕 / 淺棕背景
```

---

## 文字系統（SLText）

```dart
import 'package:b2b_manager/util/view/sl_text.dart';
```

| Factory | 預設字體 | 預設粗細 | 用途 |
|---------|---------|---------|------|
| `SLText.title(text: '')` | 20 | w600 | 頁面標題 |
| `SLText.medium(text: '')` | 18 | w400 | 副標題 |
| `SLText.body(text: '')` | 15 | w400 | 一般內文（含 ellipsis） |
| `SLText(text: '', fontSize: 12)` | 12 | normal | 小字（表格欄位等） |

所有 SLText 使用 `fontFamily: 'NotoSansTC'`，**不需要額外指定**。

### 自訂範例
```dart
SLText(
  text: '自訂文字',
  fontSize: 14,
  color: SLColor.textGray,
  fontWeight: FontWeight.w600,
  maxLine: 2,
  overflow: TextOverflow.ellipsis,
)
```

---

## 間距系統（SpacerWidget）

```dart
import 'package:b2b_manager/util/view/spacer_util.dart';

const double spacerSmallSize = 12;
const double spacerMediumSize = 16;

SpacerWidget(width: spacerSmallSize)   // 水平間距 12
SpacerWidget(height: spacerSmallSize)  // 垂直間距 12
SpacerWidget(width: spacerMediumSize)  // 水平間距 16
SpacerWidget(height: spacerMediumSize) // 垂直間距 16
```

---

## 圓角系統

```dart
import 'package:b2b_manager/util/effect/radius_style.dart';

const double kAppRadius = 8; // 所有元件統一圓角
BorderRadius.circular(kAppRadius)
```

---

## 尺寸規範（flutter_screenutil）

**基準解析度：1920×1024**

```dart
import 'package:flutter_screenutil/flutter_screenutil.dart';
```

### 使用 `.w` / `.h` / `.sp`
```dart
width: 300.w      // 版面容器寬度
height: 200.h     // 版面容器高度（非表格）
fontSize: 16.sp   // 字體大小
EdgeInsets.all(16.w)  // 自訂 padding/margin
size: 20.w        // icon 尺寸（最小 20.w）
```

### 不使用 `.w` / `.h`（固定像素）
```dart
// 表格容器：固定 px，確保任何解析度都能顯示 10 列
SizedBox(height: 600, child: DataTable2(...))

// SpacerWidget 常數（spacerSmallSize=12、spacerMediumSize=16 已是 double，不加 .h）
SpacerWidget(height: spacerSmallSize)

// kAppRadius 常數
BorderRadius.circular(kAppRadius) // 不加 .w

// const Widget 內部（const 與 screenutil 不相容）
// 使用 screenutil 時必須移除 const
```

**最小規範：**
- 最小 icon 尺寸：`20.w`
- 最小字體：`12.sp`

---

## 按鈕元件

```dart
import 'package:b2b_manager/page/common/widgets/custom_button.dart';

// 主要按鈕（藍底白字）
PositiveButton(
  text: '確認',
  onPressed: () {},
  buttonSize: ButtonSize.small, // ButtonSize.medium / ButtonSize.large
)

// 次要按鈕（白底藍框）
NegativeButton(
  text: '取消',
  onPressed: () {},
)

// Icon 按鈕
BuildIconBtn(
  icon: Icons.edit,
  onPressed: () {},
  size: 24,
  color: SLColor.iconColor,
)

// 文字按鈕
BuildTextBtn(
  text: '查看更多',
  onPressed: () {},
  color: SLColor.primaryButton,
)
```

---

## 卡片元件

```dart
import 'package:b2b_manager/page/common/widgets/custom_card.dart';

// 標準 Card（白底、圓角、陰影）
CustomCard(
  child: Padding(
    padding: EdgeInsets.all(16.w),
    child: ...,
  ),
)
```

---

## Riverpod 狀態管理

```dart
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

// 簡單布林狀態
final isExpandedProvider = StateProvider<bool>((ref) => false);

// 複雜業務邏輯
final myFeatureProvider = StateNotifierProvider<MyNotifier, MyState>((ref) {
  return MyNotifier();
});

// 在 Widget 中使用
class MyWidget extends HookConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(myFeatureProvider);       // 監聽並重建
    final notifier = ref.read(myFeatureProvider.notifier); // 觸發事件時使用

    final localState = useState(false); // 本地狀態（flutter_hooks）

    return ...;
  }
}
```

---

## 標準頁面結構

```dart
class MyPage extends StatefulHookConsumerWidget {
  const MyPage({super.key});
  static const String ROUTE_NAME = '/my_page';

  @override
  State<MyPage> createState() => _MyPageState();
}

class _MyPageState extends ConsumerState<MyPage> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      // 初始化 API 呼叫放這裡
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: SLColor.primaryBackground,
      body: Column(
        children: [
          // Header
          // 搜尋列
          // 主體內容（含表格）
        ],
      ),
    );
  }
}
```
