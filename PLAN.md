# awesome-agent-skills（ctxfst 版）

給接手的 agent：照這份做，不要自行擴大範圍。做完只回報結果與沒做到的部分，不必回報檢查過程。不要 commit、不要 push。

## 這是什麼

一份 Agent Skill 清單，加上一個讓 AI 找 Skill 的 `find-skill`。做法是**看候選再反問**：

1. 用 embedding 搜出前 8 個候選 Skill。
2. AI 讀這 8 個候選的 description，判斷是不是已經有一個明顯合適。
3. 不明顯時，只問使用者一題（可以把幾個方向列成選項），把回答接在原需求後面再搜一次。
4. 推薦 Skill，附來源連結，提醒使用者安裝前自己做安全驗證。

這個方向來自驗證實驗（見 `experiment/RESULTS.md`）：模糊需求直接搜，第一名命中率 0.45；看候選後問一題，升到 0.70。只看原始 description 出題，和看工作線卡出題一樣好，所以**產品不使用工作線卡**。

這個 repo 只發佈清單與索引（名稱、description、來源連結），不複製上游 Skill 的檔案。

## 目標結構

```
README.md
PLAN.md
sources.yaml                   要收錄的上游 repo
catalog/skills.json            每個 Skill 一筆：id、name、description、來源、commit、url
index/                         vectors.npz、meta.json
find-skill/SKILL.md            搜尋與反問的規則（給 AI 讀）
find-skill/scripts/harvest.py  從 sources.yaml 收集 Skill，寫 catalog/skills.json
find-skill/scripts/find.py     build / search
tests/
experiment/                    驗證實驗與工作線卡，研究紀錄，不屬於產品
```

## 要做的事

### 1. 把工作線卡移出產品

- `cards/`（30 張官方工作線卡）移到 `experiment/official-cards/`。
- 把舊 `PLAN.md` 裡的實驗結果整理成 `experiment/RESULTS.md`：三輪實驗（檢索、反問含 raw_targeted 對照、作者那一側改寫 description）的數字、結論與限制。舊版內容可從 `experiment/report.json`、`experiment/ask/`、`experiment/desc/` 重建；數字以那些報告檔為準。
- 產品程式與 `find-skill/SKILL.md` 不再提到卡片、六槽、`Not for`、`group`。

### 2. `sources.yaml` 與 `harvest.py`

- `sources.yaml` 列出要收的 repo，每筆 `repo`、`commit`（固定版本）、`kind`（`official` 或 `community`）。第一版收：`anthropics/skills`、`openai/skills`、`microsoft/skills`，以及 `experiment/sources.json` 裡 `role: skill-source` 的社群 repo。不做安全篩選。
- `harvest.py`：把每個 repo 在指定 commit 抓到 repo 外的快取目錄（預設 `~/.cache/awesome-agent-skills/src`），找出所有 `SKILL.md`，讀 frontmatter 的 `name` 與 `description`，寫 `catalog/skills.json`。每筆欄位：`id`（`<owner>/<repo>/<skill 路徑>`）、`name`、`description`、`source`、`path`、`commit`、`url`（指向固定 commit）、`kind`、`has_scripts`（該 Skill 目錄下有沒有 `scripts/` 或可執行檔）。
- 沒有 `description` 的 Skill 跳過，並在執行結束時列出被跳過的數量。
- 同一個 `id` 只留一筆；`catalog/skills.json` 依 `id` 排序，讓 diff 好讀。

### 3. `find.py`

- `build`：讀 `catalog/skills.json`，嵌入 `name` 加 `description`，寫 `index/`。保留現有的嵌入設定、快取、模型不一致時報錯。預設 Voyage `voyage-3.5`；`SKILL_FINDER_EMBED_URL`／`SKILL_FINDER_EMBED_MODEL` 可換成任何 OpenAI 相容端點（含本機模型）。
- `search "<需求>" --top 8 --json`：回傳前 k 筆的 `id`、`name`、`description`、`url`、`commit`、`kind`、`has_scripts`、`score`。
- 移除卡片解析、`--description-only`、`eval` 子命令中依賴卡片的部分。`eval` 若保留，改讀 `catalog` 的 id。

### 4. 改寫 `find-skill/SKILL.md`

只寫實驗驗證過的流程，必須能獨立使用：

1. 用使用者的原話搜尋，取前 8 筆。
2. 讀這 8 筆的 description。只有在**一個候選明顯合適、其他明顯不合適**時直接推薦。
3. 否則只問一題。問題要能分開這些候選：可以把候選代表的幾種做法列成選項，或問它們差別所在的條件（平台、輸入檔案、框架、要交出什麼）。不在問題裡推銷某個 Skill，不問使用者已經講過的事。
4. 把回答接在原需求後面再搜一次，再判斷。第二次仍分不出來時，列出最接近的 2～3 個與差別，讓使用者自己選，不再追問。
5. 沒有合適的就直說沒有，不拿最不差的頂替。
6. 推薦時附 `url`（固定 commit）、`kind`、`has_scripts`，並說明：**收錄不代表安全，安裝前請自己讀過該 Skill 的檔案。**不自動安裝、不自動執行。

不要寫分數門檻，實驗沒有量出可靠的數字。

### 5. 測試

用模擬的嵌入端點測：`harvest` 能從一個假 repo 目錄產生正確的 `catalog`（含跳過沒有 description 的 Skill）；`build`／`search` 正常；模型不一致時報錯。

### 6. README

- 這是什麼、和其他 awesome 清單的差別（看候選再反問），附實驗的一行結論與 `experiment/RESULTS.md` 連結。
- 安裝 `find-skill`、設定嵌入 API key、改用本機模型並自建索引的方法。
- 清單：依來源列出 `name` 與一行 description，由 `catalog/skills.json` 產生。
- 安全聲明：收錄不代表安全，使用者找到 Skill 後，安裝前必須自己做安全驗證。

### 7. 重建與驗收

- 跑 `harvest.py`、`find.py build`，產生正式的 `catalog/` 與 `index/`。
- 用 `experiment/vague-queries.json` 裡任意 3 條模糊需求，實際照 `find-skill/SKILL.md` 走一遍（自己扮演使用者回答），確認流程走得通。這不是評測，不要報數字。
- 回報：收了幾個來源、幾個 Skill、跳過幾個、測試結果、README 是否完成。

## 之後再說

- 每週自動更新：比對上游 commit，有變動時重跑 `harvest` 與 `build`。
- 收錄申請：別人開 issue 提供 repo。
- 把那幾份 awesome 清單（VoltAgent、ComposioHQ、BehiSecc 等）裡的 repo 整批加進 `sources.yaml`。
- 分群、分數門檻。
- 工作線在作者那一側的用途（寫 description 的檢查清單）：目前實驗未證明有效，只能當寫作建議，不寫進產品。
