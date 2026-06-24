---
description: react-doctor — Million.js 团队出品的 React 代码质量扫描工具，11K+ Stars，确定性扫描状态/Effect、性能、架构、安全、无障碍 5 大维度，支持 CI 集成与自动化修复。
---

# React Doctor

## 概述

`react-doctor` 是 Million.js 团队（`millionco/react-doctor`）发布的 React 代码质量扫描工具，在 GitHub 上获得 **11K+ Stars**。与依赖 LLM 判断的审查工具不同，它通过**确定性规则扫描** React 代码库，发现状态管理、性能、架构、安全、无障碍等维度的问题。口号是："Your agent writes bad React. This catches it." — 它是 AI 编码代理的安全网，在代码提交前捕获常见的 React 反模式。

- **分类**：开发 & 集成
- **调用方式**：`npx react-doctor@latest`（CLI）/ 自动触发（Skill 模式）
- **来源**：社区（Million.js）

## 触发条件

以下场景应调用该 Skill：

- AI 生成了 React 组件代码，需要自动检查质量
- PR Review 中需要自动化 React 最佳实践检查
- 新成员加入团队，需要统一 React 编码规范
- 从 JavaScript 迁移到 TypeScript 后的 React 代码审查
- CI 流水线中需要 React 专项质量门禁

以下场景**不应**使用：

- 非 React 框架项目（使用对应框架的工具）
- 后端 Node.js 逻辑检查
- CSS/样式问题（使用 [[frontend-design]] 或 stylelint）

## 扫描维度

| 维度 | 检查内容 |
| --- | --- |
| **State & Effects** | `useEffect` 依赖数组缺失、不必要的状态、状态提升不当、竞态条件 |
| **Performance** | 缺少 `useMemo`/`useCallback`、渲染次数过多、不必要的重渲染 |
| **Architecture** | 组件职责不清、Props Drilling 过深、Hook 使用违反规则 |
| **Security** | XSS 风险、危险的 `dangerouslySetInnerHTML`、不安全的数据渲染 |
| **Accessibility** | 缺少 ARIA 标签、键盘导航问题、语义化 HTML 缺失 |

## 使用示例

### 快速扫描（无需安装）

```bash
npx react-doctor@latest
```

### 安装为 Agent Skill

```bash
npx react-doctor@latest install
```

安装后 Skill 文件进入 `~/.claude/skills/`，Claude Code 在编辑 React 文件时自动触发检查。

### CI 集成（GitHub Actions）

```yaml
- name: React Doctor Check
  run: npx react-doctor@latest --reporter=github
```

### 输出示例

```
❌ src/components/UserProfile.tsx:23
   Missing dependency 'userId' in useEffect

⚠️  src/hooks/useFetchData.ts:15
   Unnecessary useMemo — value is a primitive

✅ src/components/Button.tsx
   All checks passed
```

## 最佳实践

- 在 `pre-commit` Hook 中运行 `react-doctor`，拦截低质量代码
- 与 [[vercel-react-best-practices]] 搭配使用：前者做确定性扫描，后者做上下文感知的优化建议
- 将 `react-doctor` 集成到 CI 流水线中作为质量门禁
- 扫描结果结合 [[shadcn]] 的 `/improve` 命令进行深度修复

## 注意事项

- `react-doctor` 是确定性工具，不会产生误报率极高的模糊建议 — 但如果规则过于严格，可通过配置排除特定规则
- 支持所有 React 框架/工具链：Next.js、Vite、TanStack、React Native、Expo
- 扫描速度很快（通常 < 5 秒），适合频繁运行

## 相关 Skills

- [[vercel-react-best-practices]] — React 性能优化最佳实践
- [[shadcn]] — shadcn/improve 深度代码审计
- [[next-best-practices]] — Next.js 专用最佳实践

## 参考资源

- [GitHub 仓库](https://github.com/millionco/react-doctor)
- [npm 包](https://www.npmjs.com/package/react-doctor)
- [Million.js 官网](https://million.dev)
