#!/usr/bin/env python3
"""Validate calibrated Markdown against the locked output contract.

Enforced (always):
- section headings: ## Page NN / ## Region NN / ## Screen NN / ## Sheet: Name
- no duplicate numbered headings; optional --expected-pages coverage
- every numbered/sheet section has exactly one source line (源图：/源页：)
- reconstruction-note header line (> 重建说明：... 原图逐页查看 N/M 页)
- screenshot links resolve when --pages-dir is given

Enforced with --require-visual-sections:
- exact Chinese H3 labels: ### 页面目的 / ### 布局地图 / ### 按区域确认内容 / ### 视觉备注
- rejection of legacy label styles (English labels, bare-text labels with colons)
- canned-sentence repetition in 视觉备注 across pages
- full-page code-fence dumps
- generic layout/visual-note template detection
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

REQUIRED_LABELS = ["页面目的", "布局地图", "按区域确认内容", "视觉备注"]

LEGACY_LABEL_PATTERNS = [
    (r"^#{2,6}\s*(Page purpose|Layout map|Confirmed content by region|Visual notes)\b", "english heading label"),
    (r"^\s*(Page purpose|Layout map|Confirmed content by region|Visual notes)\s*[:：]", "english bare-text label"),
    (r"^\s*(页面目的|布局地图|按区域确认内容|视觉备注)\s*[:：]", "bare-text label with colon (must be H3 heading)"),
    (r"^#{4,6}\s*(页面目的|布局地图|按区域确认内容|视觉备注)\s*$", "wrong heading level (must be H3)"),
]

GENERIC_LAYOUT_PATTERNS = [
    "顶部或左上区域为页标题",
    "主体区域承载段落、条目、卡片或图示信息",
    "页脚/角标保留品牌识别",
    "页眉、页脚、品牌 Logo 与装饰性背景用于版式识别",
    "若本页包含图标、卡片或分栏",
]

SECTION_HEADING_RE = re.compile(
    r"^## (?:(Page|Region|Screen)\s+(\d+)\b.*|Sheet:\s*(.+?)\s*)$", flags=re.MULTILINE
)
SOURCE_LINE_RE = re.compile(r"^源[图页]：", flags=re.MULTILINE)
RECON_NOTE_RE = re.compile(r"^> 重建说明：.*原图逐页查看\s*\d+\s*/\s*\d+\s*页", flags=re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--md", required=True, help="Calibrated Markdown file.")
    parser.add_argument("--pages-dir", help="Directory containing page screenshots.")
    parser.add_argument("--expected-pages", type=int, help="Expected numbered section count.")
    parser.add_argument(
        "--allow-zero-pages",
        action="store_true",
        help="Allow Markdown with no numbered sections. Intended only for debugging non-page-aligned files.",
    )
    parser.add_argument(
        "--require-visual-sections",
        action="store_true",
        help="Require the locked Chinese H3 labels in every section: "
        "### 页面目的 / ### 布局地图 / ### 按区域确认内容 / ### 视觉备注.",
    )
    return parser.parse_args()


def sections(text: str) -> list[tuple[str, str, str]]:
    """Return (kind, id, body) for each ## section."""
    matches = list(SECTION_HEADING_RE.finditer(text))
    out: list[tuple[str, str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        if match.group(3) is not None:
            kind, ident = "Sheet", match.group(3)
        else:
            kind, ident = match.group(1), match.group(2)
        out.append((kind, ident, text[start:end]))
    return out


def missing_labels(section: str) -> list[str]:
    missing: list[str] = []
    for label in REQUIRED_LABELS:
        if not re.search(rf"^### {re.escape(label)}\s*$", section, flags=re.MULTILINE):
            missing.append(label)
    return missing


def legacy_label_failures(section: str) -> list[str]:
    failures: list[str] = []
    for pattern, reason in LEGACY_LABEL_PATTERNS:
        match = re.search(pattern, section, flags=re.MULTILINE | re.IGNORECASE)
        if match:
            failures.append(f"{reason}: {match.group(0).strip()[:60]!r}")
    return failures


def fence_dump_failures(section: str) -> list[str]:
    failures: list[str] = []
    lines = section.splitlines()
    nonempty = sum(1 for line in lines if line.strip())
    fence_lines = 0
    current = 0
    largest = 0
    in_fence = False
    for line in lines:
        if re.match(r"^\s*(```|~~~)", line):
            if in_fence:
                largest = max(largest, current)
            in_fence = not in_fence
            current = 0
            continue
        if in_fence:
            current += 1
            fence_lines += 1
    largest = max(largest, current)
    if largest >= 20:
        failures.append(f"full-page code fence dump ({largest} fenced lines)")
    elif nonempty and fence_lines / nonempty > 0.5:
        failures.append(f"code fences cover {fence_lines}/{nonempty} non-empty lines")
    return failures


def generic_reconstruction_failures(section: str) -> list[str]:
    failures: list[str] = []
    generic_hits = [pattern for pattern in GENERIC_LAYOUT_PATTERNS if pattern in section]
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


def visual_note_lines(section: str) -> list[str]:
    match = re.search(r"^### 视觉备注\s*$", section, flags=re.MULTILINE)
    if not match:
        return []
    body = section[match.end() :]
    next_heading = re.search(r"^#{1,3}\s+", body, flags=re.MULTILINE)
    if next_heading:
        body = body[: next_heading.start()]
    lines = []
    for line in body.splitlines():
        stripped = re.sub(r"^\s*-\s+", "", line).strip()
        if len(stripped) >= 8:
            lines.append(stripped)
    return lines


def main() -> None:
    args = parse_args()
    md_path = Path(args.md)
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    parsed = sections(text)
    numbered = [(kind, ident, body) for kind, ident, body in parsed if kind != "Sheet"]
    sheet_count = len(parsed) - len(numbered)
    numbers = [ident for _, ident, _ in numbered]

    ok = True
    print(f"numbered sections: {len(numbered)} (Page/Region/Screen)")
    if sheet_count:
        print(f"sheet sections: {sheet_count}")
    print(f"unique numbered sections: {len(set(numbers))}")

    if not parsed and not args.allow_zero_pages:
        ok = False
        print("no section headings detected")

    if len(numbers) != len(set(numbers)):
        ok = False
        duplicates = sorted(n for n, count in Counter(numbers).items() if count > 1)
        print(f"duplicate numbered headings detected: {duplicates}")

    kinds = {kind for kind, _, _ in numbered}
    if len(kinds) > 1:
        ok = False
        print(f"mixed section kinds in one file: {sorted(kinds)}")

    if args.expected_pages is not None:
        width = max(2, len(str(args.expected_pages)))
        expected = {f"{i:0{width}d}" for i in range(1, args.expected_pages + 1)}
        actual = set(numbers)
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        print(f"missing pages: {missing}")
        print(f"extra pages: {extra}")
        ok = ok and not missing and not extra

    # Reconstruction-note header.
    if parsed:
        if RECON_NOTE_RE.search(text):
            print("reconstruction note: ok")
        else:
            ok = False
            print("reconstruction note missing or malformed "
                  "(expected: > 重建说明：模式 ...；来源 `...`；共 M 页；原图逐页查看 N/M 页。)")
        if re.search(r"^## Page\s+\d+：", text, flags=re.MULTILINE):
            ok = False
            print("full-width colon detected in page heading (use '## Page NN: Title')")
        # Whole-file fence dominance: catches transcribe outputs dumped into
        # code fences even when --require-visual-sections is not used.
        all_lines = text.splitlines()
        in_fence = False
        fenced = 0
        nonempty = 0
        for line in all_lines:
            if re.match(r"^\s*(```|~~~)", line):
                in_fence = not in_fence
                continue
            if line.strip():
                nonempty += 1
                if in_fence:
                    fenced += 1
        if nonempty and fenced / nonempty > 0.6:
            ok = False
            print(f"document body is mostly code fences ({fenced}/{nonempty} non-empty lines) — "
                  "transcribe content as text/tables, not fenced dumps")
        entity_hits = re.findall(r"&(?:nbsp|emsp|ensp|thinsp);", text)
        if entity_hits:
            ok = False
            print(f"HTML whitespace entities detected ({len(entity_hits)}x, e.g. &{entity_hits[0][1:]}) — "
                  "indentation is layout, not content; replace with plain text structure")
        glued_tables = 0
        for i in range(len(all_lines) - 2):
            cur = all_lines[i].strip()
            nxt = all_lines[i + 1].strip()
            nxt2 = all_lines[i + 2].strip()
            if (
                cur and not (cur.startswith("|") and cur.endswith("|"))
                and nxt.startswith("|") and nxt.endswith("|")
                and nxt2.startswith("|") and nxt2.endswith("|")
                and all(c in "|-: " for c in nxt2)
            ):
                glued_tables += 1
        if glued_tables:
            ok = False
            print(f"tables missing preceding blank line: {glued_tables} — "
                  "they render as plain text; run scripts/fix_tables.py")

    # Source lines: exactly one per section.
    source_failures: list[str] = []
    for kind, ident, body in parsed:
        count = len(SOURCE_LINE_RE.findall(body))
        if count != 1:
            source_failures.append(f"{kind} {ident}: {count} source lines (expected exactly 1 源图：/源页： line)")
    print(f"source-line failures: {len(source_failures)}")
    for failure in source_failures:
        print(failure)
    ok = ok and not source_failures

    if args.pages_dir:
        pages_dir = Path(args.pages_dir)
        links = re.findall(r"\]\(([^)]+)\)", text)
        links = [
            link.strip()
            for link in links
            if re.search(r"(^|/)page-\d+\.(?:png|jpg|jpeg|webp)$", link.strip(), flags=re.IGNORECASE)
        ]
        missing_links: list[str] = []
        dead_relative_links: list[str] = []
        for link in links:
            candidate = (md_path.parent / link).resolve()
            if candidate.exists():
                continue
            fallback = (pages_dir / Path(link).name).resolve()
            if fallback.exists():
                # The image exists but not at the written path: the link is
                # dead for any Markdown viewer opening the deliverable.
                dead_relative_links.append(link)
            else:
                missing_links.append(link)
        print(f"screenshot links: {len(links)}")
        print(f"missing screenshot links: {missing_links}")
        if dead_relative_links:
            shown = dead_relative_links[:5]
            print(f"dead relative links ({len(dead_relative_links)}): image exists under --pages-dir "
                  f"but not at the written path, e.g. {shown} — fix the link path "
                  "(relative to the .md file) or switch to 源页 notes")
        ok = ok and not missing_links and not dead_relative_links

    if args.require_visual_sections:
        failures: list[str] = []
        note_counter: Counter[str] = Counter()
        for kind, ident, body in parsed:
            label = f"{kind} {ident}"
            missing = missing_labels(body)
            if missing:
                failures.append(f"{label}: missing H3 labels: {', '.join(missing)}")
            for failure in legacy_label_failures(body):
                failures.append(f"{label}: {failure}")
            for failure in fence_dump_failures(body):
                failures.append(f"{label}: {failure}")
            for failure in generic_reconstruction_failures(body):
                failures.append(f"{label}: {failure}")
            for line in set(visual_note_lines(body)):
                note_counter[line] += 1
        for line, count in note_counter.most_common():
            if count >= 3:
                failures.append(f"canned 视觉备注 repeated on {count} pages: {line[:50]!r}")
        print(f"visual section failures: {len(failures)}")
        for failure in failures:
            print(failure)
        ok = ok and not failures

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
