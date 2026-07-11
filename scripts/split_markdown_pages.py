#!/usr/bin/env python3
"""Split MarkItDown-style Markdown into per-page text files.

Supports form-feed breaks and MarkItDown's ``<!-- Slide number: N -->``
markers for PPT/PPTX sources.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SLIDE_MARKER_RE = re.compile(r"<!--\s*Slide number:\s*(\d+)\s*-->", flags=re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", required=True, help="Raw Markdown file.")
    parser.add_argument("--out-dir", required=True, help="Directory for page text files.")
    parser.add_argument("--prefix", default="page", help="Output filename prefix.")
    return parser.parse_args()


def split_pages(raw_text: str) -> list[str]:
    if "\f" in raw_text:
        return raw_text.split("\f")
    matches = list(SLIDE_MARKER_RE.finditer(raw_text))
    if matches:
        pages: dict[int, str] = {}
        for index, match in enumerate(matches):
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(raw_text)
            pages[int(match.group(1))] = raw_text[start:end]
        total = max(pages)
        return [pages.get(number, "") for number in range(1, total + 1)]
    return [raw_text]


def main() -> None:
    args = parse_args()
    raw_path = Path(args.raw)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    text = raw_path.read_text(encoding="utf-8", errors="ignore")
    pages = split_pages(text)
    width = max(2, len(str(len(pages))))

    for index, page in enumerate(pages, 1):
        out = out_dir / f"{args.prefix}-{index:0{width}d}.md"
        out.write_text(page.strip() + "\n", encoding="utf-8")

    print(f"wrote {len(pages)} pages to {out_dir}")


if __name__ == "__main__":
    main()
