# 已知的差異原因

`flutter-ui-compare` 第 7 步用。依症狀查，照「驗算」確認是不是這個原因，再套「修法」。

| 症狀 | 原因 | 驗算 | 修法 |
|---|---|---|---|
| Flutter 文字比網頁寬 3～5%（數字多的更明顯） | Flutter `ThemeData` 沒關 Material 3，TextTheme 帶字距：bodyMedium 0.25、titleSmall／labelLarge 0.1、bodySmall 0.4、bodyLarge 0.5 | 字數 × 字距 ≈ 寬度差 | 網頁對應的文字加同樣的 `letter-spacing` |
| 按鈕裡的文字字型或字寬不對 | 原生 `<button>` 不繼承字型與字距（Chrome 預設 Arial、字距 normal） | 讀 `getComputedStyle(button).fontFamily` | 全站樣式加 `button { font-family: inherit; letter-spacing: inherit }` |
| 固定高度的區塊比 Flutter 高（差值剛好是上下 padding 或框線） | Flutter `Container(height:, padding:)` 的 height 含 padding；網頁元素是 `content-box`（關掉 CSS reset 的專案、antd Modal 內部都是） | 高度差 = padding＋框線 | 該元素加 `box-sizing: border-box` |
| 同一個共用元件，在不同頁面量到的文字位置差 1px（有的頁一致、有的頁差 1） | 置中後的位移落在半像素（例：(46 − 23) / 2 = 11.5），Chrome 依元素在頁面上的位置把半像素進位到上或下 | DOM 讀文字元素的 `getBoundingClientRect().top`，小數是 .5 就是這個原因 | 調整外層高度或內距，讓置中後的位移是整數（b2b-manager 表頭：內容區上方留 1，(45 − 23) / 2 = 11） |
| 多行或單行文字的區塊高度不同 | Flutter 文字行高約 1.5 倍（NotoSansTC） | 字級 × 1.5 ≈ Flutter 的行高 | 網頁給 `line-height: 1.5` |
| 多行輸入框的第一行文字比 Flutter 高約 20px（左邊也差幾 px） | Flutter 輸入元件的 title 傳空字串仍佔一行高（例：b2b-manager `SLInputTextField(title: '')` 用 16px 字的空 `SLText`），下面再加 TextField 的 `contentPadding` | 讀 widget 原始碼：空 title 一行（字級 × 約 1.45）＋ contentPadding top；實測「框線到第一行字」的距離 | 網頁輸入框的 `padding-top` 補上差值（b2b-manager 工單申請：antd 8.5 → 30.5、左 11 → 18） |
| 輸入框、下拉的文字距左框不同 | Flutter 輸入元件的內距是「框線＋padding＋contentPadding」相加，和 UI 套件預設不同 | 讀 Flutter widget 原始碼把三個值相加 | 調整網頁元件的 `padding-inline-start` |
| 標題列比 Flutter 高幾 px | `inline-flex` 對齊 baseline，放在標題元素裡會多出下伸部空白 | 把 display 改成 `flex` 後重量 | 用 block 層級的 flex |
| hover 時網頁變色、Flutter 不變 | Flutter InkWell 的墨水被父層 `Container(color:)` 蓋住 | 在 Flutter 上真實 hover 截圖 | 以 Flutter 實測為準，網頁不加 hover 底色 |
| 停用的按鈕 Flutter 仍有 tooltip | Flutter `IconButton` 有 tooltip 時停用也會顯示 | 在 Flutter 上 hover 停用的按鈕 | 網頁停用狀態保留 tooltip |
| 下拉選單可見高度差很多 | UI 套件的選單高度上限和 Flutter 元件不同（antd Select 預設 256） | 讀 Flutter 下拉元件的上限 | 設定網頁元件的選單高度 |
| icon 粗細或形狀略有不同 | 兩邊 icon 字型版本不同（例：FontAwesome Pro 對免費版） | 比對兩邊載入的字型檔 | 由使用者決定 |
| icon 後面的文字左右偏移幾 px | Flutter `FaIcon` 的寬度＝字形寬（不是正方形，`font_awesome_flutter/lib/src/fa_icon.dart`）；Pro icon 換成免費 icon 時字形寬不同（例：`solidMemoCircleInfo` 576/512×24＝27、`faFileLines` 384/512×24＝18） | 查兩個 icon 的 viewBox 寬度 ×（icon 大小／512），相減等於偏移量 | 網頁 icon 外包一層，寬度設成 Pro 字形的寬（b2b-manager 是 `IconLabel` 的 `iconWidth`） |
| 粗體字筆畫不同 | Flutter 打包了各字重的字型檔，網頁只宣告 Regular、粗體由瀏覽器合成 | 查網頁 `@font-face` 宣告了哪些字重 | 由使用者決定 |
| 日期在某些瀏覽器顯示錯誤 | 後端回 `yyyy-MM-dd HH:mm:ss`（空白分隔），Safari 的 `new Date()` 不接受 | 看實際回應的日期字串 | 解析前轉成 ISO 格式 |
