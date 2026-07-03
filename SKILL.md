---
name: ky-markdown-rebuilder
description: Rebuild visual documents into reliable Markdown by combining text extraction with page or screenshot alignment. Use when converting or cleaning up PDFs, slide decks, PPT/PPTX files, HTML pages, long screenshots, Word-like reports, whitepapers, course materials, business decks, or visually dense documents where plain text extraction may jumble layout, charts, timelines, diagrams, tables, screenshots, or logos.
metadata:
  short-description: Rebuild visual documents into page-aligned Markdown
---

# KY Markdown Rebuilder

Use this skill when a document should become Markdown but the visual layout matters. The goal is not just conversion; it is content reconstruction with a reliable visual source of truth.

Core principle:

> Extract text first, render visual pages second, then rebuild Markdown from a page-aligned source of truth.

Default deliverable principle:

> Use intermediate files as working evidence, but deliver only the final calibrated Markdown and, when requested, an outline Markdown.

## Host Compatibility

This package is portable across Codex and Claude Code:

- Codex install path: `~/.codex/skills/ky-markdown-rebuilder/`
- Claude Code install path: `~/.claude/skills/ky-markdown-rebuilder/`
- Shared assets: `scripts/` and `references/`
- Codex-only UI metadata: `agents/openai.yaml`

Both hosts should use the same workflow below. If a host cannot access one helper script or renderer, use its native browser/document tools for that step and keep the page-aligned output contract unchanged.

## When To Use

Use for:

- PDF reports, PPT-style PDFs, whitepapers, course packs, proposal decks.
- PPT/PPTX decks, slide exports, Keynote-like slide files.
- HTML pages or local web pages that need Markdown reconstruction.
- Long screenshots or image-heavy documents.
- Word/document files that contain diagrams, tables, screenshots, or complex layout.

Do not use for simple text-only files where normal conversion is enough.

## Output Modes

Choose the smallest mode that satisfies the user.

| Mode | Use when | Output |
| --- | --- | --- |
| `fast` | The document is mostly linear text | raw conversion plus light cleanup |
| `page-aligned` | Default for decks, PDFs, reports, or mixed text/visual pages | one Markdown section per page/slide/screen |
| `deep-visual` | High-stakes, visually dense, or sales/solution deck material | page-aligned Markdown with careful screenshot inspection and explicit page maps |
| `reading` | User wants a readable article/report | generate only after a page-aligned source exists |

Important: never generate a `reading` version directly from raw extraction when the source is visually complex. First create or verify the page-aligned source.

## Document Routing

Route by observed structure, not only by file extension. A file extension is a hint; the screenshot/rendered view and extracted structure are the source of truth.

| Kind | Typical inputs | Default calibrated structure |
| --- | --- | --- |
| `deck` | PPT/PPTX, proposal PDFs, slide-style PDFs | `## Page NN` with visual sections for dense slides |
| `report` | Word/PDF reports, whitepapers, manuals | document headings plus page anchors where visual layout matters |
| `spreadsheet` | XLS/XLSX/CSV, finance models, dashboards | `## Sheet: Name`, then tables, formulas, charts, dashboard regions |
| `image` | single images, long screenshots, scanned pages | `## Image/Region NN` or split sections by visual region |
| `html` | web pages, local HTML exports | `## Screen/Section NN` with DOM/visual region structure |
| `mixed` | files with multiple strong forms | combine the relevant structures; do not force one template |

Flexible routing rules:

- Upgrade a spreadsheet to visual/dashboard treatment when it contains charts, KPI cards, slicers, pivot tables, dashboards, screenshots, or complex merged-cell layouts.
- Upgrade a Word/PDF report to page-aligned treatment when it contains diagrams, tables, sidebars, screenshots, forms, or page-specific visual meaning.
- Treat PPT/solution decks as `deep-visual` by default when they include product imagery, callouts, case studies, comparison matrices, or contact pages.
- If one document contains multiple forms, use section-level routing. Example: a workbook may have a dashboard sheet, raw data sheets, and formula/model sheets.
- Never let routing block output. If classification is uncertain, choose `mixed` and state the chosen structure in the reconstruction note.

## Workflow

1. Establish deliverables and output path before conversion:
   - default: create `source.calibrated.md`;
   - if the user mentions `outline`, `大纲`, `大纲版`, `two files`, `两个文件`, or asks to generate a version based on the calibrated Markdown, create both `source.calibrated.md` and `source.outline.md`;
   - do not finish the task until every requested deliverable exists.
2. Extract a raw text Markdown draft using MarkItDown or the best local extractor.
3. Render visual references:
   - PDF: render pages to images.
   - PPT/PPTX: convert to PDF, then render pages.
   - HTML: capture screenshots of the relevant page or viewport.
   - Images/long screenshots: use the source image directly or split if needed.
4. Create a manifest with page number, screenshot path, extracted title, text length, and visual-check priority.
5. Inspect only the pages that need visual attention first:
   - sparse text but complex screenshot;
   - diagrams, timelines, architecture maps, tables, matrices, screenshots, logo grids;
   - pages where raw text order looks suspicious.
6. Rebuild Markdown:
   - choose headings from Document Routing, such as `## Page NN: Title`, `## Sheet: Name`, or `## Section NN`;
   - include a screenshot link for each page/screen during validation when visual references exist;
   - keep content from that page/sheet/section only;
   - include page layout/region notes for visual decks;
   - rebuild cards, columns, KPI blocks, matrices, and insight boxes as grouped modules or tables; do not dump text as one bullet per OCR line;
   - convert visual structures using the rules in `references/visual-transcription-rules.md` when needed.
