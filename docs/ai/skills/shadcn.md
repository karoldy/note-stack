---
description: shadcn — shadcn/ui 生态的 Claude Code Skill 合集，包括组件安装、主题生成、代码审计（shadcn/improve）、无障碍与性能优化等专业 Agent。
---

# shadcn

## 概述

`shadcn` 是 shadcn/ui 生态下的 Claude Code Skill/Agent 集合，核心是 **`shadcn/improve`** — 由 shadcn 本人打造，使用昂贵模型审计代码库、生成优化计划，再由廉价模型执行修复。此外还包括组件安装、主题生成、无障碍审计、性能优化、表单构建、Dashboard 架构等 12 个专业 Agent。该 Skill 生态在 GitHub 上拥有 6K+ Stars。

- **分类**：开发 & 集成
- **调用方式**：`/improve`（审计模式）、自动触发（组件相关场景）
- **来源**：社区（shadcn 官方）

## 触发条件

以下场景应调用该 Skill：

- 使用 shadcn/ui 组件库的项目开发
- 需要对现有代码进行全面质量审计（正确性、安全性、性能、测试）
- 从截图/URL 生成 shadcn/ui 主题
- 构建表单、Dashboard、数据表格等复杂 UI 场景
- MCP 模式下通过自然语言安装 shadcn 组件

以下场景**不应**使用：

- 不使用 shadcn/ui 的项目
- 简单的 CSS 样式调整（无需组件级 Skill）
- 非 React 项目（shadcn/ui 仅支持 React 生态）

## 核心能力

### shadcn/improve — 代码审计

跨 9 个维度审计代码质量，优先生成修复计划，然后逐步执行：

1. Correctness（正确性）
2. Security（安全性）
3. Performance（性能）
4. Tests（测试覆盖率）
5. Tech Debt（技术债务）
6. Accessibility（无障碍访问）
7. Bundle Size（打包体积）
8. Code Style（代码风格）
9. Architecture（架构设计）

### shadcn-installer — 多框架安装

支持 Next.js、Vite、Remix、Astro、Laravel 等框架的 shadcn/ui 初始化。

### shadcn-theming-specialist — 主题定制

CSS 变量管理、暗色模式、品牌色集成、主题生成。

## 使用示例

### 安装 shadcn/improve

```bash
npx skills add shadcn/improve
```

### 启动审计

```bash
/improve
```

### 生成主题

```bash
# 从截图生成主题
$clonecn --screenshot path/to/design.png

# 从 URL 抓取设计令牌
$clonecn --url https://example.com
```

### 通过 MCP 安装组件

在 `.mcp.json` 中配置：

```json
{
  "mcpServers": {
    "shadcn": {
      "command": "npx",
      "args": ["shadcn@latest", "mcp"]
    }
  }
}
```

然后在 Claude Code 中自然语言操作：

```
"帮我添加 button、dialog、card 组件"
"展示所有可用组件列表"
```

## 最佳实践

- 在 PR 合并前运行 `/improve` 审计，自动发现潜在问题
- 将 shadcn/ui 组件安装与 MCP Server 结合，通过对话即可完成组件添加
- 使用 `clonecn` 从设计稿快速生成主题，减少手动配置 CSS 变量
- 搭配 [[playwright-best-practices]] 对 shadcn 组件编写 E2E 测试

## 注意事项

- `shadcn/improve` 运行成本较高（使用高级模型审计），建议在关键节点使用而非每次 Commit
- shadcn/ui 组件依赖 Tailwind CSS，确保项目已正确配置 Tailwind
- MCP 模式需要 Node.js 环境的 `npx` 支持

## 相关 Skills

- [[frontend-design]] — Anthropic 官方的视觉设计方向指导
- [[react-doctor]] — React 代码质量扫描与修复
- [[playwright-best-practices]] — E2E 测试编写
- [[web-quality]] — Lighthouse 维度的质量审计

## 参考资源

- [shadcn/improve GitHub](https://github.com/shadcn/improve)
- [shadcn/ui 官方文档](https://ui.shadcn.com)
- [mozinator/code-agents-for-shadcn](https://github.com/mozinator/code-agents-for-shadcn)
- [clonecn 主题生成器](https://github.com/hunvreus/clonecn)
