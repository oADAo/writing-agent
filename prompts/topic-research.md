# Topic Research Prompt

你現在只做一件事：替 `玫玫物語` 找出最近值得做的長影片題目。

不要直接寫稿，也不要自動跳到標題或腳本。

## 先讀文件

- `docs/profiles/may-story/channel_scope.md`
- `docs/profiles/may-story/topic_research_rules.md`

## 任務目標

- 找出最近值得切入的熱門題目
- 固定比對中文、日文、英文三個語圈的高流量內容
- 每次都要查 `YouTube` 以外的高流量社群平台、論壇、攻略站或其他玩家真的會找攻略的站外來源
- 先把候選影片整理成 `主題簇`，再判斷哪個題型真的在跑
- 也要把站外內容整理成 `討論簇 / 問題簇 / 攻略需求簇`
- 說清楚觀眾為什麼會點、為什麼現在做有機會
- 判斷哪些外國爆款角度最適合翻成中文圈可吃的題目

## 工作原則

- 題材必須符合 `玫玫物語` 的頻道邊界
- 涉及最新資訊、趨勢、更新、排行榜、競品或演算法變化時，要重新查證
- 搜尋時要用各語圈自己的原生關鍵字，不要只拿單一語言硬搜
- 站外來源不可以只限於固定平台名單，要依遊戲生態找真正有高流量、高互動的地方
- 原則上至少要查 `2 種站外來源類型`；如果站外生態太薄，要直接寫明資料不足
- 每次研究都要留下查詢證據：查了哪些平台 / 站點、用了哪些關鍵字、找到哪些高流量貼文 / 討論串 / 攻略頁
- 只有 `跨語圈反覆出現` 或 `同語圈多位高流量創作者都在做` 的題型，才能當主結論
- 如果要推成 `Top 1 Recommendation`，還要通過 `YouTube + 站外來源` 的交叉驗證，不能只靠單支影片或單篇爆文
- 低觀看、小頻道、單支特例片只能當輔證，不能直接當熱門主題
- 如果站外高流量樣本不足，要直接寫進 `Risks / Unknowns`
- 不要只列題目，要補受眾需求、流量理由與頻道適配度
- 不要只看中文圈
- 不要把很多相近題目偽裝成不同方向
- 完成後除了正式 `Topic Brief`，也要把查詢證據整理進 `workspace/memory/runs/...`
- 如果這次研究對某款遊戲形成可重用結論，還要更新 `workspace/memory/games/...`

## 輸出格式

```md
# Topic Brief

## Inputs
## Query Log
 - 查詢平台 / 站點
 - 使用關鍵字
 - 找到的高訊號內容
 - 是否納入主結論
## Market Signals
## Community / Forum Signals
## Cross-Language Competitor Hits
## Cross-Source Validation
## Chinese Audience Fit
## 5 Topic Options
### Option 1
 - 題目
 - 切角
 - YouTube 證據
 - 站外證據
 - 為什麼有流量
 - 為什麼適合這個頻道
## Top 1 Recommendation
## Why Now
## Risks / Unknowns
```
