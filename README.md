# KY Markdown Rebuilder

> 中文说明见下方；English README follows after the Chinese section.

## 中文说明

KY Markdown Rebuilder 是一个面向 Codex / Claude Code 的文档重建 Skill。它用于把视觉结构复杂的文件重建为可靠的 Markdown，而不是只做普通文字提取。

它特别适合处理：

- PDF 报告、白皮书、课程资料、方案文档；
- PPT/PPTX、提案 deck、幻灯片式 PDF；
- 含图表、时间线、矩阵、截图、架构图、logo 墙的视觉型资料；
- 长截图、HTML 页面、Word 类报告；
- 需要按页、按屏、按 slide 保留信息结构的材料。

核心原则：

> 先抽取文本，再渲染页面视觉参考，最后基于页面对齐的视觉源重建 Markdown。

## 能解决什么问题

普通转换工具经常会把视觉型文档变成混乱文本，例如：

- 表格列顺序错乱；
- 卡片、矩阵、时间线被拆成一堆散行；
- 图表、流程图、架构图失去关系；
- PPT 相邻页内容混在一起；
- 图片、截图、logo、强调区域无法解释；
- 只得到 OCR 文本，无法看出原页面的信息层级。

本 Skill 的目标是生成可复用、可校验、按页对齐的 Markdown。对于方案 deck 和复杂报告，它会要求输出包含页面目的、布局地图、按区域确认内容和视觉备注。

## 仓库结构

```text
ky-markdown-rebuilder/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── output-formats.md
│   ├── token-control.md
│   └── visual-transcription-rules.md
└── scripts/
    ├── check_output.py
    ├── make_manifest.py
    ├── render_pages.py
    └── split_markdown_pages.py
```

说明：

- `SKILL.md`：Skill 主说明与执行协议。
- `scripts/`：机械辅助脚本，用于渲染页面、生成 manifest、拆分 Markdown、校验输出。
- `references/`：视觉转写规则、输出格式模板、token 控制策略。
- `agents/openai.yaml`：Codex 端 UI/agent 元数据。Claude Code 可以保留此文件，不影响使用。

## 安装方式

### 安装到 Codex

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/<your-username>/ky-markdown-rebuilder.git ~/.codex/skills/ky-markdown-rebuilder
```

如果你已经把仓库 clone 到本地，也可以复制：

```bash
mkdir -p ~/.codex/skills/ky-markdown-rebuilder
cp -R ./ky-markdown-rebuilder/. ~/.codex/skills/ky-markdown-rebuilder/
```

### 安装到 Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/<your-username>/ky-markdown-rebuilder.git ~/.claude/skills/ky-markdown-rebuilder
```

或从本地复制：

```bash
mkdir -p ~/.claude/skills/ky-markdown-rebuilder
cp -R ./ky-markdown-rebuilder/. ~/.claude/skills/ky-markdown-rebuilder/
```

### 同步到两端

如果你希望 Codex 与 Claude Code 使用同一版本，可以分别 clone 两份，或从一个源目录同步：

```bash
ditto ./ky-markdown-rebuilder ~/.codex/skills/ky-markdown-rebuilder
ditto ./ky-markdown-rebuilder ~/.claude/skills/ky-markdown-rebuilder
```

## 依赖

Skill 本身是 Markdown 指令 + Python helper scripts。不同输入格式可能需要以下工具：

- Python 3.10+；
- `pdftoppm`，通常来自 Poppler，用于 PDF 页面渲染；
- LibreOffice / `soffice`，用于 PPT/PPTX 转 PDF；
- MarkItDown、Pandoc 或宿主环境自带的文档抽取工具，用于原始文本提取。

不同宿主可用工具不完全一致时，仍应遵守 `SKILL.md` 中的页面对齐输出协议。

## 使用方式

在 Codex 或 Claude Code 中请求时，可以直接点名 Skill：

```text
[$ky-markdown-rebuilder] 帮我把这个 PPTX 做成 Markdown
```

或自然语言触发：

```text
把这个视觉比较复杂的 PDF 重建成 page-aligned Markdown
```

典型输出：

```text
source.calibrated.md
source.outline.md   # 仅在用户要求大纲/两个文件时生成
```

## 输出模式

