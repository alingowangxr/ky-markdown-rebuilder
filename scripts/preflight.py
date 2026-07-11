#!/usr/bin/env python3
"""Report which document-pipeline tools are available before starting work.

Run once per session so the pipeline never discovers missing tools mid-run.
Informational by default (always exits 0); --strict exits 1 when a core tool
(pdftoppm) is missing.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

FALLBACK_DIRS = [
    Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/bin",
    Path("/opt/homebrew/bin"),
    Path("/usr/local/bin"),
    Path("/usr/bin"),
]

COMMANDS = [
    # (command, needed for, hint when missing)
    ("pdftoppm", "core: render PDF pages to PNG", "brew install poppler / apt install poppler-utils"),
    ("pdfinfo", "page count / text-layer detection", "brew install poppler / apt install poppler-utils"),
    ("soffice", "PPT/PPTX -> PDF conversion", "brew install --cask libreoffice / apt install libreoffice"),
    ("markitdown", "raw text extraction", "pipx install 'markitdown[all]'"),
    ("tesseract", "OCR route for scanned documents", "brew install tesseract tesseract-lang / apt install tesseract-ocr"),
]

MODULES = [
    ("PIL", "contact sheets / image handling", "python3 -m pip install pillow"),
    ("pypdf", "text-layer inspection fallback", "python3 -m pip install pypdf"),
]


def find_command(command: str) -> str | None:
    path = shutil.which(command)
    if path:
        return path
    for directory in FALLBACK_DIRS:
        candidate = directory / command
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def tesseract_langs(tesseract: str) -> list[str]:
    try:
        proc = subprocess.run(
            [tesseract, "--list-langs"], capture_output=True, text=True, timeout=15
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    langs = []
    for line in (proc.stdout + proc.stderr).splitlines():
        line = line.strip()
        if line and not line.startswith("List of") and "/" not in line:
            langs.append(line)
    return langs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Exit 1 when pdftoppm is missing.")
    args = parser.parse_args()

    core_missing = False
    print("| Tool | Status | Needed for | Hint |")
    print("| --- | --- | --- | --- |")
    for command, needed, hint in COMMANDS:
        path = find_command(command)
        if path:
            status = f"ok ({path})"
            hint_cell = ""
        else:
            status = "MISSING"
            hint_cell = hint
            if command == "pdftoppm":
                core_missing = True
        print(f"| {command} | {status} | {needed} | {hint_cell} |")

    for module, needed, hint in MODULES:
        found = importlib.util.find_spec(module) is not None
        status = "ok" if found else "MISSING"
        print(f"| python3 {module} | {status} | {needed} | {'' if found else hint} |")

    tesseract = find_command("tesseract")
    if tesseract:
        langs = tesseract_langs(tesseract)
        shown = ", ".join(langs[:20]) + (" ..." if len(langs) > 20 else "")
        print(f"\ntesseract languages: {shown or 'none detected'}")
        print("(scanned Chinese/Thai documents need chi_sim / chi_tra / tha; "
              "install via: brew install tesseract-lang / apt install tesseract-ocr-<lang>)")

    print("\nnote: always call scripts with python3; a bare `python` may not exist on this machine.")
    sys.exit(1 if (args.strict and core_missing) else 0)


if __name__ == "__main__":
    main()
