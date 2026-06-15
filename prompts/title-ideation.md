# Title Ideation Prompt

你現在的任務是替既定題目發想：
- 高流量標題
- 封面文案
- 封面構圖方向

不要直接寫稿，也不要直接生圖。

## 先讀文件

- `docs/profiles/may-story/channel_scope.md`
- `docs/profiles/may-story/title_thumbnail_rules.md`
- `workspace/memory/style-corpus/maymei-title-benchmark.json`
- `workspace/memory/style-corpus/maymei-title-benchmark.md`
- `workspace/memory/style-corpus/maymei-thumbnail-benchmark.json`
- `workspace/memory/style-corpus/maymei-thumbnail-benchmark.md`
- `workspace/memory/style-corpus/maymei-thumbnail-text-annotations.json`

## 任務目標

- 產出一組可比較的標題候選
- 讓每個標題有清楚切角
- 先用頻道過往 YouTube Studio 數據建立歷史對照
- 補齊封面文案與構圖方向
- 找出最有點擊潛力、又不會和內容脫鉤的標題與封面組合

## 工作原則

- 標題、封面字也算文稿型任務，要套用 `maymei-script-finalizer+ 中文撰寫系統` 的底層流程。
- 正式發想前先鎖內容事實與不可承諾點，再判斷切角類型，最後才寫標題和封面字。
- 標題封面用的是 `切角卡`：觀眾痛點、點擊 promise、可用事實、不可承諾、歷史錨點、封面字方向。
- 使用者親自改過或明確認可的標題 / 封面字優先級最高；後續同類題目要先學那份的中文語感和 promise 強度。
- 產出後也要做 AI 文風驗收：檢查像不像玫玫頻道會用、會不會太英文翻譯腔、是否承諾過頭，再看數據分數。
- 標題判斷必須先依靠 `maymei-title-benchmark.json`，不要只憑主觀預測
- 封面字判斷必須先依靠 `maymei-thumbnail-benchmark.json`，不要只憑主觀預測
- 如果使用者給新的 YouTube Studio 匯出，先跑 `python scripts/build_maymei_title_benchmark.py <zip-or-csv-or-dir>`
- 如果需要更新頻道縮圖，先跑 `python scripts/build_maymei_thumbnail_benchmark.py`
- 只做長影片標題時，優先使用 `format: long` 的歷史錨點，不要讓 Shorts 數據混進長片判斷
- 每個 Top 3 候選至少要附 2 到 5 支可比歷史影片，列出 CTR、曝光、觀看、公式、封面字與相似理由
- ABC 測試要同時給 `標題 + 封面字`，不能只測標題
- 不要使用收益欄位判斷標題；收益不能當點擊 promise 的依據
- 沒有足夠歷史對照時，要標成 `低信心` 或 `資料不足`，不能硬推
- 一次先出多個版本，不要太早收斂
- 如果使用者沒有明確要求最後定案，預設先交 `高資訊量、可刪改的標題素材包`
- 標題先拆收益、損失、效率、反差、好奇、權威角度
- 可以借鏡外國爆款題型，但要翻成自然中文
- 避免只有情緒沒有資訊
- 避免標題和內容承諾對不上
- 避免只給標題不補封面方向
- 候選之間要保留夠大的切角差異，讓使用者可以混搭、刪改、再收斂
- 正式成品預設寫到 `workspace/deliverables/title/`

## 輸出格式

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
