# 2026 東京冬令營 — 交接說明

給接手這個專案的 Claude（或任何人）。開工前先讀完這份。

## 專案是什麼

12/13–12/19 東京＋輕井澤家族旅行的行程網站，單一自含式 HTML（index.html），放在 GitHub Pages：
https://stuart0401.github.io/2026Winter/

- 航班：JX314 台中 09:15 → 成田第 2 航廈 13:25；JX315 成田第 2 航廈 14:25 → 台中 17:55
- 住宿：TOSEI酒店 可可尼築地銀座（12/13、12/15–12/18）；輕井澤英迪格酒店（12/14）
- 分組：大邱組（A，圖示是棒球＋手套）、三口組（B，圖示是三個人）

## 使用者的工作規則（一定要遵守）

1. **推送前先讓使用者確認改動。** 流程：改 `src/` → 建置 → 跑測試 → 發布到預覽頁面 → 等使用者回「核准」→ 才推 GitHub（不再同步任何「主版」頁面）。使用者明說「直接推」時才可跳過確認。
2. **GitHub 首頁檔名只能是 `index.html`，放在 repo 根目錄。** 不可改名、不可放進子資料夾，否則網址會打不開。
3. 回覆用繁體中文；說明要白話，使用者不需要知道工具細節。
4. 使用者說某個待議「已解決」時，直接把那一項刪掉，不要保留打勾。
5. **對話長度提醒。** 對話一旦被自動壓縮過（開頭變成一份先前對話的摘要），之後每次回報完成時，在結尾加一句：「這個對話已經壓縮過，建議先把新的決定補進 HANDOFF.md、推上 GitHub，再開新對話接手。」使用者說「先不用換」時，改成每 5 次回覆提醒一次。

## 已取消、不要再提的項目

- 用 taste-site 重新設計整站風格
- 照片 EXIF 浮水印
- 每日頁首插圖動畫（已改回靜態圖）
- 把 12/17 拆成兩天（暫緩）

## 檔案結構

```
index.html          ← 建置產物，GitHub Pages 讀這個。不要手改，改 src/ 再建置。
src/build_site.py   ← 主程式：HTML/CSS/JS 樣板＋所有行程資料
src/illus.py        ← 手繪風 SVG 插圖（每張是一個函式，登記在 ALL；記帳頁用 ledger）
src/gen.py          ← 顏色主題（LIGHT/DARK）、填色類別、圖示；它的 __main__ 是舊設計稿，用不到
tests/check.py      ← 回歸檢查
HANDOFF.md          ← 這份
```

建置與檢查（在 repo 根目錄）：

```
python3 src/build_site.py            # 產出 ./index.html
python3 src/build_site.py /tmp/x.html  # 產出到別處（做預覽用）
python3 tests/check.py [檔案]          # 預設檢查 ./index.html，印出「全部通過」才算過
```

推送：`git -c push.negotiate=true push origin main`。推完 GitHub Pages 約 1 分鐘生效，驗證時網址加 `?v=任意字` 避開快取。

## build_site.py 裡的資料（都是 JS 常數，寫在 Python 樣板字串裡）

- **DAYS**：每天一筆 `{id:"d1"…"d7", date, wd, title, sub, art, seal, stay, stayArt, stayNote, memo?, tips?, shuttle?}`，行程三種寫法：
  - 一般日：`items:[…]`
  - 全天分組（12/16）：`groups:{A:{name, note?, items}, B:{…}}`
  - 部分分組（12/13）：`pre:[…]`（兩組一起）＋ `groups` ＋ `post:[…]`（會合後）
  - 分組日的組名預設是 GNAME（A 大邱組、B 三口組）。某天要用別的組名時，在那天加 `gnames:{A:"邱博組",B:"悠閒組"}`，圖示用 `gicons:{A:"cap",B:"cup"}`（GICON 裡的鍵）。記帳的組別標籤會自動跟著用當天組名。
- **行程項目的種類**：
  - 卡片：`{t, title, note, art, spot?, opt?:"選配", link?, extra?, shop?}`
  - 移動列：`{t, title, note, m:"train|bus|car|taxi|walk|plane|bowl|bag…", shop?, dir?, ql?}`；有 `dir`（Google 地圖路線網址）時地圖按鈕改成「Google 地圖車程」
  - 交通二選一：`{t, alt:true, title, opts:[{tag, m, title, note, q 或 dir, ql}]}`
  - 英迪格接駁車：`{t, sh:"to"|"from", title, note}`
