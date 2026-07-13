# Output Formats

All deliverables follow the LOCKED Output Contract in SKILL.md. Structural labels are always the exact Chinese strings shown here; body content and page titles follow the source document language (Chinese, English, Thai, or anything else). `check_output.py` enforces these templates literally.

## Raw Markdown

Purpose: preserve extracted text from MarkItDown or another extractor.

Suggested filename:

```text
source.raw.md
```

Do not over-edit raw output. It is a reference layer and lives in `.ky-md-work/`.

## Calibrated Markdown (Page/Region/Screen routes)

Purpose: reliable source of truth, one section per page/slide/screen.

Template (validation phase, screenshots retained):

```markdown
# 文件標題

> 重建說明：模式 deep-visual；來源 `source.pdf`；共 15 頁；原圖逐頁查看 15/15 頁。

## Page 01: 頁標題（跟隨原文語言）

源圖：[page-01.png](pages/page-01.png)

### 頁面目的

- ...

### 佈局地圖

- ...

### 按區域確認內容

#### 區域 1：左側 2x2 卡片區

...

### 視覺備註

- ...

## Page 02: 頁標題

源圖：[page-02.png](pages/page-02.png)

...
```

Rules:

- Exactly one `## Page NN: Title` heading per page; half-width colon; zero-padded numbers (min 2 digits). Image inputs use `## Region NN:`, HTML uses `## Screen NN:`, with the same inner template.
- The four H3 labels are the only accepted spellings: `### 頁面目的` / `### 佈局地圖` / `### 按區域確認內容` / `### 視覺備註`. No English, no bare-text-with-colon, no other heading level.
- Exactly one source line per section, directly under the `##` heading:
  - validation phase: `源圖：[page-NN.png](pages/page-NN.png)`
  - final deliverable without screenshots: `源頁：第 N 頁` (PDF/scan) or `源頁：Slide NN` (PPT) or `源圖：<原始輸入文件名>` (single image)
- The reconstruction note reports the TRUE original-resolution inspection count (`原圖逐頁查看 N/M 頁`); thumbnails do not count.
- Keep content from that page only; preserve visible sequence over inferred grouping.
- Use tables for structured visual content; do not collapse a dense slide into a generic summary; do not wrap page bodies in code fences.
- Title/transition pages keep all four sections, each may be a single bullet.
- Validate with `python3 scripts/check_output.py --md file.md --pages-dir pages --expected-pages N --require-visual-sections` before delivery.

## Spreadsheet-Calibrated Markdown

Purpose: rebuild workbook content without forcing page/slide semantics.

Template:

```markdown
# 工作簿標題

> 重建說明：模式 page-aligned；來源 `book.xlsx`；共 4 表；原圖逐頁查看 4/4 頁。

## Sheet: Dashboard

源頁：Sheet "Dashboard"

### 頁面目的

- ...

### 佈局地圖

- 頂部 KPI 卡片：
- 左側篩選器：
- 主圖表：
- 底部明細表：

### 按區域確認內容

...（含圖表與公式；數據表優先字段、單位、公式、篩選與數據質量說明）

### 視覺備註

- ...

## Sheet: Raw Data

...
```

Rules:

- Use `## Sheet: Name` for workbook structure; the four H3 labels stay identical to the page route.
- For dashboard-like sheets, treat regions exactly like a slide.
- For data sheets, 按區域確認內容 prioritizes table fields, units, formulas, filters, and data quality notes.
- For financial or operational models, preserve assumptions, calculation flow, dependencies, and outputs.

## Transcribed Markdown (`transcribe` mode, scanned documents)

Default deliverable for scanned books, forms, and budget/reference documents where the user wants the content 1:1. No four-section template — the page body IS the transcription.

Template:

```markdown
# 文件標題

> 重建說明：模式 transcribe；來源 `scanned-book.pdf`；共 52 頁；原圖逐頁查看 52/52 頁。
> 補充：內容由視覺模型分批直讀原圖轉寫（10 頁/批並行）。

## Page 01: 第 01 頁

源圖：[page-01.png](pages/page-01.png)

<該頁全部文字 1:1 轉寫，跟隨原文語言>

| รายการ | หน่วยนับ | จำนวน |
| --- | --- | --- |
| ... | คน | 12,500 |

## Page 02: <頁標題>

...
```

Rules:

- Page titles come from the visually confirmed heading; a page without a readable heading uses `## Page NN: 第 NN 頁`. Never use raw OCR first-line garbage as a title.
- Transcription must come from original-resolution page images (vision-model direct reading preferred; tesseract fallback must be reconciled against the images).
- Tables become Markdown tables preserving empty cells and dash-only (`-`) placeholders — never full-page code fences. After concatenating batches, run `python3 scripts/fix_tables.py <file>`.
- Merged cells follow the LOCKED rules in `references/visual-transcription-rules.md`: 跨列合併=每個跨到的列重複內容；跨行合併=只寫首行、後續行留空；多行表頭=第一行做 Markdown 表頭、其餘表頭行按序做正文首行。Never pick a different convention per run.
- Unreliable readings (amounts, units, small labels) are marked `[?]` inline.
- Degraded pages (quota fallback, reference-file transcription, crashed batch) are listed by page number in the reconstruction note, and the `原圖逐頁查看 N/M` count excludes them.
- Validate with `check_output.py --expected-pages N` WITHOUT `--require-visual-sections`.

## Translated Deliverable

Only when the user requests a translation. Filename: `source.calibrated.<lang>.md` (e.g. `.zh.md`).

- Generated from the calibrated file AND spot-checked against original page images.
- Structural labels stay Chinese; `## Page NN:` keeps "Page" and the half-width colon; only body content and page titles are translated.
- The reconstruction note states it is a translation and names the source calibrated file.

## Outline Markdown

Purpose: the required second deliverable when the user asks for an outline, 大綱版, or two final Markdown files.

Filename: `source.outline.md`

Rules:

- Generate from the calibrated Markdown only; mandatory when requested — do not deliver only the calibrated file.
- Keep page/sheet/section anchors; preserve argument flow and major evidence; do not duplicate all body details.
- For decks/proposals, group by narrative function rather than page titles.

Locked skeleton (headers always these Chinese strings):

```markdown
# 文件標題 - 大綱

> 來源：`source.calibrated.md`（校準版）；原始文件 `source.ext`。

## 1. 核心主線

- ...

## 2. 結構地圖

| 章節 | 來源頁/表 | 作用 |
| --- | --- | --- |

## 3. 詳細大綱

### 3.1 章節

- 要點
- 支撐頁碼

## 4. 關鍵證據

| 證據 | 來源 | 為什麼重要 |
| --- | --- | --- |
```

## Reading Markdown

Purpose: user-friendly report or article generated from the page-aligned source.

Rules:

- Start from the page-aligned version, not raw extraction.
- Group pages into reader-friendly sections only after page coverage is verified.
- Optionally keep a page-reference appendix.
- Do not introduce new facts absent from the page-aligned source.

## Manifest

Purpose: guide visual inspection and token allocation. Lives in `.ky-md-work/`.

Template:

```markdown
| Page | Screenshot | Title | Text chars | Priority | Reason |
| --- | --- | --- | ---: | --- | --- |
| 01 | pages/page-01.png | Title | 120 | low | enough text |
| 02 | pages/page-02.png | Diagram title | 38 | high | sparse text, likely diagram |
```
