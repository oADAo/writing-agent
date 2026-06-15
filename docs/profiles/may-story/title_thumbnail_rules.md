# 玫玫物語標題與封面方向規則

## 用途

這份文件負責替既定題目產出：
- 高流量標題
- 封面文案
- 封面構圖方向

這一版不直接生圖。

## 先過邊界

正式發想前，先讀：
- `docs/profiles/may-story/channel_scope.md`

如果題目本身不屬於頻道邊界，就不要硬做標題。

## 基本原則

- 標題一定要和內容 promise 對得上。
- 封面不是重複標題，而是補強資訊或情緒。
- 參考外國爆款可以，但要翻成自然的中文點擊語感。
- 標題與封面要一起看，不要各做各的。
- 標題判斷一律先依靠頻道過往數據，不要只憑主觀預測。
- 預設先交 `資訊量夠多、可刪改` 的標題素材包，不要太早只收成唯一標題。
- 如果使用者沒有明確要求最後定案，優先保留更多候選、切角理由、可替換字眼與不同強度版本。

## YouTube 歷史數據規則

正式發想前，先看：
- `workspace/memory/style-corpus/maymei-title-benchmark.json`
- `workspace/memory/style-corpus/maymei-title-benchmark.md`
- `workspace/memory/style-corpus/maymei-thumbnail-benchmark.json`
- `workspace/memory/style-corpus/maymei-thumbnail-benchmark.md`
- `workspace/memory/style-corpus/maymei-thumbnail-text-annotations.json`

如果使用者提供新的 YouTube Studio 匯出，先跑：

```powershell
python scripts/build_maymei_title_benchmark.py "<zip-or-csv-or-folder>"
```

如果需要更新頻道縮圖，先跑：

```powershell
python scripts/build_maymei_thumbnail_benchmark.py
```

標題判斷時要遵守：
- 長影片標題只用 `format: long` 當主要歷史錨點；Shorts 只能當補充，不要混進主判斷。
- 優先找同遊戲、同公式、同玩家需求、同標題語法的可比影片。
- 每個 Top 3 候選都要附 2 到 5 支歷史錨點；至少列出 `標題 / 公式 / CTR / 曝光 / 觀看 / 相似理由`。
- 每個 Top 3 候選也要附可比封面錨點；至少列出 `封面字 / 縮圖連結或本地路徑 / 相似理由`。
- 如果同遊戲樣本不足，就退到同公式或同玩家需求；如果仍不足，要標成 `低信心`。
- 不要使用收益欄位判斷標題；收益不能當標題 promise 的依據。
- 不要把高觀看直接等同好標題；要一起看曝光、CTR、觀看、平均觀看比例與題材盤子。

## 封面字資料規則

- 封面字和標題是同一組 promise，要一起判斷，不要分開做。
- 封面圖資料只能從 `玫玫物語` YouTube 頻道抓縮圖，再用 `video_id` 對回 YouTube Studio benchmark。
- 不要沒有看圖就假裝知道封面寫了什麼；沒有可靠辨識時，`thumbnail_text_source` 要保持 `pending_manual_review`。
- 封面字要短、可視覺化，通常比標題更像「第一眼理由」。
- A/B/C 測試一律要同時列：
  - `Title`
  - `Thumbnail Text`
  - `Thumbnail visual promise`
  - `Historical title anchor`
  - `Historical thumbnail anchor`

## 標題分數卡

每個 Top 3 候選都要用 1 到 5 分標記：
- `歷史公式貼合度`
- `CTR 錨點強度`
- `曝光量級信心`
- `玩家需求清晰度`
- `內容承諾安全性`
- `封面互補度`

分數不是裝飾，要用歷史錨點解釋；如果只是感覺，寧可不給高分。

## 發布後回測

每次定稿後保留 `Retro Fields`，方便發片後補：
- 發片日期
- 實際標題與封面版本
- 24h / 72h / 7d 觀看
- 曝光次數
- CTR
- 平均觀看時間
- 平均觀看比例
- 主要流量來源
- 是否改標題或封面
- 這次要保留、修正或淘汰的標題規則

## 標題切角框架

每次發想前，至少先拆這幾種角度：
- 收益
- 損失
- 效率
- 反差
- 好奇
- 權威

不是每支影片都要六種全用，但至少要明確知道目前候選標題走的是哪一個角度。

## 標題寫法要求

- 一次先出多個版本，不要第一個就定案。
- 標題要有具體資訊，不要只剩情緒。
- 標題要優先對應這個頻道常見題型：
  - 買前必知
  - 新手必看
  - 第一天一定要做
  - 每天必做
  - 前期速衝
  - 機制拆解
- 如果是從外國爆款轉譯來的，要點出它的原始爆點是什麼。
- 候選之間最好保留明顯差異，讓使用者可以刪、改、混搭，而不是只是同一句小改字。

## 封面文案要求

- 封面文案要短，讀一眼就懂。
- 盡量讓封面補資訊，而不是只是把標題縮短。
- 一個封面方向通常只留 1 到 2 句短文案。
- 可以強調：
  - 大錯誤
  - 關鍵收益
  - 最大反差
  - 最值得先做的事

## 封面構圖方向要求

每個方向都要說清楚：
- 主畫面主角是誰
- 要突出哪個資訊
- 文案放哪裡
- 視覺對比重點是什麼

常見可用方向：
- `角色 / 主角 + 關鍵 UI + 大字收益`
- `前後對比`
- `錯誤 vs 正解`
- `稀有 / 隱藏重點放大`
- `大數字 + 系統畫面`

## 標題與封面搭配原則

- 標題負責主要 promise。
- 封面負責補一個最直觀的點擊理由。
- 如果標題已經很具體，封面可以更短更狠。
- 如果標題比較偏好奇，封面要補足具體資訊。
- 先把好用的材料攤開，再決定哪一組最終成對。

## 禁止行為

- 不要只給 1 個標題就收工。
- 不要把封面文案寫成完整句子一大串。
- 不要直接把外文爆款標題硬翻成生硬中文。
- 不要做出內容根本撐不起來的誇張 promise。
- 不要只寫標題，不補封面構圖方向。

## 固定輸出格式

```md
# Title Pack

## Topic

## Historical Data Baseline

## Thumbnail Data Baseline

## Comparable Title Anchors

## Top 3

## ABC Title + Thumbnail Text Tests

## 10 Candidate Titles

## Title Scorecard

## Data-Based Click Hypothesis

## Angle Notes

## 3 Thumbnail Copy Options

## 3 Thumbnail Composition Directions

## Final Title + Thumbnail Pair

## Retro Fields
```

## 一句話版交接

這一步不是亂想聳動句子，而是先用 `玫玫物語` 過往 YouTube Studio 數據找可比錨點，再把既定題目拆成高點擊切角，做出一組能直接拿去拍封面的標題與封面方向。
