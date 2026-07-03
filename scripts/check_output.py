#!/usr/bin/env python3
"""Validate page-aligned Markdown coverage and screenshot links."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--md", required=True, help="Page-aligned Markdown file.")
    parser.add_argument("--pages-dir", help="Directory containing page screenshots.")
    parser.add_argument("--expected-pages", type=int, help="Expected page count.")
    parser.add_argument(
        "--allow-zero-pages",
        action="store_true",
        help="Allow Markdown with no Page headings. Intended only for debugging non-page-aligned files.",
    )
    parser.add_argument(
        "--require-visual-sections",
        action="store_true",
        help=(
            "Require each Page section to include visual reconstruction fields: "
            "Page purpose, Layout map, Confirmed content by region, and Visual notes. "
            "Chinese labels are also accepted."
        ),
    )
    return parser.parse_args()


def page_sections(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^## Page\s+(\d+)\b.*$", text, flags=re.MULTILINE))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(1), text[start:end]))
    return sections


def missing_visual_fields(section: str) -> list[str]:
    required = [
        ("page purpose", r"(页面目的|Page purpose)"),
        ("layout map", r"(布局地图|Layout map)"),
        ("confirmed content by region", r"(按区域确认内容|Confirmed content by region)"),
        ("visual notes", r"(视觉备注|Visual notes)"),
    ]
    missing: list[str] = []
    for label, pattern in required:
        if not re.search(pattern, section, flags=re.IGNORECASE):
            missing.append(label)
    return missing


def generic_reconstruction_failures(section: str) -> list[str]:
    failures: list[str] = []
    generic_layout_patterns = [
        "顶部或左上区域为页标题",
        "主体区域承载段落、条目、卡片或图示信息",
        "页脚/角标保留品牌识别",
        "页眉、页脚、品牌 Logo 与装饰性背景用于版式识别",
        "若本页包含图标、卡片或分栏",
    ]
    generic_hits = [pattern for pattern in generic_layout_patterns if pattern in section]
    if len(generic_hits) >= 2:
        failures.append("generic layout/visual-note template detected")

    raw_text_heading = re.search(r"^#{3,6}\s*页面文本（按视觉阅读顺序）", section, flags=re.MULTILINE)
    if raw_text_heading:
        raw_text_body = section[raw_text_heading.end() :]
        next_heading = re.search(r"^#{3,6}\s+", raw_text_body, flags=re.MULTILINE)
        if next_heading:
            raw_text_body = raw_text_body[: next_heading.start()]
        bullet_count = len(re.findall(r"^\s*-\s+", raw_text_body, flags=re.MULTILINE))
        if bullet_count >= 4:
            failures.append(f"raw bullet dump detected under page text heading ({bullet_count} bullets)")

    return failures


def main() -> None:
    args = parse_args()
    md_path = Path(args.md)
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    headings = re.findall(r"^## Page\s+(\d+)\b", text, flags=re.MULTILINE)

    ok = True
    print(f"page headings: {len(headings)}")
    print(f"unique headings: {len(set(headings))}")

    if not headings and not args.allow_zero_pages:
        ok = False
        print("no page headings detected")

    if len(headings) != len(set(headings)):
        ok = False
        print("duplicate page headings detected")

    if args.expected_pages is not None:
        width = max(2, len(str(args.expected_pages)))
        expected = {f"{i:0{width}d}" for i in range(1, args.expected_pages + 1)}
        actual = set(headings)
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        print(f"missing pages: {missing}")
        print(f"extra pages: {extra}")
        ok = ok and not missing and not extra

    if args.pages_dir:
        pages_dir = Path(args.pages_dir)
        links = re.findall(r"\]\(([^)]+)\)", text)
        links = [
            link.strip()
            for link in links
            if re.search(r"(^|/)page-\d+\.(?:png|jpg|jpeg|webp)$", link.strip(), flags=re.IGNORECASE)
        ]
        missing_links: list[str] = []
        for link in links:
            candidate = (md_path.parent / link).resolve()
            if not candidate.exists():
                candidate = (pages_dir / Path(link).name).resolve()
            if not candidate.exists():
                missing_links.append(link)
        print(f"screenshot links: {len(links)}")
        print(f"missing screenshot links: {missing_links}")
        ok = ok and not missing_links

    if args.require_visual_sections:
        failures: list[str] = []
        for page, section in page_sections(text):
            missing_fields = missing_visual_fields(section)
            if missing_fields:
                failures.append(f"Page {page}: missing {', '.join(missing_fields)}")
            generic_failures = generic_reconstruction_failures(section)
            for failure in generic_failures:
                failures.append(f"Page {page}: {failure}")
        print(f"visual section failures: {len(failures)}")
        for failure in failures:
            print(failure)
        ok = ok and not failures

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
