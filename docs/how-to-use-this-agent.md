# How To Use This Agent

這個 repo 的主入口是自然語言，不是 CLI。

你只要直接說你要做什麼，我會依 `AGENTS.md` 的規則判斷模式、查資料、產出成品，並把工作記憶寫進 repo。

## 可用功能

- `熱門主題搜尋`
- `高流量標題與封面方向`
- `長影片腳本撰寫`
- `Shorts 文本撰寫`

## 自然語言下法

- `幫我找這款遊戲最近能做的熱門題目`
- `這個題目幫我想高點擊標題和封面文案`
- `這個題目直接幫我出長影片腳本`
- `把這個題目寫成一篇 Shorts 口播稿`

如果一句話明顯屬於其中一步，我會直接執行。
如果一句話同時混了兩步以上，或缺少關鍵前提，我才會補問。

## 成品會寫去哪裡

正式成品寫到：

- `workspace/deliverables/topic/`
- `workspace/deliverables/title/`
- `workspace/deliverables/script/`
- `workspace/deliverables/shorts/`

## 工作記憶會寫去哪裡

單次任務的查詢證據、來源與決策理由寫到：

- `workspace/memory/runs/`

可長期回用的遊戲記憶寫到：

- `workspace/memory/games/`

## 目前內部工具

repo 內部會逐步補齊：

- deliverable 模板
- memory 模板
- 文件一致性檢查
- 成品結構檢查
- memory 完整性檢查
