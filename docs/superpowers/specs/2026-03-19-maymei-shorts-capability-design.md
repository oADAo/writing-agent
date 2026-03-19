# 玫玫物語 Shorts Capability Design

**Goal:** 在現有主題研究、標題封面、長影片腳本之外，新增 `Shorts 文本撰寫` 能力，專門服務 YouTube Shorts / 抖音型遊戲短影音。

## Product Scope

### In Scope
- 新增第 4 個工作模式：`Shorts 文本撰寫`
- 維持 `玫玫物語` 既有聲線，但節奏比長影片更狠、更快、更情緒
- 題材維持遊戲相關，但不限定劇情、冷知識、反轉、提醒、攻略等單一題型
- 固定輸出：
  - `Hook Title`
  - `Final Short Script`

### Out of Scope
- 不處理 Shorts 剪輯、字幕切軸、畫面腳本、上字幕時間軸
- 不直接生成影片描述、標題包、封面圖
- 不把 Shorts 併進長影片模式；維持獨立模式

## Design Principles

- Shorts 不是長影片縮短版，而是單一 punch 的短影音口播稿。
- 保留 `玫玫物語` 的帶路感與判斷感，但允許更高情緒張力。
- 每支短稿只打一個核心點，不塞多個主軸。
- 預設長度參考使用者提供的高流量樣本，落在約 `300 到 400` 字中文口播稿。

## Architecture

### 1. Root Controller Update
更新 `AGENTS.md`：
- 從 3 個模式改成 4 個模式
- 新增 Shorts 模式的必讀文件、輸出格式與禁止行為

### 2. Profile Rule Layer
新增 `docs/profiles/may-story/shorts_rules.md`：
- 定義 Shorts 聲線、節奏、結構、題型與長度
- 與 `voice_memory.md` 串接，保留品牌聲音一致性

### 3. Prompt Layer
新增 `prompts/shorts-writing.md`：
- 清楚規定 Shorts 任務目標
- 指定必讀文件
- 固定輸出 `Shorts Package`

## Shorts Writing Model

### Core Job
Shorts 的任務不是完整講解大題，而是快速打穿一個最值得講的點，例如：
- 一個悲劇故事
- 一個隱藏設定
- 一個很多人不知道的反轉
- 一個提醒
- 一個會讓觀眾想轉發的荒謬細節

### Voice
- 保留 `玫玫物語` 的成熟、親切、講人話
- 比長影片更直接、更快、更狠
- 可以更情緒化，但不能淪為空泛喊情緒

### Structure
Shorts 固定節奏：
1. 第一行直接鉤人
2. 第二段快速點核心事件
3. 中段一路推進資訊
4. 最後一句收在重擊、反轉、荒謬、哀傷或震撼點

### Output
```md
# Shorts Package

## Hook Title
## Final Short Script
```

## File Plan

### Create
- `docs/profiles/may-story/shorts_rules.md`
- `prompts/shorts-writing.md`
- `docs/superpowers/specs/2026-03-19-maymei-shorts-capability-design.md`
- `docs/superpowers/plans/2026-03-19-maymei-shorts-capability.md`

### Modify
- `AGENTS.md`
- `README.md`
- `docs/workflows/content-production.md`
- `examples/output-outline.md`

## Risks and Guardrails

- 如果直接沿用長影片規則，Shorts 很容易變成資訊過重的縮寫版。
- 如果只追求情緒，會失去 `玫玫物語` 原本的可信度與判斷感。
- 如果不限制只打一個 punch，短影音會失焦。

## Verification Plan

- 確認 `AGENTS.md` 已新增 Shorts 作為第 4 個模式
- 確認 README、workflow、examples 都反映新模式與新輸出格式
- 確認 Shorts 規則明寫與長影片不同的節奏與輸出
