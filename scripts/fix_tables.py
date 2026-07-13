#!/usr/bin/env python3
"""Normalize Markdown tables after batch transcription.

Two fixes, applied in place:
1. Insert a blank line before any table that directly follows a text line —
   without it, Markdown renderers show the table as plain text.
2. Pad every row to the table's max column count (empty trailing cells are
   often dropped during transcription).

Only tables with a separator row are touched; other lines pass through.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", help="Markdown files to fix in place.")
    return parser.parse_args()


def column_count(line: str) -> int:
    line = line.strip()
    if not line.startswith("|") or not line.endswith("|"):
        return -1
    return line.count("|") - 1


def split_row(line: str) -> list[str]:
    stripped = line.strip()
    if not is_table_line(stripped):
        return [stripped]
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def join_row(cells: list[str]) -> str:
    return "|" + "|".join(cells) + "|"


def pad_row(line: str, target_cols: int, is_separator: bool) -> str:
    cells = split_row(line)
    if len(cells) >= target_cols:
        return join_row(cells)
    filler = "---" if is_separator else ""
    cells.extend([filler] * (target_cols - len(cells)))
    return join_row(cells)


def is_table_line(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|")


def is_separator_row(line: str) -> bool:
    stripped = line.strip()
    return is_table_line(line) and all(c in "|-: " for c in stripped)


def insert_blank_before_tables(lines: list[str]) -> tuple[list[str], int]:
    out: list[str] = []
    inserted = 0
    for i, line in enumerate(lines):
        out.append(line)
        if (
            i + 2 < len(lines)
            and line.strip()
            and not is_table_line(line)
            and is_table_line(lines[i + 1])
            and is_separator_row(lines[i + 2])
        ):
            out.append("")
            inserted += 1
    return out, inserted


def fix_markdown(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    lines, blank_inserts = insert_blank_before_tables(lines)
    if blank_inserts:
        print(f"{path}: inserted {blank_inserts} blank line(s) before tables")
    out_lines: list[str] = []
    fixed_tables = 0

    i = 0
    while i < len(lines):
        if is_table_line(lines[i]):
            j = i
            table = []
            while j < len(lines) and is_table_line(lines[j]):
                table.append(lines[j])
                j += 1
            has_separator = len(table) >= 2 and all(c in "|-: " for c in table[1].strip())
            if has_separator:
                max_cols = max(column_count(t) for t in table)
                rebuilt = [pad_row(t, max_cols, is_separator=(k == 1)) for k, t in enumerate(table)]
                if rebuilt != [t.strip() for t in table]:
                    fixed_tables += 1
                out_lines.extend(rebuilt)
            else:
                out_lines.extend(table)
            i = j
        else:
            out_lines.append(lines[i])
            i += 1

    path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    return fixed_tables


def main() -> None:
    args = parse_args()
    for name in args.files:
        path = Path(name)
        fixed = fix_markdown(path)
        print(f"{path}: normalized {fixed} table(s)")


if __name__ == "__main__":
    main()
