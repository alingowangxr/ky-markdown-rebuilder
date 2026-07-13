# Visual Transcription Rules

Use these rules when raw text extraction loses the structure of a visual page.

## General Page Map

For each page that needs visual inspection, identify:

- title;
- primary regions, from top to bottom and left to right;
- main visual type;
- confirmed text blocks;
- relationships between blocks;
- details that are too small or uncertain.

Keep the final Markdown concise. The goal is reliable content, not pixel-perfect layout narration.

For visual decks, include the page map in the final output when it improves reliability. Do not hide it in analysis only.

Page section fields are LOCKED (see Output Contract in SKILL.md). The only accepted labels, always as H3 headings, always these exact Chinese strings regardless of document language:

- `### 頁面目的`
- `### 佈局地圖`
- `### 按區域確認內容`（區域用 `#### 區域 N：<位置>` 分組）
- `### 視覺備註`

Title, transition, or mostly linear text pages keep all four sections but may reduce each to a single bullet.

## Forbidden Anti-Patterns

Do not use a generic bucket such as `頁面文本（按視覺閱讀順序）` for visually structured pages. If the page has cards, columns, KPI blocks, matrices, diagrams, or insight boxes, rebuild those structures directly.

Avoid generic layout notes that could fit any page, such as:

- "Top or upper-left area is the page title."
- "Main area contains paragraphs, bullets, cards, or graphics."
- "Header/footer/logo/decorations are ignored."

Instead, name the actual visible regions: "left 2x2 policy cards", "right hero image", "bottom green Key Insight box", "three vertical advantage cards", "five innovation cards", and so on.

## Common Visual Types

### Timeline

Convert to a table:

| Time | Event |
| --- | --- |

Preserve chronological order. If the visual is a horizontal timeline but dates are unclear, use the visible order and avoid guessing.

### Flowchart or Process

Convert to ordered steps:

1. Step name: confirmed description.
2. Step name: confirmed description.

If there is a loop, add a short "Loop" note after the steps.

### Architecture Diagram

Use modules and relationships:

- Module A: purpose or visible contents.
- Module B: purpose or visible contents.
- Relationship: A sends data to B; B returns output to C.

Avoid over-describing decorative arrows. Capture meaningful dependencies.

### Matrix or Quadrant

Use a table when labels are visible. If labels are unclear, describe quadrants by position:

| Region | Content |
| --- | --- |
| Top left | ... |

### Table-Like Graphic

Rebuild as a Markdown table if rows and columns are legible. If not, use grouped bullets.

### Merged Cells and Multi-Row Headers (LOCKED)

These three rules are fixed — never choose a different convention per run:

1. **Horizontal merge (跨列)**: repeat the merged content in EVERY spanned column of that row. `งบประมาณ` spanning 2 columns → `| งบประมาณ | งบประมาณ |`. Applies to header and body rows alike; column count must stay aligned.
2. **Vertical merge (跨行)**: write the content in the FIRST row only; leave the corresponding cells in continuation rows EMPTY. Never repeat vertically-merged content in later rows — an empty cell means "merged from above", a repeated value reads as a second data point.
3. **Multi-row header (多行表頭)**: Markdown allows one header row, so the FIRST header row becomes the Markdown header; every remaining header row becomes the first body row(s), in original order. Do not fold multiple header rows into one cell with `<br>` and do not drop sub-header rows.

Example — a two-row header where columns 1-2 are vertically merged and two groups span horizontally:

```markdown
| รายการ/แหล่งเงิน | หน่วยนับ | งบประมาณ | งบประมาณ | ประมาณการ** | ประมาณการ** |
| --- | --- | --- | --- | --- | --- |
| | | ปีที่ 1 แผน | ปีที่ 2 แผน | ปีที่ 3 แผน | ปีที่ 4 แผน |
| รายการที่ 1 : ... | ไร่ | 10,000 | | | 25,000 |
```

### Card Grid

Use one table row per card or one grouped subsection per card:

| Card | Main claim | Supporting text | Tags/visual markers |
| --- | --- | --- | --- |

Preserve the visual grouping, such as 2x2 cards, 2-column problem cards, 3-column advantage cards, or 5-card innovation grids. Do not split each wrapped line into a separate bullet.

### Insight or Callout Box

Use a separate callout group:

- Label: KEY INSIGHT / 核心洞察
- Claim: ...
- Emphasis: highlighted words or numbers

Keep callouts separate from ordinary body cards because they usually contain the page conclusion.

### Logo or Partner Grid

List only reliably identifiable names. Use:

- "Visible partners include: ..."
- "Other logos are present but not reliably legible."

Do not infer an organization from a partial or blurry logo.

### Screenshot Montage

Extract only:

- screenshot title;
- product/page/event name;
- visible date or number if legible;
- main takeaway.

Do not copy tiny UI text unless it is clearly legible.

### Product Feature Slide

Use:

- Product image role: hero image, detail image, dimension diagram, UI screenshot.
- Feature callouts: preserve callout numbers and labels.
- Supporting copy: group by nearby image or callout.
- Visual emphasis: note highlighted capacity, size, speed, or workflow claims.

### Case Study Slide

Use:

- Case subject and headline result.
- Background/setting region.
- Pain points or operating status region.
- Result/KPI region.
- Photo or map role.

Do not merge case background and solution result if they are separate regions.

### Contact Slide

Use:

- QR code labels exactly as visible.
- Business contact details.
- Address blocks, preserving Chinese and English lines.
- Do not infer QR contents beyond visible labels.

### Dense Infographic

Start from the center node, then describe surrounding categories clockwise or by region:

- Center: ...
- Top: ...
- Right: ...
- Bottom: ...
- Left: ...

### Formulas and Equations

Chemistry and math notation uses inline `<sub>`/`<sup>` HTML, never code fences and never plain-text approximations:

- `Zn + H<sub>2</sub>SO<sub>4</sub> = ZnSO<sub>4</sub> + H<sub>2</sub>↑`
- `E = mc<sup>2</sup>`

Preserve arrows (↑ ↓ →), condition annotations above arrows as parenthetical notes, and equation numbering when visible.

### Textbook / Educational Page

- Keep the page's own content headings (表1-1, 實驗1-2, 討論) as `####` headings inside 按區域確認內容; do not replace the locked four-section skeleton with them.
- Boxed tips or callouts become `> **提示**` blockquotes.
- An illustration is described in place: bold caption + one-line description of what the image shows. Never embed the whole source page screenshot as if it were the illustration.
- Do not invent an H1 for a page that has none; follow the Output Contract rule (`# <自擬標題>（自擬）`).

## Uncertainty Rules

- If text is not readable, do not invent it.
- If a label might be wrong, omit it or flag it as uncertain.
- If neighboring pages cover similar topics, keep each page independent in page-aligned output.
- If the user wants a polished reading version, generate it after page-aligned verification.
