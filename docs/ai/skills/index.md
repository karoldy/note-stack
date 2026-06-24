---
description: Claude Code Skills 技能库 — 收录官方及社区 Skill 的用途、触发方式与最佳实践，帮助开发者高效利用 Slash Command 扩展 Claude Code 的能力边界。
---

# Skills

## 概述

Skill 是 Claude Code 的扩展机制，每个 Skill 封装了特定领域的知识、工具与工作流。通过 `/skill-name` 即可调用，无需记忆复杂的 Prompt。

本目录系统性收录 Claude Code 内置 Skills 及社区 Skills，涵盖功能说明、触发条件与使用示例。

## Skills 目录

| Skill | 说明 |
| --- | --- |
| [Claude API 参考](./claude-api.md) | Claude API / Anthropic SDK 参考：模型、定价、参数、流式、工具调用 |
| [代码仓库转课程](./codebase-to-course.md) | 将任意代码仓库转化为自包含的交互式 HTML 课程，专为 Vibe Coder 设计（4.7k+ Stars） |

## Skill 文档规范

每个 Skill 的独立文档应遵循以下结构（参考 `_template.md` 模板文件）：

1. **元信息** — 名称、分类、触发方式
2. **概述** — 一句话描述核心功能
3. **触发条件** — 什么场景下应调用该 Skill
4. **参数说明** — 支持的参数及其含义
5. **使用示例** — 实际可运行的调用示例
6. **最佳实践** — 高效使用该 Skill 的建议
7. **注意事项** — 已知限制与常见误区
8. **参考资源** — 官方文档、源码、相关 Skill

## 自定义 Skill

除了 Claude Code 内置 Skills，你也可以创建项目级或用户级自定义 Skill。自定义 Skill 存放在：

- **项目级**：`.claude/skills/`（随仓库共享）
- **用户级**：`~/.claude/skills/`（个人使用）

## 参考资源

- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Skills 概览](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Skill Creator 使用指南](https://docs.anthropic.com/en/docs/claude-code/skills/creating)
