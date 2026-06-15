# Script Writing Prompt

你現在的任務是把研究資料轉成 `玫玫物語` 可直接使用的長影片腳本。

這一步只寫長影片，不處理封面、標題、描述或社群貼文。

## 先讀文件

- `docs/profiles/may-story/content_rules.md`
- `docs/profiles/may-story/voice_memory.md`
- `docs/profiles/may-story/article_taxonomy.md`
- `docs/profiles/may-story/script_template.md`
- `workspace/memory/style-corpus/google-maymei-game-scripts.md`
- `skills/maymei-script-finalizer/SKILL.md`
- `skills/maymei-script-finalizer/references/chinese-writing-system.md`
- `skills/maymei-script-finalizer/references/finalizer-rubric.md`
- `docs/profiles/may-story/writing-retention-system.md`
- `docs/profiles/may-story/maymei-micro-voice-fingerprint.md`
- `docs/profiles/may-story/anti-ai-chinese-patterns.md`

## 任務目標

- 先完成結構稿
- 再產完整稿
- 保持 `玫玫物語` 的實際口氣與帶路感

## 工作原則

- 不管這次是哪種長片文稿，都必須先套用 `maymei-script-finalizer+ 中文撰寫系統`。
- 正式寫稿前先鎖事實、判片型、檢索同片型樣本或使用者認可稿、建立章節卡，再逐章寫正文。
- 正式稿不能直接從研究包生成全文。先建立 `包裝承諾卡 / 玩家雙層問題卡 / 章節留存卡`，再讓 AI 先審大綱，最後才逐章寫。
- 檢索同片型樣本不能省略。依題目、遊戲、片型先執行：

```powershell
python scripts/retrieve_maymei_writing_guidance.py --topic "<題目>" --game "<遊戲名>" --formula "<片型>" --markdown --output "workspace/memory/style-corpus/retrieved-writing-guidance-<slug>.md"
```

- 如果樣本不足或需要更精準對照，再執行：

```powershell
python scripts/retrieve_maymei_samples.py --topic "<題目>" --game "<遊戲名>" --formula "<片型>" --output "workspace/memory/style-corpus/retrieved-samples-<slug>.json"
```

- 撰寫前回報準備時，必須說清楚這次判定的片型、參考到的同片型樣本、會學哪些文稿特徵、最後會如何打分；不能只說「我會依照你的風格寫」。
- 使用者親自改過或明確認可的版本優先級最高；同類稿要先學那版的句長、轉場、章節收尾和判斷語氣。
- 先做 AI 文風驗收，再跑機械檢查；機械分數不能取代使用者體感。
- 先判斷這支片是 `新手開局 / 完整攻略 / 資源效率 / 配裝流派 / 排行精選 / 推薦清單 / 買前必看` 的哪一種
- 片型一旦判錯，後面的 promise、段落節奏和收尾口氣都會偏掉，所以不要跳過這一步
- 長片正式稿預設保留固定自介：`大家好~這裡是玫玫物語`
- 固定自介和影片 promise 要拆成兩段，不要揉成一大句
- 影片 promise 要盡快講出觀眾能得到什麼，不要只講情緒或背景
- 如果抽象規則和聲線記憶有衝突，以 `voice_memory.md` 為準
- 如果要學真正像玫玫的外層框架，優先參考 `google-maymei-game-scripts.md`
- 先整理事實、重點、觀眾收益，再開始寫
- 無論是哪一種文案研究，都不能只靠官方來源；官方只用來校正基本事實。
- 每次都要補玩家社群或留言訊號，依遊戲生態查 `YouTube 高讚留言 / B站留言或動態 / 巴哈姆特 / Reddit / Steam 討論 / X / Threads / Discord 公開討論 / 評論區 / 玩家攻略站`。
- 玩家社群訊號要用來判斷：觀眾真正想知道什麼、擔心什麼、哪裡不懂、哪些賣點最有感、哪些說法不能講死。
- 有時效性的資訊要先重新確認
- 最終成稿要能直接使用，不要保留研究筆記腔
- 不要跳過結構直接寫全文
- 正式成品預設寫到 `workspace/deliverables/script/`
- 完成 `正式文案 / 最終定稿 / 可直接朗讀版` 後，預設建立 Google Docs 文件並回傳連結；如果只是研究包、章節池或素材包，不必強制建立，除非使用者要求。
- Google Docs 文件標題要清楚標出頻道、遊戲或主題、文案類型與日期。
- 完稿後固定跑：

```powershell
python scripts/check_maymei_final_draft.py <draft> --json
python scripts/check_maymei_ai_patterns.py <draft> --json
python scripts/check_maymei_read_aloud_friction.py <draft> --json
```

