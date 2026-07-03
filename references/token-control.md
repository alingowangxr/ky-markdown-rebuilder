# Token Control

Visual document rebuilding can become token-heavy. Use this order of operations.

## Default Strategy

1. Extract raw text.
2. Render pages/screens.
3. Generate a manifest.
4. Inspect high-priority pages first.
5. Build page-aligned Markdown.
6. Validate page coverage.

## Prioritize Visual Inspection

Inspect visually when:

- extracted text is very short;
- page has a diagram, flowchart, timeline, matrix, table, screenshot montage, or logo grid;
- page is a sales/solution deck slide with product images, callouts, case results, or contact blocks;
- raw text order is clearly jumbled;
- the page is important to the user's purpose.

Do not inspect deeply when:

- the page is text-dominant and raw extraction is coherent;
- the page is a section divider;
- the page is a title or closing slide;
- the user requested a quick conversion.

## Practical Thresholds

These are heuristics, not hard rules:

- `0-80` extracted characters: visual check likely needed.
- `80-300` extracted characters: inspect if screenshot is visually complex.
- `300+` extracted characters: use raw text unless layout is suspicious.

Exception: for slide decks and solution proposals, inspect visually any page with product imagery, highlighted KPIs, before/after comparison, diagrams, or dense tables even when extracted text exceeds 300 characters.

## Batch Workflow

For large documents:

1. Build the manifest for all pages.
2. Summarize priorities.
3. Work in batches of 5-10 pages.
4. Validate after each batch if the output is long.

## Avoiding Rework

- Keep a screenshot link in every page-aligned section.
- Keep raw text available as a separate file.
- Use page numbers as immutable anchors.
- Generate reading versions only after the page-aligned source is stable.
