---
description: vercel-react-best-practices — Vercel 官方出品的 React/Next.js 性能优化 Skill，涵盖 40+ 条规则，覆盖瀑布请求消除、打包体积优化、SSR 性能、客户端数据获取与重渲染优化等 8 大类别。
---

# Vercel React Best Practices

## 概述

`vercel-react-best-practices` 是 Vercel Labs 官方发布的 Agent Skill，提供 React 与 Next.js 性能优化的最佳实践指南。它包含 **40+ 条优化规则**，按优先级分为 8 大类别，从消除数据瀑布到高级渲染模式全覆盖。该 Skill 在 Claude Code 生态中安装量最高，被社区广泛验证可显著减少 React 代码 Bug（约 40%）并改善页面加载速度（平均 600ms 提升）。

- **分类**：开发 & 集成
- **调用方式**：自动触发（编辑 React/Next.js 文件时）
- **来源**：社区（Vercel Labs）

## 触发条件

以下场景应调用该 Skill：

- 编写或修改 React 组件、Next.js 页面
- 遇到首屏加载慢、交互延迟等性能问题
- 需要优化 `useEffect`、`useMemo`、数据请求模式
- Code Review 中需要检查 React 反模式
- 新项目初始化时建立性能基线

以下场景**不应**使用：

- 非 React 框架项目（Vue、Angular、Svelte）
- 纯后端 Node.js 代码
- CSS 样式调整（使用 [[frontend-design]]）

## 规则体系

按优先级从高到低排列的 8 大类别：

| 优先级 | 类别 | 影响级别 |
| --- | --- | --- |
| 1 | Eliminating Waterfalls（消除请求瀑布） | CRITICAL |
| 2 | Bundle Size Optimization（打包体积优化） | CRITICAL |
| 3 | Server-Side Performance（服务端性能） | HIGH |
| 4 | Client-Side Data Fetching（客户端数据获取） | MEDIUM-HIGH |
| 5 | Re-render Optimization（重渲染优化） | MEDIUM |
| 6 | Rendering Performance（渲染性能） | MEDIUM |
| 7 | JavaScript Performance（JS 性能） | LOW-MEDIUM |
| 8 | Advanced Patterns（高级模式） | LOW |

## 使用示例

### 安装

```bash
npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices
```

或使用简写：

```bash
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices
```

### 验证安装

```bash
/skills
```

## 最佳实践

- 将该 Skill 与 `vercel-composition-patterns` 和 [[frontend-design]] 搭配使用，获得完整的 Vercel 前端开发体验
- 在新项目初始化阶段就安装该 Skill，从源头避免性能反模式
- 结合 Lighthouse 和 Web Vitals 监控工具验证优化效果
- 关注 Skill 更新 — Vercel 团队会根据 React/Next.js 新版本持续更新规则

## 注意事项

- 该 Skill 包含大量规则文件，建议通过目录结构按需加载，避免全量注入上下文窗口
- 部分规则（如高级模式）可能不适用于所有项目规模，按实际场景选择性采纳
- 首次安装后可能需要运行 `npx skills update` 获取最新版本

## 相关 Skills

- [[web-quality]] — Google Lighthouse 维度的 Web 质量审计
- [[frontend-design]] — Anthropic 官方的视觉设计 Skill
- [[next-best-practices]] — Next.js 框架专用最佳实践

## 参考资源

- [GitHub 仓库](https://github.com/vercel-labs/agent-skills)
- [Agent Skills 官方文档](https://examples.vercel.com/docs/agent-resources/skills)
- [SkillsMP 市场页](https://skillsmp.com/skills/fcakyon-claude-codex-settings-plugins-react-skills-skills-react-best-practices-skill-md)
