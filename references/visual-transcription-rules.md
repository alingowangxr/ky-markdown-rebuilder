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

Recommended page section fields:

- Page purpose
- Layout map
- Confirmed content by region
- Visual notes

Use a shorter form only for title, transition, or mostly linear text pages.

## Forbidden Anti-Patterns

Do not use a generic bucket such as `页面文本（按视觉阅读顺序）` for visually structured pages. If the page has cards, columns, KPI blocks, matrices, diagrams, or insight boxes, rebuild those structures directly.

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

## Uncertainty Rules

- If text is not readable, do not invent it.
- If a label might be wrong, omit it or flag it as uncertain.
- If neighboring pages cover similar topics, keep each page independent in page-aligned output.
- If the user wants a polished reading version, generate it after page-aligned verification.
