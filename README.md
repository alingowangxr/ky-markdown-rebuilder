# KY Markdown Rebuilder

把視覺文件重建成**可核對、按頁對齊、結構可靠的 Markdown**。

它不是普通的“文件轉 Markdown”工具，而是一套面向 Codex、Claude Code 和 Antigravity 的文件重建 Skill：先提取文本，再渲染原始頁面，最後結合頁面視覺結構校準內容，並通過腳本檢核頁數、格式、圖片連結和輸出契約。

適合處理普通文本提取容易失真的資料，例如 PDF、PPT/PPTX、掃描件、長截圖、報告、白皮書、課程資料、方案 deck，以及包含表格、流程圖、架構圖、時間線、卡片或多欄佈局的文件。

## 為什麼用它

普通轉換工具通常只保留文本，容易出現閱讀順序錯亂、跨頁串內容、表格散架、圖示關係丟失等問題。

KY Markdown Rebuilder 使用“文本提取 + 頁面渲染 + 原圖核對 + 機械驗收”的方式重建文件：

- 每頁、每張 Slide 或每個視覺區域單獨成節，避免相鄰頁面內容混在一起。
- 保留標題、分欄、卡片、表格、流程、矩陣和圖示關係。
- 對視覺密集頁面使用原始解析度檢查，而不是從縮略圖猜內容。
- 掃描件優先使用視覺模型逐頁轉寫，無法使用時才回退到 Tesseract OCR。
- 無法可靠辨認的金額、單位或小字會顯式標記，不靜默猜測。
- 輸出前運行檢核器；格式漂移、缺頁、死連結或表格錯誤會阻止交付。
- 如實記錄真正打開原圖核對的頁數，不把縮略圖瀏覽算作逐頁檢查。

## 支持的輸入

- PDF 報告、白皮書、手冊、課程資料
- PPT / PPTX / slide deck / 方案文件
- 掃描 PDF、拍照書頁、圖片型文件
- Word 風格報告和圖文混排文件
- HTML 頁面、本地網頁導出
- 長截圖和單張複雜圖片
- 帶圖表、KPI 卡片或儀表盤的表格文件

純文本或結構簡單的 Markdown 不需要使用本 Skill，直接轉換更快。

## 輸出模式

| 模式 | 適用場景 | 結果 |
| --- | --- | --- |
| `fast` | 以線性文本為主的文件 | 原始轉換 + 輕量清理 |
| `page-aligned` | PDF、報告、普通 deck、圖文混排資料 | 每頁一個 Markdown 區塊 |
| `deep-visual` | 高風險、視覺密集、銷售或解決方案 deck | 逐頁原圖檢核 + 視覺結構重建 |
| `transcribe` | 掃描書籍、表格、預算或檔案資料 | 按頁 1:1 轉寫正文和表格，不添加版式評論 |

如果需要更適合連續閱讀的文章版，可以在 `page-aligned` 校準版完成後繼續生成 `reading` 版本；不會直接從未經校準的原始提取結果生成。

## 默認產物

默認生成：

```text
source.calibrated.md
```

如果用戶要求“大綱”“outline”或“兩個文件”，還會生成：

```text
source.outline.md
```

如需翻譯版，會單獨生成：

```text
source.calibrated.zh.md
```

翻譯版從校準版生成，並回到原始頁面抽查；不會把翻譯混進原文校準文件。

中間截圖、原始提取、頁清單和分批草稿統一保存在：

```text
.ky-md-work/<source-name>/
```

這些證據文件會保留到用戶確認結果無誤後再刪除。

## 安裝

### Codex

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/KyrieCheungYep/ky-markdown-rebuilder.git \
  ~/.codex/skills/ky-markdown-rebuilder
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/KyrieCheungYep/ky-markdown-rebuilder.git \
  ~/.claude/skills/ky-markdown-rebuilder
