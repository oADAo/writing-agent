# Cross-Project Video Pipeline

這份文件定義 `玫玫物語` 長影片生產線的跨專案規則。它不是要把所有 repo 合併，而是讓每個 repo 知道自己在同一支影片的哪一段，並用固定輸入 / 輸出交接。

## 核心原則

- 使用者不手動建立影片 manifest、工作資料夾或狀態表。
- Agent 必須從現有證據自動回填狀態：Google Docs、`workspace/deliverables/`、`voice-retake-cleaner/output/`、剪輯輸出、YouTube 頻道新片、YouTube Studio 匯出。
- 如果某一段由外部剪輯師完成，系統仍要透過 YouTube 新片偵測補回紀錄，不要求使用者手動登記。
- 不同專案不要互相讀內部暫存當成穩定介面；只認正式輸出和報告檔。
- 任何跨專案工作都要留下可追溯來源：檔案路徑、Google Docs 連結、YouTube URL、產出時間、缺口或人工交接點。

## 專案角色

| 專案 | 角色 | 穩定輸入 | 穩定輸出 |
| --- | --- | --- | --- |
| `X:\writing-agent` | Write engine / 內容上游 | 遊戲名、片型、研究需求、頻道資料 | 研究包、標題封面包、Google Docs 腳本、Claude Code 寫作提示 |
| `X:\voice-retake-cleaner` | 旁白重錄清理 | 最終腳本、編號 WAV 或原始錄音 | `final.wav`、`review.csv`、`transcript.json`、`segments.json`、人工複查報告 |
| Mac mini 字幕動畫流程 | 字幕與基本動畫 | `final.wav`、最終腳本 | 已對時字幕、字幕動畫層、過場動畫或合成層 |
| `X:\prebuy-video-agent` | 買前片剪輯自動化 | 最終腳本、`final.wav`、視覺需求、可用素材 | `edit_plan.json`、`sources.json/md`、`music_report.md`、review artifacts、可 render 成品 |
| `X:\game-footage-broll-assistant` | 遊戲畫面 / B-roll 專案 | 腳本語意單位、視覺需求、遊戲素材庫或錄製需求 | shot list、素材缺口、B-roll 選片、人工剪輯交接包 |
| `X:\money` | 業配與廠商情報 | 影片排程、遊戲類型、頻道合作方向 | 廠商候選、聯絡資訊、適合置入方式、風險與證據 |

## 自動狀態回填規則

跨專案中樞不能依賴使用者手動建立資料。未來需要紀錄影片狀態時，依序自動找：

1. `writing-agent` 的研究包、標題封面包、腳本 deliverables。
2. Google Docs 腳本連結與雲端內容。
3. `voice-retake-cleaner/output/` 裡最新同遊戲或同片型的 `final.wav` 與 review artifacts。
4. `prebuy-video-agent/outputs/` 或 `game-footage-broll-assistant` 的 edit plan、sources、review artifacts。
5. YouTube 頻道的新片清單。
6. YouTube Studio 匯出或公開 metadata。
7. 留言與觀眾回饋。

如果找不到某段，不要要求使用者補 manifest；要把該段標成 `unknown`，並記錄「需要哪種自動偵測器」。

## YouTube 新片偵測與回測

因為影片有時由外部剪輯師直接上傳，回測系統必須主動監測頻道，而不是等待手動登記。

新片偵測流程：

1. 定期讀取頻道最新影片。
2. 以標題、遊戲名、發布時間、描述文字、縮圖文字或片型關鍵字，嘗試匹配既有研究包 / 腳本 / 音訊輸出。
3. 找不到匹配時，自動建立 `unmatched upload` 紀錄，等待後續用標題或留言再歸類。
4. 抓取公開 metadata：標題、影片 URL、發布時間、觀看數、留言數、按讚數、描述、縮圖。
5. 若使用者提供 YouTube Studio 匯出，再補 CTR、曝光、觀眾維持率、流量來源。
6. 把留言主題整理成下一支影片的選題與腳本研究輸入。

回測輸出至少包含：

- 影片識別：YouTube URL、標題、發布時間。
- 匹配到的上游產物：研究包、標題封面包、腳本、音訊、剪輯包。
- 表現摘要：24 小時 / 7 天 / 28 天觀看、CTR、留言主題、相對頻道基準。
- 判斷：標題封面是否命中痛點、內容是否帶來下一支影片需求、這個遊戲是否值得繼續追。
- 下一步：可做的新題目、需要修正的標題封面公式、需要補強的研究方法。

## 跨專案任務啟動規則

只要使用者提到以下任一關鍵字，先讀本文件：

- 一條龍、整合、跨專案、不同電腦、回測、自動抓新片
- 錄音、重錄、旁白、final.wav、字幕、動畫
- 剪輯、B-roll、遊戲畫面、素材庫、Remotion、edit plan
- YouTube 上架、標題封面成效、留言、CTR、業配

如果任務只屬於單一專案，可以在讀完本文件後回到該專案規則；不要為了整合而把單一任務做重。

