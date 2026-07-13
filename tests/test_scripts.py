from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_output = load_module("check_output", "scripts/check_output.py")
fix_tables = load_module("fix_tables", "scripts/fix_tables.py")
render_pages = load_module("render_pages", "scripts/render_pages.py")


class ScriptTests(unittest.TestCase):
    def test_check_output_accepts_valid_page_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pages_dir = root / "pages"
            pages_dir.mkdir()
            (pages_dir / "page-01.png").write_bytes(b"png")
            md = root / "doc.md"
            md.write_text(
                "\n".join(
                    [
                        "# Title",
                        "",
                        "> 重建說明：模式 page-aligned；來源 `doc.pdf`；共 1 頁；原圖逐頁查看 1/1 頁。",
                        "",
                        "## Page 01: Intro",
                        "",
                        "源圖：[page-01.png](pages/page-01.png)",
                        "",
                        "### 頁面目的",
                        "",
                        "- Intro",
                        "",
                        "### 佈局地圖",
                        "",
                        "- One region",
                        "",
                        "### 按區域確認內容",
                        "",
                        "#### 區域 1：主體區",
                        "",
                        "- Text",
                        "",
                        "### 視覺備註",
                        "",
                        "- Unique note for page 1",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "check_output.py"),
                    "--md",
                    str(md),
                    "--pages-dir",
                    str(pages_dir),
                    "--expected-pages",
                    "1",
                    "--require-visual-sections",
                ],
                capture_output=True,
                text=True,
                cwd=ROOT,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_check_output_rejects_misaligned_source_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pages_dir = root / "pages"
            pages_dir.mkdir()
            (pages_dir / "page-01.png").write_bytes(b"png")
            md = root / "doc.md"
            md.write_text(
                "\n".join(
                    [
                        "# Title",
                        "",
                        "> 重建說明：模式 page-aligned；來源 `doc.pdf`；共 1 頁；原圖逐頁查看 1/1 頁。",
                        "",
                        "## Page 01: Intro",
                        "",
                        "- wrong line before source",
                        "",
                        "源圖：[page-01.png](pages/page-01.png)",
                    ]
                ),
                encoding="utf-8",
            )
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "check_output.py"),
                    "--md",
                    str(md),
                    "--pages-dir",
                    str(pages_dir),
                    "--expected-pages",
                    "1",
                    "--require-visual-sections",
                ],
                capture_output=True,
                text=True,
                cwd=ROOT,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("source line must be the first non-empty line", proc.stdout)

    def test_check_output_rejects_mismatched_screenshot_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pages_dir = root / "pages"
            pages_dir.mkdir()
            (pages_dir / "page-01.png").write_bytes(b"png")
            (pages_dir / "page-02.png").write_bytes(b"png")
            md = root / "doc.md"
            md.write_text(
                "\n".join(
                    [
                        "# Title",
                        "",
                        "> 重建說明：模式 page-aligned；來源 `doc.pdf`；共 1 頁；原圖逐頁查看 1/1 頁。",
                        "",
                        "## Page 01: Intro",
                        "",
                        "源圖：[page-02.png](pages/page-02.png)",
                    ]
                ),
                encoding="utf-8",
            )
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "check_output.py"),
                    "--md",
                    str(md),
                    "--pages-dir",
                    str(pages_dir),
                    "--expected-pages",
                    "1",
                    "--require-visual-sections",
                ],
                capture_output=True,
                text=True,
                cwd=ROOT,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("screenshot link does not match section number", proc.stdout)

    def test_fix_tables_repairs_ragged_table(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "table.md"
            path.write_text(
                "\n".join(
                    [
                        "Intro",
                        "| A | B |",
                        "| --- | --- |",
                        "| 1 |",
                    ]
                ),
                encoding="utf-8",
            )
            fixed = fix_tables.fix_markdown(path)
            self.assertEqual(fixed, 1)
            self.assertEqual(
                path.read_text(encoding="utf-8").splitlines(),
                [
                    "Intro",
                    "",
                    "|A|B|",
                    "|---|---|",
                    "|1||",
                ],
            )

    def test_render_pages_normalize_padding_is_collision_safe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            (out_dir / "page-1.png").write_text("1", encoding="utf-8")
            (out_dir / "page-2.png").write_text("2", encoding="utf-8")
            (out_dir / "page-10.png").write_text("10", encoding="utf-8")
            render_pages.normalize_padding(out_dir, "page")
            self.assertTrue((out_dir / "page-01.png").exists())
            self.assertTrue((out_dir / "page-02.png").exists())
            self.assertTrue((out_dir / "page-10.png").exists())
            self.assertFalse((out_dir / "page-1.png").exists())
            self.assertFalse((out_dir / "page-2.png").exists())


if __name__ == "__main__":
    unittest.main()
