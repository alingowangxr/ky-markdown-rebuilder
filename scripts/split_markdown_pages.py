#!/usr/bin/env python3
"""Split MarkItDown-style Markdown into per-page text files."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", required=True, help="Raw Markdown file.")
    parser.add_argument("--out-dir", required=True, help="Directory for page text files.")
    parser.add_argument("--prefix", default="page", help="Output filename prefix.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_path = Path(args.raw)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    text = raw_path.read_text(encoding="utf-8", errors="ignore")
    pages = text.split("\f")
    width = max(2, len(str(len(pages))))

    for index, page in enumerate(pages, 1):
        out = out_dir / f"{args.prefix}-{index:0{width}d}.md"
        out.write_text(page.strip() + "\n", encoding="utf-8")

    print(f"wrote {len(pages)} pages to {out_dir}")


if __name__ == "__main__":
    main()

