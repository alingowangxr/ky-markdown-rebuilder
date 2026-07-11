#!/usr/bin/env python3
"""Create a page manifest from raw Markdown and rendered page images."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

SLIDE_MARKER_RE = re.compile(r"<!--\s*Slide number:\s*(\d+)\s*-->", flags=re.IGNORECASE)


def split_pages(raw_text: str) -> list[str]:
    """Split raw Markdown into pages.

    Supports form-feed breaks (pdftotext style) and MarkItDown's
    ``<!-- Slide number: N -->`` markers for PPT/PPTX sources.
    """
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", required=True, help="Raw Markdown with optional form-feed page breaks.")
    parser.add_argument("--pages-dir", required=True, help="Directory containing rendered page images.")
    parser.add_argument("--out", required=True, help="Output manifest Markdown path.")
    parser.add_argument("--page-prefix", default="page", help="Image page prefix, e.g. page-01.png.")
    return parser.parse_args()


def first_title(page: str, fallback: str) -> str:
    for line in page.splitlines():
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^#+\s*", "", line)
        return line[:120]
    return fallback


def priority(chars: int) -> tuple[str, str]:
    if chars <= 80:
        return "high", "sparse extracted text; inspect screenshot"
    if chars <= 300:
        return "medium", "moderate text; inspect if visually complex"
    return "low", "text extraction likely sufficient unless layout is complex"


def image_sort_key(path: Path) -> tuple[int, str]:
    match = re.search(r"(\d+)(?=\.[^.]+$)", path.name)
    if match:
        return int(match.group(1)), path.name
    return 10**9, path.name


def image_page_number(path: Path) -> int | None:
    match = re.search(r"(\d+)(?=\.[^.]+$)", path.name)
    if not match:
        return None
    return int(match.group(1))


def main() -> None:
    args = parse_args()
    raw = Path(args.raw)
    pages_dir = Path(args.pages_dir)
    out = Path(args.out)

    raw_text = raw.read_text(encoding="utf-8", errors="ignore")
    text_pages = split_pages(raw_text)
    images = sorted(
        (
            p for p in pages_dir.iterdir()
            if p.is_file()
            and p.suffix.lower() in IMAGE_EXTS
            and re.match(rf"^{re.escape(args.page_prefix)}-\d+\.[^.]+$", p.name)
        ),
        key=image_sort_key,
    )
    image_numbers = [page_number for image in images if (page_number := image_page_number(image)) is not None]
    raw_has_pages = len(text_pages) > 1 or bool(raw_text.strip())
    text_total = len(text_pages) if raw_has_pages else 0
    image_total = max(image_numbers) if image_numbers else len(images)
    total = max(text_total, image_total)
    width = max(2, len(str(total)))
    image_by_page = {
        page_number: image
        for image in images
        if (page_number := image_page_number(image)) is not None
    }

    rows = [
        "| Page | Screenshot | Extracted title | Text chars | Priority | Reason |",
        "| --- | --- | --- | ---: | --- | --- |",
    ]

    for i in range(1, total + 1):
        page_text = text_pages[i - 1] if i <= len(text_pages) else ""
        chars = len(page_text.strip())
        title = first_title(page_text, f"Page {i:0{width}d}")
        prio, reason = priority(chars)
        image = image_by_page[i].as_posix() if i in image_by_page else ""
        rows.append(
            f"| {i:0{width}d} | {image} | {title.replace('|', '/')} | {chars} | {prio} | {reason} |"
        )

    out.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"wrote manifest for {total} pages to {out}")


if __name__ == "__main__":
    main()
