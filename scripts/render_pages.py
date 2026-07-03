#!/usr/bin/env python3
"""Render visual document pages to PNG images.

Supported directly:
- PDF via pdftoppm.
- PPT/PPTX via LibreOffice conversion to PDF, then pdftoppm.

HTML screenshots are environment-specific; use browser tooling when available.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="PDF, PPT, or PPTX file.")
    parser.add_argument("--out-dir", required=True, help="Output directory for PNG pages.")
    parser.add_argument("--dpi", type=int, default=150, help="Render DPI for pdftoppm.")
    parser.add_argument("--prefix", default="page", help="Output image prefix.")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing rendered images with the same prefix before rendering.",
    )
    return parser.parse_args()


def require(command: str) -> str:
    path = shutil.which(command)
    if path:
        return path
    candidates = [
        Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/bin" / command,
        Path("/opt/homebrew/bin") / command,
        Path("/usr/local/bin") / command,
        Path("/usr/bin") / command,
    ]
    for candidate in candidates:
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)
    raise SystemExit(f"required command not found: {command}")


def run_quiet(command: list[str]) -> None:
    proc = subprocess.run(command, text=True, capture_output=True)
    filtered_stderr = "\n".join(
        line
        for line in proc.stderr.splitlines()
        if "Fontconfig error" not in line
        and "No writable cache directories" not in line
        and "Cannot load default config file" not in line
        and "poppler/prefix/var/cache/fontconfig" not in line
        and ".cache/fontconfig" not in line
    ).strip()
    if proc.returncode != 0:
        if proc.stdout.strip():
            print(proc.stdout.strip())
        if filtered_stderr:
            print(filtered_stderr)
        raise subprocess.CalledProcessError(proc.returncode, command)
    if filtered_stderr:
        print(filtered_stderr)


def render_pdf(pdf: Path, out_dir: Path, dpi: int, prefix: str) -> None:
    pdftoppm = require("pdftoppm")
    out_dir.mkdir(parents=True, exist_ok=True)
    run_quiet(
        [pdftoppm, "-png", "-r", str(dpi), str(pdf), str(out_dir / prefix)],
    )


def ppt_to_pdf(src: Path, tmp_dir: Path) -> Path:
    soffice = require("soffice")
    run_quiet(
        [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(tmp_dir), str(src)],
    )
    pdf = tmp_dir / f"{src.stem}.pdf"
    if not pdf.exists():
        matches = list(tmp_dir.glob("*.pdf"))
        if matches:
            return matches[0]
        raise SystemExit("LibreOffice conversion did not produce a PDF")
    return pdf


def main() -> None:
    args = parse_args()
    src = Path(args.input)
    out_dir = Path(args.out_dir)
    suffix = src.suffix.lower()

    if args.clean and out_dir.exists():
        for old in out_dir.glob(f"{args.prefix}-*.png"):
            old.unlink()

    if suffix == ".pdf":
        render_pdf(src, out_dir, args.dpi, args.prefix)
    elif suffix in {".ppt", ".pptx"}:
        with tempfile.TemporaryDirectory() as tmp:
            pdf = ppt_to_pdf(src, Path(tmp))
            render_pdf(pdf, out_dir, args.dpi, args.prefix)
    else:
        raise SystemExit(f"unsupported render input: {suffix}")

    print(f"rendered pages to {out_dir}")


if __name__ == "__main__":
    main()
