---
description: Claude Code Skills 技能库 — 收录官方及自定义 Skill 的用途、触发方式、参数与最佳实践，帮助开发者高效利用 Slash Command 扩展 Claude Code 的能力边界。
---

# Skills

## 概述

Skill 是 Claude Code 的扩展机制，每个 Skill 封装了特定领域的知识、工具与工作流。通过 `/skill-name` 即可调用，无需记忆复杂的 Prompt。

本目录系统性地收录和整理 Claude Code 内置 Skills 及社区/自定义 Skills，涵盖功能说明、触发条件、参数配置与使用示例，帮助团队快速检索和复用。

## Skills 目录

### 文档 & 内容

| Skill | 说明 |
| --- | --- |
| [doc-coauthoring](./doc-coauthoring.md) | 结构化协同撰写技术文档、提案、决策记录 |
| [docx](./docx.md) | Word 文档 (.docx) 的创建、读取、编辑与格式处理 |
| [pdf](./pdf.md) | PDF 文件的读取、合并、拆分、加水印、OCR 等操作 |
| [pptx](./pptx.md) | PowerPoint 演示文稿的创建、编辑与模板处理 |
| [xlsx](./xlsx.md) | Excel 电子表格的创建、公式计算、图表与数据清洗 |
| [internal-comms](./internal-comms.md) | 内部沟通文档写作：周报、公告、FAQ、事故报告等 |

### 设计 & 创意

| Skill | 说明 |
| --- | --- |
| [algorithmic-art](./algorithmic-art.md) | 基于 p5.js 的生成艺术创作，支持流场、粒子系统等 |
| [canvas-design](./canvas-design.md) | 静态视觉设计（海报、艺术品），输出 PNG/PDF |
| [frontend-design](./frontend-design.md) | 前端 UI 的美学指导：排版、配色、避免模板化设计 |
| [brand-guidelines](./brand-guidelines.md) | 应用 Anthropic 品牌色与字体到任意产出物 |
| [theme-factory](./theme-factory.md) | 为幻灯片/文档/页面等产出物套用或生成主题样式 |
| [slack-gif-creator](./slack-gif-creator.md) | 创建适配 Slack 的动画 GIF，含尺寸/时长校验 |
| [web-artifacts-builder](./web-artifacts-builder.md) | 构建复杂多组件 HTML Artifact（React + Tailwind + shadcn/ui） |

### 开发 & 集成

| Skill | 说明 |
| --- | --- |
| [claude-api](./claude-api.md) | Claude API / Anthropic SDK 参考：模型、定价、参数、流式、工具调用 |
| [mcp-builder](./mcp-builder.md) | 构建高质量 MCP Server，连接 LLM 与外部服务 |
| [skill-creator](./skill-creator.md) | 创建、修改、评估和优化自定义 Skill |
| [webapp-testing](./webapp-testing.md) | 使用 Playwright 对本地 Web 应用进行功能测试与调试 |

### Rspress 生态

| Skill | 说明 |
| --- | --- |
| [rspress-best-practices](./rspress-best-practices.md) | Rspress 配置、CLI、内容组织、frontmatter、主题、部署等最佳实践 |
| [rspress-custom-theme](./rspress-custom-theme.md) | 通过 CSS 变量、Layout 插槽、组件包裹等方式定制 Rspress 主题 |
| [rspress-description-generator](./rspress-description-generator.md) | 为 Rspress 文档批量生成和管理 description frontmatter |
| [rspress-v2-upgrade](./rspress-v2-upgrade.md) | Rspress v1 到 v2 的迁移指南与校验 |

### Claude Code 工作流

| Skill | 说明 |
| --- | --- |
| [code-review](./code-review.md) | 对当前 diff 进行代码审查，检查 Bug 与代码质量 |
| [simplify](./simplify.md) | 审查并自动修复代码中的冗余、复杂度与可维护性问题 |
| [verify](./verify.md) | 运行应用验证代码变更是否达到预期效果 |
| [review](./review.md) | 对 Pull Request 进行全面审查 |
| [security-review](./security-review.md) | 对当前分支变更进行安全审查 |
| [deep-research](./deep-research.md) | 多源深度调研：并行搜索 → 交叉验证 → 生成含引用的报告 |
| [loop](./loop.md) | 按间隔循环执行 Prompt 或 Slash Command |
| [run](./run.md) | 启动并驱动项目应用，确认变更在真实环境中生效 |
| [init](./init.md) | 为新项目初始化 CLAUDE.md 代码库文档 |

### 配置 & 工具

| Skill | 说明 |
| --- | --- |
| [update-config](./update-config.md) | 管理 Claude Code 的 settings.json 配置、权限、环境变量与 Hook |
| [keybindings-help](./keybindings-help.md) | 自定义键盘快捷键与组合键绑定 |
| [fewer-permission-prompts](./fewer-permission-prompts.md) | 扫描历史调用，生成权限白名单以减少交互式授权弹窗 |

### NoteStack 专属

| Skill | 说明 |
| --- | --- |
| [notestack-branding](./notestack-branding.md) | 重新生成或更新 NoteStack 品牌图片（favicon、logo、icon） |

### 社区 Skill

| Skill | 说明 |
| --- | --- |
| [codebase-to-course](./codebase-to-course.md) | 将任意代码仓库转化为自包含的交互式 HTML 课程，专为 Vibe Coder 设计（4.7k+ Stars） |

## Skill 文档规范

每个 Skill 的独立文档应遵循以下结构（参考 [_template.md](./_template.md)）：

1. **元信息** — 名称、分类、触发方式
2. **概述** — 一句话描述核心功能
3. **触发条件** — 什么场景下应调用该 Skill
4. **参数说明** — 支持的参数及其含义
5. **使用示例** — 实际可运行的调用示例
6. **最佳实践** — 高效使用该 Skill 的建议
7. **注意事项** — 已知限制与常见误区
8. **参考资源** — 官方文档、源码、相关 Skill

## 自定义 Skill

除了 Claude Code 内置 Skills，你也可以创建项目级或用户级自定义 Skill。详见 [skill-creator](./skill-creator.md)。

自定义 Skill 存放在：

- **项目级**：`.claude/skills/`（随仓库共享）
- **用户级**：`~/.claude/skills/`（个人使用）

## 参考资源

- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Skills 概览](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Skill Creator 使用指南](https://docs.anthropic.com/en/docs/claude-code/skills/creating)
