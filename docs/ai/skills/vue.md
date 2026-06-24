---
description: vue — Vue 3 开发最佳实践 Skill（vuejs-ai/skills），覆盖 Composition API、`<script setup>`、Pinia、Vue Router、Composables、JSX、测试等核心领域。
---

# Vue

## 概述

`vue` 是 Vue.js 社区维护的 Vue 3 开发 Skill，最权威的实现来自 **`vuejs-ai/skills`**。它覆盖 Vue 3 Composition API、`<script setup>` 语法、Pinia 状态管理、Vue Router 路由、Composables 设计、JSX 支持与测试策略。该 Skill 强制使用 `<script setup lang="ts">` 模式，拒绝 Options API，确保代码遵循 Vue 3 官方推荐风格。

- **分类**：开发 & 集成
- **调用方式**：自动触发（编辑 `.vue` / `.ts` 文件时）
- **来源**：社区（vuejs-ai）

## 触发条件

以下场景应调用该 Skill：

- 创建或修改 `.vue` 单文件组件
- 编写或重构 Composables
- 设计 Pinia Store
- 配置 Vue Router 路由
- 从 Vue 2 / Options API 迁移到 Vue 3
- 编写 Vue 组件测试（Vitest + Vue Test Utils）
- 集成 Nuxt 框架时（搭配 [[nuxt]]）

以下场景**不应**使用：

- Vue 2 或 Options API 项目（建议先迁移）
- 非 Vue 生态项目
- React/Angular/Svelte 开发

## 核心规范

### 组件结构（强制执行）

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

// Props & Emits
const props = defineProps<{
  title: string;
  count?: number;
}>();

const emit = defineEmits<{
  update: [value: number];
}>();

// Composables
const { data, loading } = useFetchData(props.title);

// Computed
const displayCount = computed(() => props.count ?? 0);

// Lifecycle
onMounted(() => {
  console.log('Component mounted');
});
</script>

<template>
  <div class="component">
    <h1>{{ title }}</h1>
    <p>{{ displayCount }}</p>
  </div>
</template>
```

### Composables 设计

```typescript
// composables/useFetchData.ts
import { ref, watchEffect } from 'vue';

export function useFetchData(key: string) {
  const data = ref<string | null>(null);
  const loading = ref(false);

  watchEffect(async () => {
    loading.value = true;
    data.value = await fetch(`/api/${key}`).then(r => r.json());
    loading.value = false;
  });

  return { data, loading };
}
```

## 使用示例

### 安装

```bash
npx skills add vuejs-ai/skills
```

### 进阶安装（含 Nuxt 生态）

```bash
# vue-claude-stack 提供更多生成命令
npx skills add mvtandas/vue-claude-stack

# 包含的命令：
# /generate-component  — 生成 Vue 组件
# /generate-composable — 生成 Composable
# /generate-store      — 生成 Pinia Store
# /generate-test       — 生成测试文件
# /generate-api        — 生成 API 调用层
```

## 最佳实践

- 始终使用 `<script setup lang="ts">` — 不使用 Options API
- 将可复用逻辑提取为 Composables，文件放在 `composables/` 目录
- Pinia Store 使用 Composition API 风格（`defineStore` 的 setup 语法）
- 使用 `defineProps<T>()` 和 `defineEmits<T>()` 获得完整的 TypeScript 类型推断
- 搭配 [[nuxt]] 使用时，注意 Server/Client 代码边界

## 注意事项

- 该 Skill 假定使用 TypeScript，纯 JavaScript 项目会收到迁移建议
- Composables 中的 `watchEffect` 会在组件卸载时自动清理，无需手动 `onUnmounted`
- 避免在 `<script setup>` 中直接使用 `async/await` 顶层代码（会导致组件挂起），使用 Suspense 包裹

## 相关 Skills

- [[nuxt]] — Nuxt 4+ 框架最佳实践
- [[frontend-design]] — Vue 组件的视觉美化
- [[playwright-best-practices]] — Vue 应用的 E2E 测试

## 参考资源

- [vuejs-ai/skills GitHub](https://github.com/vuejs-ai/skills)
- [Vue 3 官方文档](https://vuejs.org)
- [mvtandas/vue-claude-stack](https://github.com/mvtandas/vue-claude-stack)
- [vinayakkulkarni/vue-nuxt-best-practices](https://github.com/vinayakkulkarni/vue-nuxt-best-practices)