```

### Antigravity

把倉庫複製到當前 workspace，在任務中要求 Agent 按倉庫內的 `SKILL.md` 執行。

### 更新已有安裝

Codex：

```bash
git -C ~/.codex/skills/ky-markdown-rebuilder pull --ff-only
```

Claude Code：

```bash
git -C ~/.claude/skills/ky-markdown-rebuilder pull --ff-only
```

## 環境預檢

安裝後建議先運行：

```bash
python3 ~/.codex/skills/ky-markdown-rebuilder/scripts/preflight.py
```

預檢會報告當前環境是否具備：

- `pdftoppm` / `pdfinfo`：PDF 頁渲染、頁數和文字層檢核
- `soffice`：PPT/PPTX 轉 PDF
- `markitdown`：原始文本提取
- `tesseract`：掃描件 OCR 後備方案及已安裝語言包
- `PIL` / `pypdf`：圖片處理和 PDF 文字層檢核

並非所有輸入都需要全部工具。Skill 會根據文件類型和當前環境選擇可用路線，不會在任務中途靜默安裝依賴。

## 使用方式

在 Codex 或 Claude Code 中直接點名 Skill：

```text
使用 $ky-markdown-rebuilder，把 proposal.pdf 重建成按頁對齊的 Markdown。
```

視覺密集的方案或銷售 deck：

```text
使用 $ky-markdown-rebuilder，以 deep-visual 模式重建這個 PPTX，
並額外生成一份 outline。
```

掃描件 1:1 轉寫：

```text
使用 $ky-markdown-rebuilder，把這份掃描 PDF 按原文逐頁轉寫成 Markdown。
表格保留為 Markdown 表格，不翻譯，不要版式分析。
```

也可以直接用自然語言觸發：

```text
把這個視覺結構複雜的 PDF 重建成可核對的 Markdown，保留每頁結構和表格。
```

## 工作流程

```text
環境預檢
  → 提取原始文本
  → 渲染逐頁原圖
  → 建立頁清單並判斷檢核優先級
  → 按原圖重建 Markdown
  → 運行輸出檢核器
  → 交付校準版 / 大綱版
```

對於無文字層的掃描件，會切換到 `transcribe` 路線：優先從原始解析度頁面直接轉寫；只有在視覺模型不可用時才使用 Tesseract。

## 輸出質量契約

`scripts/check_output.py` 會在交付前檢核關鍵約束，包括：

- 頁碼是否連續，頁數是否完整
- 每頁是否有且只有一個來源行
- 頁面標題、固定結構標籤和標點是否符合約定
- 截圖連結是否真實可用，連結位置是否與實際頁面圖片一致
- 是否存在整頁代碼圍欄、HTML 空白實體或無法渲染的表格
- 是否重複使用空泛的版式套話或罐頭式視覺備註
- `deep-visual` / `page-aligned` 是否包含完整的頁面結構資訊

檢核失敗時不應交付結果；先修正，再重新運行檢核。

## 內置腳本

| 腳本 | 用途 |
| --- | --- |
| `scripts/preflight.py` | 檢核文件處理工具和語言包 |
| `scripts/render_pages.py` | 把 PDF、PPT、PPTX 渲染成逐頁圖片 |
| `scripts/split_markdown_pages.py` | 按分頁符或 Slide 標記拆分原始 Markdown |
| `scripts/make_manifest.py` | 生成頁碼、標題、文本長度和視覺檢查優先級清單 |
| `scripts/check_output.py` | 檢核頁數、格式、連結和輸出契約 |
| `scripts/fix_tables.py` | 修復掃描件轉寫後列數不齊的 Markdown 表格 |

所有腳本統一使用 `python3` 調用。

## 目錄結構

```text
ky-markdown-rebuilder/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── output-formats.md
│   ├── token-control.md
│   └── visual-transcription-rules.md
└── scripts/
    ├── check_output.py
    ├── fix_tables.py
    ├── make_manifest.py
    ├── preflight.py
    ├── render_pages.py
    └── split_markdown_pages.py
```

## English

KY Markdown Rebuilder is a document-reconstruction skill for Codex, Claude Code, and Antigravity. It turns visually complex PDFs, slide decks, scanned documents, long screenshots, and reports into reliable, page-aligned Markdown.

Instead of trusting plain text extraction alone, it combines text extraction, page rendering, original-resolution visual inspection, structured reconstruction, and automated output validation. It also provides a dedicated `transcribe` route for image-only or scanned documents.

Typical usage:

```text
Use $ky-markdown-rebuilder to rebuild this PDF as page-aligned Markdown.
Create an outline as a second deliverable.
```

Typical output:

```text
source.calibrated.md
source.outline.md
```

See `SKILL.md` for the complete workflow and output contract.
