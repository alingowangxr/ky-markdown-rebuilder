# Output Formats

## Raw Markdown

Purpose: preserve extracted text from MarkItDown or another extractor.

Suggested filename:

```text
source.raw.md
```

Do not over-edit raw output. It is a reference layer.

## Page-Aligned Markdown

Purpose: reliable source of truth, one section per page/slide/screen.

Template:

```markdown
# Document Title

> Reconstruction note: built from raw extraction plus page screenshots.

## Page 01: Title

Source image: [page-01.png](pages/page-01.png)

Page purpose:

- ...

Layout map:

- Top:
- Center:
- Left:
- Right:
- Bottom:

Confirmed content by region:

- Region:

Visual notes:

- ...

## Page 02: Title

Source image: [page-02.png](pages/page-02.png)

...
```

Rules:

- Use exactly one `## Page NN` heading per page.
- Keep content from that page only.
- Include a screenshot link during validation unless the source has no visual reference; in final deliverable-only mode, replace local screenshot links with source-page notes if screenshots are removed.
- For non-trivial visual pages, include `Page purpose`, `Layout map`, `Confirmed content by region`, and `Visual notes`.
- Use tables for structured visual content.
- Preserve visible sequence over inferred conceptual grouping.
- Do not collapse a dense slide into a generic summary.
- For deep visual reconstruction, validate with `check_output.py --require-visual-sections` before delivery.

## Spreadsheet-Calibrated Markdown

Purpose: rebuild workbook content without forcing page/slide semantics.

Template:

```markdown
# Workbook Title

> Reconstruction note: built from sheet extraction plus workbook/screenshot inspection.

## Sheet: Dashboard

Sheet purpose:

- ...

Layout map:

- Top KPI cards:
- Left filters/slicers:
- Main chart:
- Bottom table:

Confirmed content by region:

- ...

Charts and formulas:

- ...

## Sheet: Raw Data

Table structure:

| Column | Meaning | Notes |
| --- | --- | --- |
```

Rules:

- Use `## Sheet: Name` for workbook structure.
- For dashboard-like sheets, use visual sections just like a slide.
- For data sheets, prioritize table fields, units, formulas, filters, and data quality notes.
- For financial or operational models, preserve assumptions, calculation flow, dependencies, and outputs.
- Do not require `## Page NN` headings for spreadsheets unless the workbook is exported as page-like screenshots.

## Image/HTML-Calibrated Markdown

Purpose: rebuild a single visual source, long screenshot, or web page into Markdown.

Rules:

- Use `## Region NN` for images or long screenshots when page numbers do not exist.
- Use `## Screen NN` or `## Section: Name` for HTML/web pages.
- Preserve reading order, visual hierarchy, and important component relationships.
- Use visual sections for dashboards, UI screenshots, diagrams, forms, pricing tables, and comparison layouts.

## Outline Markdown

Purpose: produce the required second deliverable when the user asks for an outline, 大纲版, or two final Markdown files.

Suggested filename:

```text
source.outline.md
```

Rules:

- Generate from the calibrated Markdown only.
- Treat this as mandatory when requested; do not deliver only the calibrated file.
- Keep page/sheet/section anchors.
- Preserve the document's argument flow and major evidence.
- Do not duplicate all body details.
- Include chart/table/diagram roles when they are central to the source.
- For decks/proposals, group by narrative function rather than merely listing page titles.

Template:

```markdown
# Document Title - Outline

Source calibrated file: `source.calibrated.md`
Source document: `source.ext`

## 1. Executive Thread

- ...

## 2. Structure Map

| Section | Source pages/sheets | Role |
| --- | --- | --- |

## 3. Detailed Outline

### 3.1 Section

- Key point
- Supporting source pages

## 4. Key Evidence

| Evidence | Source | Why it matters |
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

Purpose: guide visual inspection and token allocation.

Template:

```markdown
| Page | Screenshot | Title | Text chars | Priority | Reason |
| --- | --- | --- | ---: | --- | --- |
| 01 | pages/page-01.png | Title | 120 | low | enough text |
| 02 | pages/page-02.png | Diagram title | 38 | high | sparse text, likely diagram |
```
