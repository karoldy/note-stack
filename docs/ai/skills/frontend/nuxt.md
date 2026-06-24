---
description: nuxt — Nuxt 4+ 开发最佳实践 Skill（onmax/nuxt-skills），涵盖 Server Routes、Middleware、Modules、NuxtHub、Nuxt Content、Nuxt UI、认证、SEO 等 19+ 子 Skill。
---

# Nuxt

## 概述

`nuxt` 是社区最全面的 Nuxt 开发 Skill 集合，主要维护于 **`onmax/nuxt-skills`**（19+ 子 Skill），同时 **`vinayakkulkarni/vue-nuxt-best-practices`** 也提供高质量的生产级 Nuxt 最佳实践。它覆盖 Nuxt 4+ 的新特性：`app/` 目录结构、Singleton 数据获取、浅层响应式、Server Routes、Middleware、Nuxt Modules 开发等。

- **分类**：开发 & 集成
- **调用方式**：自动触发（编辑 Nuxt 项目文件时）
- **来源**：社区

## 触发条件

以下场景应调用该 Skill：

- 创建或维护 Nuxt 4+ 项目
- 编写 Server Routes 和 API Endpoints
- 设计 Middleware 和路由守卫
- 使用 NuxtHub、Nuxt Content、Nuxt UI 等官方模块
- 实现认证流程（Nuxt Auth / Better Auth）
- SEO 优化（Meta Tags、Sitemap、JSON-LD）
- 从 Nuxt 3 迁移到 Nuxt 4

以下场景**不应**使用：

- Nuxt 2 或 Vue 2 项目
- 纯 Vue 3 项目（使用 [[vue]]）
- 非 Nuxt 框架的 SSR 方案

## 子 Skill 体系（onmax/nuxt-skills）

| 子 Skill | 内容 |
| --- | --- |
| `nuxt` | Server Routes、Routing、Middleware、Config |
| `nuxt-modules` | Nuxt Module 开发 |
| `nuxthub` | NuxtHub v0.10 集成 |
| `nuxt-content` | Nuxt Content v3 文档驱动 |
| `nuxt-ui` | Nuxt UI v4 组件库 |
| `nuxt-better-auth` | 认证模式与最佳实践 |
| `vue` | Vue 3 Composition API |
| `vueuse` | VueUse 工具库 |
| `motion` | 动画与过渡 |
| `tresjs` | 3D 场景 |
| `vitest` | 测试框架 |
| `vite` | 构建工具 |
| `pnpm` | 包管理器 |

## 使用示例

### 安装

```bash
# 安装完整的 onmax/nuxt-skills 套件
npx skills add onmax/nuxt-skills

# 安装 vue-nuxt-best-practices
npx skills add vinayakkulkarni/vue-nuxt-best-practices
```

### Nuxt 4 `app/` 目录结构

```
app/
├── app.vue                 # 根组件
├── pages/
│   └── index.vue           # 路由页面
├── components/
│   └── UserCard.vue        # 自动导入组件
├── composables/
│   └── useAuth.ts          # 自动导入 Composables
├── server/
│   ├── api/
│   │   └── users.get.ts    # Server Route
│   └── middleware/
│       └── auth.ts         # Server Middleware
├── middleware/
│   └── protected.ts        # Client Middleware
└── nuxt.config.ts
```

### Server Route 示例

```typescript
// server/api/users.get.ts
export default defineEventHandler(async (event) => {
  const { page = 1 } = getQuery(event);
  const users = await $fetch(`https://api.example.com/users?page=${page}`);
  return { data: users, page };
});
```

## 最佳实践

- 利用 Nuxt 的自动导入机制，避免手动 `import` 组件和 Composables
- Server Routes 用于处理 API 代理和数据库直连，避免在客户端暴露敏感逻辑
- 使用 `useAsyncData` 和 `useFetch` 进行数据获取，它们内置缓存和去重
- 搭配 [[vue]] 使用，确保 Vue 3 Composition API 的最佳实践在 Nuxt 中一致贯彻
- 关注 [nuxt/nuxt PR #33498](https://github.com/nuxt/nuxt/pull/33498) 官方 Skill 的发布进展

## 注意事项

- Nuxt 4 的 `app/` 目录结构是破坏性变更，Nuxt 3 项目需渐进式迁移
- Singleton 数据获取在 Nuxt 4 中是默认行为，注意与旧版 `useAsyncData` 的行为差异
- Nuxt Modules 的 Skill 建议仅用于模块开发者，应用开发者通常不需要

## 相关 Skills

- [[vue]] — Vue 3 基础开发规范
- [[web-quality]] — Web 质量审计
- [[frontend-design]] — 视觉设计
- [[playwright-best-practices]] — E2E 测试

## 参考资源

- [onmax/nuxt-skills](https://github.com/onmax/nuxt-skills)
- [vinayakkulkarni/vue-nuxt-best-practices](https://github.com/vinayakkulkarni/vue-nuxt-best-practices)
- [Nuxt 4 官方文档](https://nuxt.com)
- [官方 Skill PR #33498](https://github.com/nuxt/nuxt/pull/33498)