- 分數低於 `85` 不可交稿；分數通過但 AI 文風驗收覺得不像，也要二修。
- 正式交付要包含 `Voice Check`：AI 人工審稿結論、機械分數、是否通過 85 分、參考樣本與二修摘要。
- 如果使用者明確說自己會再刪改、要的是 `文章內容 / 素材 / 資訊越多越好`，或沒有明確要求最終定稿，預設先交資訊密度高的素材包，不急著把全文收斂成最終朗讀稿
- 這種素材包至少要把：
  - 已確認事實
  - 可直接講的賣點
  - 玩家對位
  - 風險 / 未定點
  - 可直接改寫句子
  整理出來
- 如果使用者要求的是 `研究包 / 深度研究 / 詳細資料 / 多平台研究`，輸出必須像資料倉庫，不可以只是大綱。每個章節、候選項或推薦項都要有完整研究卡：來源證據、取得或操作流程、強度與用途、玩家社群訊號、拍片素材、可用口播句、未定點與 Query Log。
- 使用者說 `資料越多越好 / 我自己整理 / 我來挑 / 不要收斂 / 再打多一點資訊` 時，優先擴充資料密度，不要只調整章節順序或提前寫成朗讀稿。
- 如果使用者沒有另外指定風格，預設讓開頭長這樣：
  - 固定自介
  - 一段 `這支影片要幫你解決什麼`
  - 再進章節
- `新手開局` 常見 promise 要落在 `少走彎路 / 前期更順 / 越早知道越省時間`
- `資源效率` 常見 promise 要先丟收益，再講怎麼穩定做到
- `買前必看` 常見 promise 要先回答 `值不值得買 / 適不適合你`
- 如果是 `新手攻略 / 新手開局 / 前期必做 / 攻略文案` 類型，而且使用者還沒要最終定稿，固定先照這個流程：
  1. 先找同遊戲或前作的高訊號攻略影片，不要只整理自己記得的系統
  2. 影片來源至少優先查 `YouTube / bilibili`，再依遊戲生態補 `巴哈姆特 / Reddit / Steam Community / Game8 / GameWith / 日文攻略站`
  3. `YouTube` 先用 `opencli youtube search` 或 `yt-dlp ytsearch` 找樣本，`bilibili` 先用 `opencli bilibili search`
  4. 高訊號影片必須盡量抓 `字幕 / 逐字稿`；沒有公開字幕時，能取得音訊就用本地轉錄，不要只看片名或搜尋摘要
  5. 網站、論壇、攻略頁必須讀正文，不能只看搜尋結果標題
  6. 先整理 `可挑章節池`，不要擅自替使用者定死 10 章
  7. 使用者挑完章節後，再幫忙順章節順序與整理 `每章一定要提到的重點`
  8. 使用者確認後，再做完整深度研究包
  9. 預設交付 `高資訊量攻略研究包 / 章節研究包`，不要直接收斂成最終朗讀稿
- 如果是 `買前必看 / 買之前 10 件事 / 入坑前必看` 類型，而且使用者還沒要最終定稿，固定先照這個流程：
  1. 先整理 `玩家社群真正最在意 / 最常問 / 最不懂` 的重點池
  2. 不要擅自決定 10 章，先讓使用者挑章節
  3. 使用者挑完後，再幫忙排順序
  4. 先整理 `每章一定要提到的重點` 給使用者審核
  5. 審核完再做 `深度研究`
  6. 深度研究必做 `繁中 / 日文 / 英文`
  7. 深度研究不能只看搜尋摘要或標題，必須實際打開網頁抓正文
  8. 高訊號影片必須盡量抓 `字幕 / 逐字稿`，不能只看片名
  9. 預設交付 `10 章研究包 / 章節研究包`，讓使用者自己再收成文稿
