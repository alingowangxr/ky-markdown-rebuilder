# KY Markdown Rebuilder

一个用于 **Codex / Claude Code** 的文档重建 Skill。

用途：把视觉结构复杂的 PDF、PPT、长截图、报告、方案 deck 等资料，重建成清晰、可靠、按页对齐的 Markdown。

> 可以尽量保留页面结构、表格、卡片、图示关系和视觉阅读顺序。

---

## 适合处理

- PPT / PPTX / slide deck
- PDF 报告、白皮书、课程资料
- 图文混排的方案文档
- 含表格、流程图、架构图、时间线、矩阵的资料
- 长截图或视觉密集页面

不适合简单纯文本文件。纯文本文件直接转换即可，不需要这个 Skill。

---

## 安装到 Codex

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/KyrieCheungYep/ky-markdown-rebuilder.git ~/.codex/skills/ky-markdown-rebuilder
```

## 安装到 Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/KyrieCheungYep/ky-markdown-rebuilder.git ~/.claude/skills/ky-markdown-rebuilder
```

---

## 使用方式

在 Codex 或 Claude Code 中直接点名这个 Skill：

```text
[$ky-markdown-rebuilder] 帮我把这个 PPTX 做成 Markdown
```

也可以自然语言触发：

```text
把这个视觉比较复杂的 PDF 重建成按页对齐的 Markdown
```

---

## 默认输出

通常会生成：

```text
source.calibrated.md
```

如果你要求大纲版、outline、两个文件，则会同时生成：

```text
source.outline.md
```

---

## 输出特点

对于复杂文档，Markdown 会尽量按原页面重建：

- 每页或每张 slide 单独成节
- 保留页面标题和主要内容
- 表格尽量转成 Markdown 表格
- 卡片、分栏、流程、矩阵会按结构整理
- 对图片、截图、图表、架构关系做必要说明
- 避免把页面内容混成一大坨散乱文本

---

## English

KY Markdown Rebuilder is a document reconstruction skill for **Codex / Claude Code**.

It converts visually complex PDFs, PPT decks, long screenshots, reports, and proposal documents into clean, reliable, page-aligned Markdown.

It is designed for documents where plain text extraction is not enough, especially when layout, tables, diagrams, cards, timelines, screenshots, or visual hierarchy matter.

### Install for Codex

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/KyrieCheungYep/ky-markdown-rebuilder.git ~/.codex/skills/ky-markdown-rebuilder
```

### Install for Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/KyrieCheungYep/ky-markdown-rebuilder.git ~/.claude/skills/ky-markdown-rebuilder
```

### Usage

```text
[$ky-markdown-rebuilder] Convert this PPTX into Markdown
```

Typical output:

```text
source.calibrated.md
```

If an outline is requested:

```text
source.outline.md
```
