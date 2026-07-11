# Token Control

Visual document rebuilding can become token-heavy. Use this order of operations.

## Default Strategy

1. Extract raw text.
2. Render pages/screens.
3. Generate a manifest.
4. Inspect high-priority pages first.
5. Build page-aligned Markdown.
6. Validate page coverage.

## Contact Sheets Are Triage Only

Thumbnail grids (contact sheets) are a cheap way to decide WHICH pages need attention. They are never a transcription source:

- transcribing text, numbers, or table contents from a thumbnail is a contract violation — small text read from a 300px-wide thumbnail is guesswork;
- every page whose section you write in `deep-visual` or `ocr` mode must have been opened at original resolution;
- pages skipped at original resolution reduce the `原图逐页查看 N/M` count in the reconstruction note — report it truthfully instead of inflating coverage.

If a document is too large to inspect every page (e.g. 86 image-only pages), say so and agree on scope with the user instead of silently downgrading to thumbnails.

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