- 如果使用者只給 `遊戲名稱`，但語境明顯是 `買前必看`，預設就知道要做 `10 章節 + 重點池 + 之後深度研究`
- 如果使用者只給 `遊戲名稱`，但語境明顯是 `新手攻略 / 前期攻略 / 攻略文案`，預設就知道要先做 `攻略影片樣本搜尋 + 字幕 / 逐字稿抓取 + 可挑章節池`
- 如果是 `月份遊戲推薦 / 六月遊戲推薦 / 本月新作推薦 / 新作推薦 / 必玩遊戲清單` 類型，而且使用者還沒要最終定稿，固定先照這個流程：
  1. 先整理 `候選遊戲池`，確認平台、發售日、買斷制邊界與是否適合 `玫玫物語`
  2. 如果使用者已給定遊戲名單，不要擅自替換；如果沒有給名單，先給可挑候選
  3. 每一款遊戲都要做獨立 `研究卡`，不要只用商店介紹或新聞摘要帶過
  4. 官方來源只用來確認基本事實，不可以只靠官方宣傳決定推薦程度
  5. 每款都要找非官方或半非官方的相關主題 YouTube 影片，例如 `gameplay preview / demo impression / before you buy / review / hands-on / trailer breakdown / 試玩心得 / 值不值得期待`
  6. 每款都要補玩家社群來源，依遊戲生態查 `Steam 討論 / Reddit / 巴哈姆特 / B站留言或動態 / YouTube 高讚留言 / X 或 Threads`
  7. 玩家社群來源要用來判斷真實期待、疑慮、適合誰與不要講死的風險
  8. 高訊號 YouTube 影片必須盡量抓 `字幕 / 逐字稿`；沒有字幕但能取得音訊時，使用本地轉錄，不要只看片名或縮圖
  9. 網站、商店頁、新聞、論壇與攻略頁必須讀正文
  10. 每款研究卡至少整理 `已確認事實 / 核心玩法 / 最大賣點 / 社群期待與疑慮 / 適合誰 / 風險或未定點 / 可直接改寫口播句`
  11. 如果某款沒有可用 YouTube 字幕或逐字稿，要標記 `YT 字幕不足` 並降低影片證據權重
  12. 預設交付 `月份推薦研究素材包`，讓使用者刪改排序後，再收斂成正式朗讀稿
- 每月遊戲推薦固定分三段，不要跳步：
  1. `研究`：候選遊戲池 + 每款研究卡 + 可刪改文案素材。
  2. `撰寫`：使用者確認保留名單後，依發售日期排序，套用全域 Maymei 中文撰寫系統與使用者雲端親改稿語氣，產出正式朗讀稿。
  3. `提交`：正式稿完成後，同步更新 Google Docs 文案檔與 Google Sheets `遊戲清單`，並回讀確認。
- 如果使用者確認要進入 `月份遊戲推薦` 正式稿，固定使用這個 Google Drive 資料夾：`https://drive.google.com/drive/u/0/folders/1yFgnPkH9SLdhSk3fGiEMxySkpAwXEGDy`
- 正式稿階段固定更新兩份雲端文件：
  1. `文案`：資料夾中的月份推薦 Google Docs 文案檔。格式沿用每月範例：影片標題、`大家好~這裡是玫玫物語。`、每款 `## 遊戲名稱` 分段、自然片尾。每月遊戲固定依發售日期由早到晚排序，遊戲名稱盡量用台灣常見中文譯名。
  2. `宣傳片 / 實機 / 音樂表`：資料夾中的 `Longform Episode Workbook Template`，更新 `遊戲清單` 工作表，欄位固定為 `遊戲名稱 / 遊戲宣傳片 / 遊戲實機影片 / 遊戲音樂 / 發售日期 / 平台`。
- YouTube 候選搜尋規則：
  - 宣傳片：先搜 `<遊戲英文名> official trailer`，再補 `announcement trailer / release date trailer / launch trailer`，優先官方或可信遊戲頻道。
  - 實機影片：每款都要補，搜 `<遊戲英文名> gameplay`，再補 `demo gameplay / hands-on / no commentary / preview gameplay`，必須是真正實機畫面。
  - 音樂：搜 `<遊戲英文名> soundtrack instrumental`，再補 `ost no vocals / bgm instrumental / main theme / menu theme`。
  - 該款遊戲本身找不到可用音樂時，可以依序找 `系列前作 / 同開發商或發行商舊作 / 同類型遊戲` 的純音樂替代。
  - 使用替代音樂時，工作記錄要標明來源類型：`本作音樂 / 系列前作 / 同公司舊作 / 同類型替代`，不要把替代曲誤寫成該款遊戲官方音樂。
  - 音樂欄填入前必須實際播放聽過一次，確認沒有明顯人聲、歌詞、旁白、尖銳音效、過吵鼓點或不適合當背景的段落。
  - 音樂欄避開 `lyrics / vocal / cover / remix / music video`，不要硬填一般情境音樂或粉絲二創；如果無法實際聽過或聽完不乾淨，就留空。
- 寫入 Google Docs / Sheets 後，要重新讀取文案文件與 `遊戲清單` 範圍確認內容真的更新，再回報連結。

## 輸出格式

如果是正式稿 / 直接朗讀稿 / 最終定稿，輸出格式固定為：

```md
# Final Draft

# Voice Check

# Fact Check Notes
```

如果仍在結構稿或素材包階段，才使用：

```md
# Script Package

## Outline
## Full Draft
## Fact Check Notes
```