| 模式 | 适用场景 | 输出形态 |
| --- | --- | --- |
| `fast` | 文档基本是线性文本 | 原始转换 + 轻量清理 |
| `page-aligned` | deck、PDF、报告、图文混排资料 | 每页/每屏一个 Markdown section |
| `deep-visual` | 高价值方案、销售 deck、视觉密集文档 | 页面级 Markdown + 布局/区域/视觉关系说明 |
| `reading` | 用户想要可读文章版 | 必须先有 page-aligned 源，再生成阅读版 |

## 辅助脚本

### 渲染 PDF/PPT/PPTX 页面

```bash
python scripts/render_pages.py deck.pdf --out-dir deck.pages --clean
python scripts/render_pages.py slides.pptx --out-dir slides.pages --clean
```

### 生成页面 manifest

```bash
python scripts/make_manifest.py --raw raw.md --pages-dir pages --out manifest.md
```

### 拆分原始 Markdown 页面

```bash
python scripts/split_markdown_pages.py --raw raw.md --out-dir split-pages
```

### 校验输出

```bash
python scripts/check_output.py --md deck.calibrated.md --pages-dir deck.pages --expected-pages 24
```

对于 deep-visual 输出：

```bash
python scripts/check_output.py --md deck.calibrated.md --pages-dir deck.pages --expected-pages 24 --require-visual-sections
```

## GitHub 发布建议

推荐不要上传以下内容：

- `__pycache__/`
- `.DS_Store`
- `.ky-md-work/`
- 渲染出的临时页面截图目录；
- 用户输入文件、客户文档、转换产物。

推荐上传：

- `SKILL.md`
- `README.md`
- `scripts/`
- `references/`
- `agents/openai.yaml`
- `.gitignore`
- 可选：`LICENSE`

## 从本地发布到 GitHub

1. 创建 GitHub 空仓库，建议仓库名：

```text
ky-markdown-rebuilder
```

2. 在本地初始化并提交：

```bash
cd ky-markdown-rebuilder
git init
git add .
git commit -m "Initial release of KY Markdown Rebuilder skill"
```

3. 绑定远程仓库并推送：

```bash
git branch -M main
git remote add origin https://github.com/<your-username>/ky-markdown-rebuilder.git
git push -u origin main
```

4. 推送后检查 GitHub 页面：

- README 是否正常显示；
- `SKILL.md` 是否在根目录；
- `scripts/__pycache__` 是否没有被上传；
- 客户文件、样例转换产物、临时截图是否没有被上传。

## 许可证

如果你希望别人使用、修改或分发，建议添加 `LICENSE`。常见选择：

- MIT：最宽松，适合公开分享工具；
- Apache-2.0：宽松，同时包含专利授权条款；
- 不添加许可证：默认保留全部权利，不建议用于开源协作。

---

# KY Markdown Rebuilder

## English README

KY Markdown Rebuilder is a Codex / Claude Code skill for reconstructing visually complex documents into reliable Markdown. It is not just a plain text extraction workflow; it preserves page-level structure, visual grouping, tables, diagrams, screenshots, cards, and layout relationships whenever those details matter.

Best suited for:

- PDF reports, whitepapers, course packs, and proposals;
- PPT/PPTX decks and slide-style PDFs;
- visual documents with charts, timelines, matrices, screenshots, architecture diagrams, logo grids, and callouts;
- long screenshots, HTML pages, and Word-like reports;
- documents that must remain traceable by page, slide, screen, or region.

Core principle:

> Extract text first, render visual references second, then rebuild Markdown from a page-aligned source of truth.

## Why This Skill Exists

Generic converters often flatten visual documents into noisy text:

- table columns become scrambled;
- cards, matrices, and timelines turn into disconnected lines;
- charts and diagrams lose relationships;
- adjacent PPT slides get merged;
- screenshots, logos, and highlighted regions are not explained;
- OCR text lacks the original information hierarchy.

This skill produces reusable, verifiable, page-aligned Markdown. For solution decks and visually dense reports, the output should include page purpose, layout map, confirmed content by region, and visual notes.

## Repository Structure

```text
ky-markdown-rebuilder/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── output-formats.md
│   ├── token-control.md
│   └── visual-transcription-rules.md
└── scripts/
    ├── check_output.py
    ├── make_manifest.py
    ├── render_pages.py
    └── split_markdown_pages.py
```

File roles:

- `SKILL.md`: main skill instructions and execution protocol.
- `scripts/`: helper scripts for rendering pages, creating manifests, splitting Markdown, and validating outputs.
- `references/`: visual transcription rules, output templates, and token-control strategies.
- `agents/openai.yaml`: Codex-side UI/agent metadata. It can remain in Claude Code installations without affecting usage.

