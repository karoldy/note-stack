---
description: svelte-code-writer — Svelte 官方维护的 Svelte 5 代码编写 Skill（sveltejs/ai-tools），提供 Svelte 5 Runes 语法、组件编写、文档查询与代码分析能力。
---

# Svelte Code Writer

## 概述

`svelte-code-writer` 是 **Svelte 官方团队**维护的 Claude Code Skill（`sveltejs/ai-tools`），专为 Svelte 5 的 Runes 语法（`$state`、`$derived`、`$effect`）设计。它必须用于创建、编辑或分析任何 `.svelte` 组件和 `.svelte.ts` / `.svelte.js` 模块文件，是 Svelte 开发的核心辅助工具。

- **分类**：开发 & 集成
- **调用方式**：自动触发（编辑 `.svelte` / `.svelte.ts` / `.svelte.js` 文件时）
- **来源**：社区（Svelte 官方）

## 触发条件

以下场景**必须**调用该 Skill：

- 创建或编辑 `.svelte` 单文件组件
- 编写 `.svelte.ts` 或 `.svelte.js` 模块
- 使用 Svelte 5 Runes（`$state`、`$derived`、`$effect`、`$props`）
- 查询 Svelte 5 API 文档
- 从 Svelte 4 迁移到 Svelte 5
- 分析 Svelte 组件的性能或兼容性问题

以下场景**不应**使用：

- Svelte 4 的旧语法（`let`、`export let`）— 建议先迁移至 Svelte 5
- 非 Svelte 框架项目
- 纯 HTML/CSS/JS 无框架页面

## 核心能力

### Svelte 5 Runes 支持

```svelte
<script>
  // $state — 响应式状态
  let count = $state(0);

  // $derived — 派生值
  let doubled = $derived(count * 2);

  // $effect — 副作用
  $effect(() => {
    console.log(`Count is now ${count}`);
  });

  // $props — 组件属性
  let { name, age = 18 } = $props();
</script>

<h1>Hello {name}</h1>
<p>Age: {age}, Doubled: {doubled}</p>
<button onclick={() => count++}>Increment</button>
```

### 文档查询

```bash
# 查询 Svelte 5 API
npx svelte-doc $state
npx svelte-doc $derived
```

### 代码分析

自动检测 Svelte 4 与 Svelte 5 的兼容性问题，并提供迁移建议。

## 使用示例

### 安装

```bash
# 方法 1：Claude Code 插件市场
/plugin marketplace add sveltejs/ai-tools
/plugin install svelte

# 方法 2：npm Skills 安装器
npx skills add sveltejs/ai-tools --skill svelte-code-writer
```

### 推荐用法

官方建议在 `svelte-file-editor` 子代理中执行，以获得最佳效果：

```
"使用 svelte-file-editor 代理修改 src/lib/UserCard.svelte"
```

## 最佳实践

- 所有 Svelte 文件编辑操作应在 `svelte-file-editor` 子代理中进行
- 优先使用 Runes 语法，避免遗留的 Svelte 4 模式（`export let`、`onMount`）
- 利用 `$state` 的深层响应性减少不必要的 `$derived` 调用
- 结合 SvelteKit 使用时，关注服务端/客户端代码边界

## 注意事项

- 该 Skill 仅支持 Svelte 5 语法，Svelte 4 项目会收到迁移提示
- 建议与 Svelte 官方 VSCode 扩展配合使用，获得语法高亮和实时错误提示
- Runes 语法在 `.svelte.js` / `.svelte.ts` 文件中的行为与 `.svelte` 组件略有不同

## 相关 Skills

- [[frontend-design]] — 视觉设计（可用于 Svelte 组件的 UI 美化）
- [[frontend-ui-engineering]] — UI 工程化落地

## 参考资源

- [sveltejs/ai-tools GitHub](https://github.com/sveltejs/ai-tools)
- [Svelte 5 官方文档](https://svelte.dev/docs)
- [Svelte AI Docs](https://svelte.dev/docs/ai/skills)
- [Svelte Claude Code 插件文档](https://svelte.dev/docs/ai/claude-plugin)
