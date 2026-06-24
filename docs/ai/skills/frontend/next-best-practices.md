---
description: next-best-practices — Next.js 16 专用最佳实践 Skill，覆盖 RSC、Async API、路由设计、性能优化、PPR、缓存策略等核心主题。
---

# Next Best Practices

## 概述

`next-best-practices` 是社区维护的 Next.js 最佳实践 Skill，专注于 Next.js 16 和 AI SDK 6 生态。它覆盖 React Server Components（RSC）、Async API、路由设计、性能优化等核心主题，帮助开发者在 Next.js 项目中写出符合官方推荐模式的代码。该 Skill 来自 `laguagu/claude-code-nextjs-skills` 仓库，常与 [[vercel-react-best-practices]] 配合使用。

- **分类**：开发 & 集成
- **调用方式**：自动触发（编辑 Next.js 文件时）
- **来源**：社区

## 触发条件

以下场景应调用该 Skill：

- 创建或修改 Next.js App Router 页面和布局
- 实现 Server Components 与 Client Components 的边界划分
- 设计数据获取策略（Server Actions、Route Handlers）
- 配置路由、中间件、国际化
- 优化 Next.js 应用的构建与运行时性能
- 集成 AI SDK、pgvector、bun 等现代工具链

以下场景**不应**使用：

- 使用 Pages Router 的旧版 Next.js 项目（v12 及以下）
- 非 Next.js 框架（如 Remix、Astro、纯 React 项目）
- 通用 CSS/UI 问题（使用 [[frontend-design]]）

## 核心领域

| 领域 | 说明 |
| --- | --- |
| **RSC（React Server Components）** | Server/Client Component 拆分、`"use server"` / `"use client"` 边界 |
| **Async API** | `async` 组件、`use()` hook、Suspense 边界 |
| **Routing** | App Router 路由设计、Parallel Routes、Intercepting Routes |
| **Optimization** | 图片优化、字体加载、打包分析、ISR/SSG 策略 |
| **Cache Components & PPR** | 部分预渲染、增量静态再生策略 |
| **SEO** | Metadata API、Sitemap、JSON-LD 结构化数据 |

## 使用示例

### 安装

```bash
npx skills add laguagu/claude-code-nextjs-skills --skill next-best-practices
```

### 配套 Skills 安装

```bash
# 同时安装 SEO 和缓存相关 Skills
npx skills add laguagu/claude-code-nextjs-skills --skill cache-components
npx skills add laguagu/claude-code-nextjs-skills --skill nextjs-seo
```

## 最佳实践

- 在项目 `CLAUDE.md` 中明确标注使用的 Next.js 版本，确保 Skill 给出版本适配的建议
- 将 `next-best-practices` 与 [[vercel-react-best-practices]] 搭配使用，覆盖 React 通用 + Next.js 专用场景
- 使用 Server Components 作为默认选择，仅在需要交互性时添加 `"use client"`
- 利用 `nextjs-seo` 子 Skill 为每个页面生成规范的 Metadata

## 注意事项

- 该 Skill 面向 Next.js 16+ 和 AI SDK 6，旧版本项目部分规则可能不兼容
- App Router 与 Pages Router 的实践差异较大，确保项目已迁移至 App Router
- 部分高级特性（PPR、Cache Components）尚处于实验阶段，生产环境需评估稳定性

## 相关 Skills

- [[vercel-react-best-practices]] — React 通用性能优化
- [[web-quality]] — Web 质量审计（Lighthouse）
- [[frontend-design]] — 视觉设计与 UI 实现

## 参考资源

- [GitHub 仓库](https://github.com/laguagu/claude-code-nextjs-skills)
- [Next.js 官方文档](https://nextjs.org/docs)
- [React Server Components 指南](https://react.dev/reference/rsc/server-components)