## Installation

### Install for Codex

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/<your-username>/ky-markdown-rebuilder.git ~/.codex/skills/ky-markdown-rebuilder
```

If the repository is already cloned locally:

```bash
mkdir -p ~/.codex/skills/ky-markdown-rebuilder
cp -R ./ky-markdown-rebuilder/. ~/.codex/skills/ky-markdown-rebuilder/
```

### Install for Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/<your-username>/ky-markdown-rebuilder.git ~/.claude/skills/ky-markdown-rebuilder
```

Or copy from a local checkout:

```bash
mkdir -p ~/.claude/skills/ky-markdown-rebuilder
cp -R ./ky-markdown-rebuilder/. ~/.claude/skills/ky-markdown-rebuilder/
```

### Keep Codex and Claude Code in Sync

```bash
ditto ./ky-markdown-rebuilder ~/.codex/skills/ky-markdown-rebuilder
ditto ./ky-markdown-rebuilder ~/.claude/skills/ky-markdown-rebuilder
```

## Dependencies

The skill itself is Markdown instructions plus Python helper scripts. Depending on the input format, the workflow may use:

- Python 3.10+;
- `pdftoppm` from Poppler for PDF page rendering;
- LibreOffice / `soffice` for PPT/PPTX to PDF conversion;
- MarkItDown, Pandoc, or host-native extraction tools for raw text extraction.

When tools differ by host, preserve the page-aligned output contract defined in `SKILL.md`.

## Usage

In Codex or Claude Code, explicitly invoke the skill:

```text
[$ky-markdown-rebuilder] Convert this PPTX into Markdown
```

Or describe the task naturally:

```text
Rebuild this visually complex PDF into page-aligned Markdown.
```

Typical outputs:

```text
source.calibrated.md
source.outline.md   # only when an outline or second file is requested
```

## Output Modes

| Mode | When to use | Output |
| --- | --- | --- |
| `fast` | Mostly linear text | Raw conversion with light cleanup |
| `page-aligned` | Decks, PDFs, reports, mixed visual documents | One Markdown section per page/slide/screen |
| `deep-visual` | High-stakes proposals, sales decks, visually dense materials | Page-aligned Markdown with layout, region, and visual relationship notes |
| `reading` | User wants a readable article/report | Generated only after a page-aligned source exists |

## Helper Scripts

### Render PDF/PPT/PPTX pages

```bash
python scripts/render_pages.py deck.pdf --out-dir deck.pages --clean
python scripts/render_pages.py slides.pptx --out-dir slides.pages --clean
```

### Create a page manifest

```bash
python scripts/make_manifest.py --raw raw.md --pages-dir pages --out manifest.md
```

### Split raw Markdown by pages

```bash
python scripts/split_markdown_pages.py --raw raw.md --out-dir split-pages
```

### Validate output

```bash
python scripts/check_output.py --md deck.calibrated.md --pages-dir deck.pages --expected-pages 24
```

For deep-visual outputs:

```bash
python scripts/check_output.py --md deck.calibrated.md --pages-dir deck.pages --expected-pages 24 --require-visual-sections
```

## Publishing to GitHub

Do not upload:

- `__pycache__/`
- `.DS_Store`
- `.ky-md-work/`
- rendered page screenshot folders;
- user input files, client documents, or generated deliverables.

Recommended files:

- `SKILL.md`
- `README.md`
- `scripts/`
- `references/`
- `agents/openai.yaml`
- `.gitignore`
- optional: `LICENSE`

## Local GitHub Release Steps

1. Create an empty GitHub repository. Recommended name:

```text
ky-markdown-rebuilder
```

2. Initialize and commit locally:

```bash
cd ky-markdown-rebuilder
git init
git add .
git commit -m "Initial release of KY Markdown Rebuilder skill"
```

3. Add the remote and push:

```bash
git branch -M main
git remote add origin https://github.com/<your-username>/ky-markdown-rebuilder.git
git push -u origin main
```

4. After pushing, verify:

- README renders correctly;
- `SKILL.md` is at the repository root;
- `scripts/__pycache__` was not uploaded;
- no private client files, temporary screenshots, or generated artifacts were uploaded.

## License

Add a `LICENSE` if you want others to use, modify, or redistribute the skill.

Common choices:

- MIT: permissive and simple;
- Apache-2.0: permissive with explicit patent terms;
- no license: all rights reserved by default, not recommended for open collaboration.
