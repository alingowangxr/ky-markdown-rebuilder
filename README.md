# KY Markdown Rebuilder

把视觉文档重建成**可核对、按页对齐、结构可靠的 Markdown**。

它不是普通的“文件转 Markdown”工具，而是一套面向 Codex、Claude Code 和 Antigravity 的文档重建 Skill：先提取文本，再渲染原始页面，最后结合页面视觉结构校准内容，并通过脚本检查页数、格式、图片链接和输出契约。

适合处理普通文本提取容易失真的资料，例如 PDF、PPT/PPTX、扫描件、长截图、报告、白皮书、课程资料、方案 deck，以及包含表格、流程图、架构图、时间线、卡片或多栏布局的文档。

## 为什么用它

普通转换工具通常只保留文本，容易出现阅读顺序错乱、跨页串内容、表格散架、图示关系丢失等问题。

KY Markdown Rebuilder 使用“文本提取 + 页面渲染 + 原图核对 + 机械验收”的方式重建文档：

- 每页、每张 Slide 或每个视觉区域单独成节，避免相邻页面内容混在一起。
- 保留标题、分栏、卡片、表格、流程、矩阵和图示关系。
- 对视觉密集页面使用原始分辨率检查，而不是从缩略图猜内容。
- 扫描件优先使用视觉模型逐页转写，无法使用时才回退到 Tesseract OCR。
- 无法可靠辨认的金额、单位或小字会显式标记，不静默猜测。
- 输出前运行检查器；格式漂移、缺页、死链接或表格错误会阻止交付。
- 如实记录真正打开原图核对的页数，不把缩略图浏览算作逐页检查。

## 支持的输入

- PDF 报告、白皮书、手册、课程资料
- PPT / PPTX / slide deck / 方案文件
- 扫描 PDF、拍照书页、图片型文档
- Word 风格报告和图文混排文档
- HTML 页面、本地网页导出
- 长截图和单张复杂图片
- 带图表、KPI 卡片或仪表盘的表格文件

纯文本或结构简单的 Markdown 不需要使用本 Skill，直接转换更快。

## 输出模式

| 模式 | 适用场景 | 结果 |
| --- | --- | --- |
| `fast` | 以线性文本为主的文档 | 原始转换 + 轻量清理 |
| `page-aligned` | PDF、报告、普通 deck、图文混排资料 | 每页一个 Markdown 区块 |
| `deep-visual` | 高风险、视觉密集、销售或解决方案 deck | 逐页原图检查 + 视觉结构重建 |
| `transcribe` | 扫描书籍、表格、预算或档案资料 | 按页 1:1 转写正文和表格，不添加版式评论 |

如果需要更适合连续阅读的文章版，可以在 `page-aligned` 校准版完成后继续生成 `reading` 版本；不会直接从未经校准的原始提取结果生成。

## 默认产物

默认生成：

```text
source.calibrated.md
```

如果用户要求“大纲”“outline”或“两个文件”，还会生成：

```text
source.outline.md
```

如需翻译版，会单独生成：

```text
source.calibrated.zh.md
```

翻译版从校准版生成，并回到原始页面抽查；不会把翻译混进原文校准文件。

中间截图、原始提取、页清单和分批草稿统一保存在：

```text
.ky-md-work/<source-name>/
```

这些证据文件会保留到用户确认结果无误后再删除。

## 安装

### Codex

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/KyrieCheungYep/ky-markdown-rebuilder.git \
  ~/.codex/skills/ky-markdown-rebuilder
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/KyrieCheungYep/ky-markdown-rebuilder.git \
  ~/.claude/skills/ky-markdown-rebuilder
