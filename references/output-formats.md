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
# 文档标题

> 重建说明：模式 deep-visual；来源 `source.pdf`；共 15 页；原图逐页查看 15/15 页。

## Page 01: 页标题（跟随原文语言）

源图：[page-01.png](pages/page-01.png)

### 页面目的

- ...

### 布局地图

- ...

### 按区域确认内容

#### 区域 1：左侧 2x2 卡片区

...

### 视觉备注

- ...

## Page 02: 页标题

源图：[page-02.png](pages/page-02.png)

...
```

Rules:

- Exactly one `## Page NN: Title` heading per page; half-width colon; zero-padded numbers (min 2 digits). Image inputs use `## Region NN:`, HTML uses `## Screen NN:`, with the same inner template.
- The four H3 labels are the only accepted spellings: `### 页面目的` / `### 布局地图` / `### 按区域确认内容` / `### 视觉备注`. No English, no bare-text-with-colon, no other heading level.
- Exactly one source line per section, directly under the `##` heading:
  - validation phase: `源图：[page-NN.png](pages/page-NN.png)`
  - final deliverable without screenshots: `源页：第 N 页` (PDF/scan) or `源页：Slide NN` (PPT) or `源图：<原始输入文件名>` (single image)
- The reconstruction note reports the TRUE original-resolution inspection count (`原图逐页查看 N/M 页`); thumbnails do not count.
- Keep content from that page only; preserve visible sequence over inferred grouping.
- Use tables for structured visual content; do not collapse a dense slide into a generic summary; do not wrap page bodies in code fences.
- Title/transition pages keep all four sections, each may be a single bullet.
- Validate with `python3 scripts/check_output.py --md file.md --pages-dir pages --expected-pages N --require-visual-sections` before delivery.

## Spreadsheet-Calibrated Markdown

Purpose: rebuild workbook content without forcing page/slide semantics.

Template:

```markdown
# 工作簿标题

> 重建说明：模式 page-aligned；来源 `book.xlsx`；共 4 表；原图逐页查看 4/4 页。

## Sheet: Dashboard

源页：Sheet "Dashboard"

### 页面目的

- ...

### 布局地图

- 顶部 KPI 卡片：
- 左侧筛选器：
- 主图表：
- 底部明细表：

### 按区域确认内容

...（含图表与公式；数据表优先字段、单位、公式、筛选与数据质量说明）

### 视觉备注

- ...

## Sheet: Raw Data

...
```

Rules:

- Use `## Sheet: Name` for workbook structure; the four H3 labels stay identical to the page route.
- For dashboard-like sheets, treat regions exactly like a slide.
- For data sheets, 按区域确认内容 prioritizes table fields, units, formulas, filters, and data quality notes.
- For financial or operational models, preserve assumptions, calculation flow, dependencies, and outputs.

## Transcribed Markdown (`transcribe` mode, scanned documents)

Default deliverable for scanned books, forms, and budget/reference documents where the user wants the content 1:1. No four-section template — the page body IS the transcription.

Template:

```markdown
# 文档标题

> 重建说明：模式 transcribe；来源 `scanned-book.pdf`；共 52 页；原图逐页查看 52/52 页。
> 补充：内容由视觉模型分批直读原图转写（10 页/批并行）。

## Page 01: 第 01 页

源图：[page-01.png](pages/page-01.png)

<该页全部文字 1:1 转写，跟随原文语言>

| รายการ | หน่วยนับ | จำนวน |
| --- | --- | --- |
| ... | คน | 12,500 |

## Page 02: <页标题>

...
```

Rules:

- Page titles come from the visually confirmed heading; a page without a readable heading uses `## Page NN: 第 NN 页`. Never use raw OCR first-line garbage as a title.
- Transcription must come from original-resolution page images (vision-model direct reading preferred; tesseract fallback must be reconciled against the images).
- Tables become Markdown tables preserving empty cells and dash-only (`-`) placeholders — never full-page code fences. After concatenating batches, run `python3 scripts/fix_tables.py <file>`.
- Merged cells follow the LOCKED rules in `references/visual-transcription-rules.md`: 跨列合并=每个跨到的列重复内容；跨行合并=只写首行、后续行留空；多行表头=第一行做 Markdown 表头、其余表头行按序做正文首行。Never pick a different convention per run.
- Unreliable readings (amounts, units, small labels) are marked `[?]` inline.
- Degraded pages (quota fallback, reference-file transcription, crashed batch) are listed by page number in the reconstruction note, and the `原图逐页查看 N/M` count excludes them.
- Validate with `check_output.py --expected-pages N` WITHOUT `--require-visual-sections`.

## Translated Deliverable

Only when the user requests a translation. Filename: `source.calibrated.<lang>.md` (e.g. `.zh.md`).

- Generated from the calibrated file AND spot-checked against original page images.
- Structural labels stay Chinese; `## Page NN:` keeps "Page" and the half-width colon; only body content and page titles are translated.
- The reconstruction note states it is a translation and names the source calibrated file.

## Outline Markdown

Purpose: the required second deliverable when the user asks for an outline, 大纲版, or two final Markdown files.

Filename: `source.outline.md`

Rules:

- Generate from the calibrated Markdown only; mandatory when requested — do not deliver only the calibrated file.
- Keep page/sheet/section anchors; preserve argument flow and major evidence; do not duplicate all body details.
- For decks/proposals, group by narrative function rather than page titles.

Locked skeleton (headers always these Chinese strings):

```markdown
# 文档标题 - 大纲

> 来源：`source.calibrated.md`（校准版）；原始文档 `source.ext`。

## 1. 核心主线

- ...

## 2. 结构地图

| 章节 | 来源页/表 | 作用 |
| --- | --- | --- |

## 3. 详细大纲

### 3.1 章节

- 要点
- 支撑页码

## 4. 关键证据

| 证据 | 来源 | 为什么重要 |
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
