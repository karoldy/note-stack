---
description: web-quality — Google Chrome 团队 Addy Osmani 出品的 Web 质量审计 Skill，基于 Lighthouse 与 Core Web Vitals，涵盖性能、无障碍、SEO、安全最佳实践等 6 项子 Skill。
---

# Web Quality

## 概述

`web-quality` 是 Google Chrome 团队的 Addy Osmani 发布的 Web 质量审计 Skill 集合（`addyosmani/web-quality-skills`）。它基于 **Lighthouse 评分体系**和 **Core Web Vitals** 标准，提供框架无关的全面质量审计能力。该 Skill 拆分为 6 个专项子模块，可按需加载，覆盖性能、无障碍访问、SEO、安全最佳实践等领域。

- **分类**：开发 & 集成
- **调用方式**：自动触发（关键词如 "audit"、"lighthouse"、"optimize"、"a11y"）
- **来源**：社区（Addy Osmani / Google Chrome）

## 触发条件

以下场景应调用该 Skill：

- 需要对项目进行全面的质量审计（性能、无障碍、SEO、最佳实践）
- 分析 Core Web Vitals 指标（LCP、INP、CLS）并优化
- 排查页面加载慢、交互延迟等性能问题
- 提升无障碍访问体验（WCAG 合规）
- 优化搜索引擎可见性（Meta Tags、结构化数据）
- 执行 Web 安全基线检查

以下场景**不应**使用：

- 框架特定的性能优化（使用 [[vercel-react-best-practices]] 或 [[next-best-practices]]）
- E2E 功能测试（使用 [[playwright-best-practices]]）
- UI 视觉设计问题（使用 [[frontend-design]]）

## 子 Skill 体系

| 子 Skill | 用途 | 触发关键词 |
| --- | --- | --- |
| `web-quality-audit` | 综合质量审计（性能、无障碍、SEO、最佳实践） | "audit", "quality review", "lighthouse" |
| `performance` | 加载速度优化 | "speed up", "optimize", "load time" |
| `core-web-vitals` | LCP、INP、CLS 专项优化 | "LCP", "INP", "CLS", "Core Web Vitals" |
| `accessibility` | WCAG 合规与无障碍修复 | "a11y", "WCAG", "accessible" |
| `seo` | 搜索引擎可见性、元标签、结构化数据 | "SEO", "meta tags", "search" |
| `best-practices` | 安全与现代最佳实践 | "security", "best practices", "modern" |

## 关键指标阈值

### Core Web Vitals（"Good" 评级）

| 指标 | 阈值 | 说明 |
| --- | --- | --- |
| **LCP**（Largest Contentful Paint） | ≤ 2.5s | 最大内容绘制时间 |
| **INP**（Interaction to Next Paint） | ≤ 200ms | 交互延迟 |
| **CLS**（Cumulative Layout Shift） | ≤ 0.1 | 累积布局偏移 |

### 性能预算

- 总资源体积 < 1.5 MB
- JavaScript < 300 KB
- CSS < 100 KB

### Lighthouse 目标分数

- Performance ≥ 90
- Accessibility: 100
- Best Practices ≥ 95
- SEO ≥ 95

## 使用示例

### 安装

```bash
# 安装综合审计工具
npx skills add https://github.com/addyosmani/web-quality-skills --skill web-quality-audit

# 安装专项模块
npx skills add https://github.com/addyosmani/web-quality-skills --skill performance
npx skills add https://github.com/addyosmani/web-quality-skills --skill core-web-vitals
npx skills add https://github.com/addyosmani/web-quality-skills --skill accessibility
```

### 执行审计

```bash
# 全面质量审计
/skills  # 确认 web-quality-audit 已加载
# 然后在对话中说："audit this page for quality"

# 专项性能检查
"check my Core Web Vitals scores and suggest optimizations"
```

## 最佳实践

- 在部署前运行 `web-quality-audit` 自动化质量门禁
- 结合 Chrome DevTools Performance 面板验证 Skill 的优化建议
- 使用 `accessibility` 子 Skill 确保达到 WCAG 2.1 AA 标准
- 将性能预算写入 `CLAUDE.md`，让 Skill 在开发过程中持续检查

## 注意事项

- 该 Skill 基于 Google Lighthouse 框架，建议配合实际 Lighthouse 报告交叉验证
- 部分优化建议（如 JavaScript 拆分）需要结合具体打包工具（Webpack、Rspack、Vite）实施
- SEO 建议需结合具体搜索引擎的最新算法调整

## 相关 Skills

- [[vercel-react-best-practices]] — React 专用性能优化
- [[next-best-practices]] — Next.js 框架最佳实践
- [[playwright-best-practices]] — E2E 测试与自动化验证
- [[shadcn]] — shadcn/ui 组件审计

## 参考资源

- [GitHub 仓库](https://github.com/addyosmani/web-quality-skills)
- [Core Web Vitals 官方文档](https://web.dev/vitals/)
- [Lighthouse 文档](https://developer.chrome.com/docs/lighthouse/)