```

### Antigravity

把仓库复制到当前 workspace，在任务中要求 Agent 按仓库内的 `SKILL.md` 执行。

### 更新已有安装

Codex：

```bash
git -C ~/.codex/skills/ky-markdown-rebuilder pull --ff-only
```

Claude Code：

```bash
git -C ~/.claude/skills/ky-markdown-rebuilder pull --ff-only
```

## 环境预检

安装后建议先运行：

```bash
python3 ~/.codex/skills/ky-markdown-rebuilder/scripts/preflight.py
```

预检会报告当前环境是否具备：

- `pdftoppm` / `pdfinfo`：PDF 页渲染、页数和文本层检测
- `soffice`：PPT/PPTX 转 PDF
- `markitdown`：原始文本提取
- `tesseract`：扫描件 OCR 后备方案及已安装语言包
- `PIL` / `pypdf`：图片处理和 PDF 文本层检查

并非所有输入都需要全部工具。Skill 会根据文件类型和当前环境选择可用路线，不会在任务中途静默安装依赖。

## 使用方式

在 Codex 或 Claude Code 中直接点名 Skill：

```text
使用 $ky-markdown-rebuilder，把 proposal.pdf 重建成按页对齐的 Markdown。
```

视觉密集的方案或销售 deck：

```text
使用 $ky-markdown-rebuilder，以 deep-visual 模式重建这个 PPTX，
并额外生成一份 outline。
```

扫描件 1:1 转写：

```text
使用 $ky-markdown-rebuilder，把这份扫描 PDF 按原文逐页转写成 Markdown。
表格保留为 Markdown 表格，不翻译，不要版式分析。
```

也可以直接用自然语言触发：

```text
把这个视觉结构复杂的 PDF 重建成可核对的 Markdown，保留每页结构和表格。
```

## 工作流程

```text
环境预检
  → 提取原始文本
  → 渲染逐页原图
  → 建立页清单并判断检查优先级
  → 按原图重建 Markdown
  → 运行输出检查器
  → 交付校准版 / 大纲版
```

对于无文本层的扫描件，会切换到 `transcribe` 路线：优先从原始分辨率页面直接转写；只有在视觉模型不可用时才使用 Tesseract。

## 输出质量契约

`scripts/check_output.py` 会在交付前检查关键约束，包括：

- 页码是否连续，页数是否完整
- 每页是否有且只有一个来源行
- 页面标题、固定结构标签和标点是否符合约定
- 截图链接是否真实可用，链接位置是否与实际页面图片一致
- 是否存在整页代码围栏、HTML 空白实体或无法渲染的表格
- 是否重复使用空泛的版式套话或罐头式视觉备注
- `deep-visual` / `page-aligned` 是否包含完整的页面结构信息

检查失败时不应交付结果；先修正，再重新运行检查。

## 内置脚本

| 脚本 | 用途 |
| --- | --- |
| `scripts/preflight.py` | 检查文档处理工具和语言包 |
| `scripts/render_pages.py` | 把 PDF、PPT、PPTX 渲染成逐页图片 |
| `scripts/split_markdown_pages.py` | 按分页符或 Slide 标记拆分原始 Markdown |
| `scripts/make_manifest.py` | 生成页码、标题、文本长度和视觉检查优先级清单 |
| `scripts/check_output.py` | 检查页数、格式、链接和输出质量契约 |
| `scripts/fix_tables.py` | 修复扫描件转写后列数不齐的 Markdown 表格 |

所有脚本统一使用 `python3` 调用。

## 目录结构

```text
ky-markdown-rebuilder/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── output-formats.md
│   ├── token-control.md
│   └── visual-transcription-rules.md
└── scripts/
    ├── check_output.py
    ├── fix_tables.py
    ├── make_manifest.py
    ├── preflight.py
    ├── render_pages.py
    └── split_markdown_pages.py
```

## English

KY Markdown Rebuilder is a document-reconstruction skill for Codex, Claude Code, and Antigravity. It turns visually complex PDFs, slide decks, scanned documents, long screenshots, and reports into reliable, page-aligned Markdown.

Instead of trusting plain text extraction alone, it combines text extraction, page rendering, original-resolution visual inspection, structured reconstruction, and automated output validation. It also provides a dedicated `transcribe` route for image-only or scanned documents.

Typical usage:

```text
Use $ky-markdown-rebuilder to rebuild this PDF as page-aligned Markdown.
Create an outline as a second deliverable.
```

Typical output:

```text
source.calibrated.md
source.outline.md
```

See `SKILL.md` for the complete workflow and output contract.
