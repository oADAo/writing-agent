# How To Use This Agent

這個 repo 現在做 `玫玫物語` 的研究工作，正式支援長片研究與 Shorts 研究。

## 可以怎麼下

長片研究：

- `幫我找這款遊戲最近能做的長片攻略主題`
- `這款遊戲買前必看可以講哪些章節`
- `這款遊戲新手攻略先幫我做候選章節池`
- `這幾章我已經鎖定，幫我查每章的資料和來源`
- `幫我做深度研究報告，原文、字幕、來源都要保留`
- `資料越多越好，我自己整理，不要收斂成正式稿`

Shorts 研究：

- `幫我找這款遊戲能做的 Shorts 題型`
- `幫我做 Shorts 主題搜尋`
- `這個 Shorts 題目幫我查資料和參考短片`
- `幫我做 Shorts 研究包，hook、punch、畫面節奏都整理`
- `我會做 Shorts 影片，先幫我整理可拍素材和來源`

## 預設會交付什麼

長片預設交付 `Longform Research Report`，不是正式朗讀稿。

Shorts 預設交付 `Shorts Topic Pack` 或 `Shorts Research Pack`，不是完整 Shorts 文稿。

## 長片報告會包含

- 研究範圍。
- 主題判斷。
- Query Log。
- Source Capture Status。
- 市場與玩家需求訊號。
- 章節規劃。
- 每章研究卡。
- 來源證據表。
- 原文、正文、字幕、逐字稿索引。
- 風險與未知。
- 需要實機驗證的點。
- 下一步研究建議。

## Shorts 研究包會包含

- 研究範圍。
- Query Log。
- Source Capture Status。
- 平台訊號。
- 主題簇。
- 參考 Shorts 證據。
- hook / punch 分析。
- 留言與社群訊號。
- 台灣觀眾適配。
- 製作研究筆記。
- 來源證據表。
- 原文、字幕、留言索引。
- 風險與未知。
- 下一步研究建議。

## 成品位置

- 長片研究報告：`workspace/deliverables/longform-research/`
- Shorts 主題包：`workspace/deliverables/shorts-topic/`
- Shorts 研究包：`workspace/deliverables/shorts-research/`
- 單次任務證據：`workspace/memory/runs/<timestamp>-<mode>-<slug>/`
- 原文與正文：`<run-dir>/source-originals/`
- 字幕與逐字稿：`<run-dir>/transcripts/`
- 長期遊戲記憶：`workspace/memory/games/<slug>/`

## 鎖定內容怎麼說

如果你已經決定章節或 Shorts 題型，直接說：

```text
這幾章鎖定，不要改順序：
1. ...
2. ...
3. ...
```

或：

```text
這支 Shorts 題型鎖定，就查這個方向，不要換題。
```

agent 只能補研究、標註風險、查證來源，不會擅自刪掉、合併或重排。

如果你還沒決定，可以說：

```text
先給我候選章節池，我自己挑，不要幫我定案。
```

或：

```text
先給我 Shorts 題型候選，我自己挑。
```

agent 只會提供候選、取捨和風險。

## 不再預設做的事

- Shorts 完整文稿。
- 長片正式稿。
- 標題封面。
- Google Docs 正式稿。
- maymei-script-finalizer 文風打分。

如果你真的要其中一項，需要明確說這次要暫時離開研究範圍。