- **MAPQ**：行程標題 → Google 地圖搜尋字串。地圖按鈕靠標題對應，改標題時記得同步改這裡。
- **SPOTS**：行程確認清單。**索引不能變動**（勾選狀態用索引存）。刪除時加 `gone:true`，新增時接在後面並用 `ord` 排順序。
- **TODO**：兩類（待議、待辦），項目 `{id, n, d?, opt?}`，用 `id` 存勾選。
- **PACK**：打包類別。**新類別只能加在最後面**（勾選用 `類別索引-項目索引` 存，插在中間會讓大家的勾選錯位）。項目可以是字串，或 `{n, d}`（d 是灰色小字說明）。
- **NEAR**：住宿附近超商・超市；**SHOP**：順路購物清單（`{k, n, w, h, q}`）。兩者都用 `listHTML()` 畫成可收合清單。
- **SHUTTLE**：英迪格接駁車時刻。
- **記帳（LEDGER）由行程自動產生**，改行程時記帳頁會跟著變，通常不用另外改：
  - 機票：DAYS 裡 `m:"plane"`、標題以航班號開頭的項目（id `fly:JX314`）；住宿：DAYS 的 `stay`，連續同一家合併（id `stay:飯店名:第一晚日期`）。
  - 每天：DAYS 的行程項目（id `日id:標題`）。預設會記帳：交通（train/bus/taxi/bike/car，接駁車 `sh` 除外）、吃飯（bowl）、交通二選一、`spot`、`opt`、有 `shop` 的項目。
  - 個別項目用 `led` 調整：`false` 不記帳（例如免費景點、已含在住宿的）、`true` 要記帳、`"名稱"` 改記帳名稱、`{n, d, c, a, all}` 改名稱／說明／幣別／預設金額，`all:true` 不標組別。新增行程時想一下要不要加 `led`。
  - `LED_PRE`（旅平險、eSIM、台灣端接送、JTTP 收入印紙）和 `LED_ETC`（Suica、機場）是手寫的，id 不能改。
  - **改行程標題＝記帳 id 改變。** 使用者已填金額的舊項目不會消失，會出現在「行程已變更的項目」，也算進合計，由使用者自己刪。所以改標題沒關係，但不要為了改字而大量改標題。
- 記帳匯出：Excel 是瀏覽器端自己組 .xlsx（`ledXlsx()`，不靠外部程式庫，含 SUMIF 合計公式）；PDF 是 `ledPrint()` 產生 `#ledprint` 列印版面後呼叫列印，使用者選「儲存為 PDF」。

## 瀏覽器端儲存

- localStorage 前綴 `twc26:`：spots、todo、todoOpen、pack、packOpen、packCustom（`{類別索引:[{id,n}]}`）、packHidden、day、group、theme；記帳：ledger（`{項目id:{a:金額,c:幣別}}`）、ledgerHidden、ledgerCustom（`{區塊id:[{id,n}]}`，自訂項目的 id 存成 `"c"+id`）、ledgerRate、ledgerOpen
- IndexedDB `twc26` / `photos`：使用者拍的照片（只存在該裝置）

## 慣例

- Google 地圖連結：搜尋用 `https://www.google.com/maps/search/?api=1&query=…`；指定出發時間的路線用 `…/data=!4m6!4m5!2m3!6e0!7e2!8j<把當地時間當 UTC 算的 epoch>!3e0`（3e0 開車、3e3 大眾運輸）。
- 營業時間、步行時間、班次都是查 Google 地圖得來，頁面上標註「以 Google 地圖為準」之類的提醒。
- 另開新視窗的連結，`aria-label` 結尾一定是「（另開新視窗）」（tests/check.py 會檢查）。
- 新插圖：在 `illus.py` 用現有的 `svg()`、`sky()`、`win()` 等積木畫，只用 `f-*` 填色類別（深色模式才會自動換色），最後 `ALL.update({...})` 登記。

## Artifact（claude.ai 上的頁面）

- **GitHub 是唯一的正式版本。** 不維護「主版」頁面；以前對話留下的頁面不用管，也不要試著更新（別的對話建立的頁面，通常改不動）。
- **預覽頁面由每個對話自己建立。** 對話中第一次要給使用者確認時，用建置出的 index.html 新建一個預覽頁面（標題如「2026 東京冬令營 預覽版」），之後在同一個對話裡都更新這一個；再次發布前先用 list_files 或 get_artifact 取得目前版本號，當作 base_version。
- 萬一連新建頁面都不行，就把建置出的 index.html 直接傳給使用者確認。