7. Validate page coverage and screenshot links with `scripts/check_output.py` for page/screen-based outputs; pass `--expected-pages` whenever the page count is known. For `deep-visual`, also pass `--require-visual-sections`.
8. If an outline was requested in step 1, generate `source.outline.md` from the calibrated version and re-check that both final files exist.
9. Clean up or hide intermediate files according to Artifact Policy.

## Page Manifest

Prefer creating a manifest before spending tokens on visual inspection. Use:

```bash
python scripts/make_manifest.py --raw raw.md --pages-dir pages --out manifest.md
```

The manifest should help decide which pages need visual checks. Typical fields:

- page number
- screenshot path
- extracted title
- extracted text length
- visual-check priority
- reason

When rendering into an existing directory, prefer:

```bash
python scripts/render_pages.py deck.pdf --out-dir deck.pages --clean
```

## Artifact Policy

By default, the user should see only final deliverables:

```text
source.calibrated.md
source.outline.md   # only when requested
```

Treat the outline as a first-class requested deliverable, not as an optional summary. If requested, it must be generated in the same run as the calibrated Markdown unless the user explicitly asks to postpone it.

Intermediate evidence is allowed but should be treated as working material:

- raw extraction;
- rendered pages/screenshots;
- page or sheet manifest;
- split raw pages;
- draft calibration files.

Prefer storing intermediate material in a temporary work folder such as:

```text
.ky-md-work/source-name/
```

After validation, remove the temporary work folder unless the user asks to keep an audit bundle or screenshot references. If the final calibrated Markdown contains local screenshot links, either keep the screenshot directory as part of an audit bundle or convert the links to non-file source notes before cleanup.

When the user asks for "only the final file", "only two files", or similar, do not leave raw, manifest, split, or rendered-page artifacts beside the final Markdown files.

## Outline Output

When requested, create an outline file from the calibrated Markdown, not from raw extraction. This is mandatory when the prompt asks for an outline, a second Markdown, or two final files.

Suggested filename:

```text
source.outline.md
```

The outline should preserve the document's logic without duplicating all details:

- title and source;
- top-level sections/pages/sheets;
- key claims or findings;
- important tables/charts/diagrams and their role;
- open uncertainties only if the calibrated source marked them.

Recommended outline structure:

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

### 3.1 ...

## 4. Key Evidence

| Evidence | Source | Why it matters |
| --- | --- | --- |
```

For decks and proposals, the outline should group pages by narrative function, not merely repeat every page title. For spreadsheets, group sheets by purpose: dashboard, raw data, assumptions, calculations, outputs, charts.

## Helper Scripts

Use scripts as mechanical helpers; do not load their source unless you need to edit or troubleshoot them.

- `scripts/render_pages.py`: render PDF/PPT/PPTX inputs into page screenshots.
- `scripts/render_pages.py --clean`: remove stale rendered images with the same prefix before rendering.
- `scripts/split_markdown_pages.py`: split raw Markdown on page breaks.
- `scripts/make_manifest.py`: build a page/slide manifest from raw Markdown and screenshots.
- `scripts/check_output.py`: verify page headings and screenshot links.
- `scripts/check_output.py --expected-pages N`: fail on missing pages, duplicate pages, or bad screenshot links.
- `scripts/check_output.py --require-visual-sections`: fail if page sections do not include page purpose, layout map, confirmed content by region, and visual notes.

## Page-Aligned Quality Gate

A page-aligned output is not acceptable if it only summarizes each page. For visual decks and solution proposals, each page section must include enough visual guidance that a reader can reconstruct the slide's information architecture.

Minimum contract per page:

- screenshot link during validation, or a clear source-page note in final deliverable-only mode;
- page purpose or headline;
- layout map for non-trivial pages: main regions and reading order;
- confirmed text grouped by its visual region;
- visual relationships: highlighted columns, center nodes, arrows, callouts, before/after areas, image roles;
- uncertainty note only when text or logos are not reliably legible.

For title or transition pages, a short section is fine. For dense tables, product feature pages, process pages, case-study pages, contact pages, and architecture diagrams, use `deep-visual` standards even if raw extraction has many characters.

Before final delivery, compare the output against these checks:

- During validation, does every visual page have a screenshot link? In final deliverable-only mode, does every visual page keep a clear source-page note?
- Could a reader tell where the text appeared on the slide?
- Are product images, diagrams, callouts, and highlighted areas described?
- Are dense pages structured as tables, region groups, or ordered steps instead of loose bullets?
- Did the output avoid merging adjacent slide content?
- Did it avoid generic filler such as "main body contains paragraphs/cards/graphics" when the actual regions are visible?
- Did it avoid `页面文本（按视觉阅读顺序）` sections with many one-line bullets?

For `deep-visual` outputs, run:

```bash
python scripts/check_output.py --md deck.page-aligned.md --pages-dir deck.pages --expected-pages N --require-visual-sections
```

## References

Load references only when needed:

- `references/visual-transcription-rules.md`: how to convert diagrams, timelines, tables, screenshots, and logos to Markdown.
- `references/output-formats.md`: templates for raw, page-aligned, and reading outputs.
- `references/token-control.md`: strategies for minimizing context use on large documents.

## Reliability Rules

- Treat page-aligned Markdown as the source of truth.
- Do not merge adjacent pages unless the output mode is explicitly `reading`.
- Do not invent unreadable small text, logos, chart labels, or screenshot details.
- Mark uncertain visual details as "not reliably legible" or omit them.
- Keep screenshot links for visual verification while intermediate evidence is retained; in deliverable-only mode, keep source-page notes instead.
- Prefer tables for timelines, matrices, repeated item grids, and comparison layouts.
- Prefer module + relationship lists for architecture diagrams.
