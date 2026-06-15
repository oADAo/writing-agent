# maymei-script-finalizer golden sample selection

golden sample 的目的不是找最紅的影片來抄，而是建立可回歸的 `style forensics` 與 `formula card`。觀看數、按讚數、按讚率、留言量只用來排序候選，不能單獨決定樣本品質。

## 建置順序

1. `build_maymei_video_metrics.py` 抓公開影片資料，欄位包含 `video_id`、`title`、`url`、`view_count`、`like_count`、`like_rate`、`comment_count`、`upload_date`、`duration`。
2. `build_maymei_golden_samples.py` 把影片表現對回 `google-maymei-game-scripts.json`、`google-docs-corpus.json`、DOCX manifest，只保留「有影片表現 + 能對到實際文案」的稿。
3. `analyze_maymei_style_samples.py` 對每篇做 style forensics，不保留大段可抄原文。
4. `build_maymei_formula_cards.py` 依文案類型聚合成 formula card。
5. `retrieve_maymei_samples.py` 在 finalizer 階段抓 3 主樣本 + 2 輔助樣本。

## 平衡規則

- 高觀看只是候選資格，還要看能不能對到實際文案。
- 同一款遊戲或同一文案類型不能塞滿整個 golden set。
- `formula card` 至少要由 5 篇同類型樣本歸納；不足就標記資料不足，不硬湊公式。
- 相似度不足時不得硬配影片與文案。
- 主樣本優先同文案類型，輔助樣本可補同遊戲、同玩家痛點或相似資訊排序。

## style forensics 欄位

每篇樣本至少要拆：

- 開頭 promise 形式
- 第一人稱經驗感
- 情緒補刀與玩家對位
- 句長節奏
- 轉場方式
- 資訊排序
- 哪些句子像玫玫
- 哪些只是資料句
- 可學結構
- 不可抄句子

## formula card 用法

formula card 只回答「這類稿通常怎麼開、怎麼排序、怎麼轉場、怎麼把資料變成玩家感受」。它不提供新事實，也不能覆蓋研究包。若研究包和樣本語氣衝突，以研究包事實為準，以樣本文風為輔。
