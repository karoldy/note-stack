---
description: tanstack-query-best-practices — TanStack Query v5 最佳实践 Skill，覆盖 32 条规则、10 大类别，涵盖 Query Keys、缓存策略、Mutations、预取、无限查询、SSR、乐观更新等核心主题。
---

# TanStack Query Best Practices

## 概述

`tanstack-query-best-practices` 是社区维护的 TanStack Query v5 最佳实践 Skill（来自 `deckardger/tanstack-agent-skills` 等仓库）。它包含 **32 条规则、10 大类别**，覆盖从基础 Query Keys 设计到高级 SSR 集成的全方位指导。每条规则包含解释、反模式示例、推荐实现和上下文建议。另有 `oakoss/agent-skills` 和 `@spardutti/claude-skills` 等社区仓库也提供 TanStack Query 专项 Skill。

- **分类**：开发 & 集成
- **调用方式**：自动触发（使用 `useQuery` / `useMutation` 等 API 时）
- **来源**：社区

## 触发条件

以下场景应调用该 Skill：

- 编写 `useQuery`、`useMutation`、`useInfiniteQuery` 等 Hook
- 设计 Query Key 工厂和管理策略
- 实现乐观更新（Optimistic Updates）
- 配置缓存失效（Invalidation）和垃圾回收（GC）
- 实现无限滚动加载
- SSR/SSG 场景下的数据预取与脱水/注水
- 从 TanStack Query v4 迁移到 v5
- 编写自定义 Query Client 配置

以下场景**不应**使用：

- 使用 SWR、React Query v3、Apollo Client 等其他数据请求库
- 简单的 `fetch` + `useState` / `useEffect` 模式
- 后端 API 设计（仅涉及前端数据获取层）

## 规则体系

| 类别 | 规则数 | 说明 |
| --- | --- | --- |
| **Query Keys** | 4 | Key 结构设计、工厂模式、层级化管理 |
| **Caching Strategies** | 4 | `staleTime` vs `gcTime`、缓存持久化 |
| **Mutations** | 4 | `useMutation`、乐观更新、错误回滚 |
| **Error Handling** | 3 | 全局错误处理、重试策略、错误边界 |
| **Prefetching** | 3 | `prefetchQuery`、Hover 预取、路由预加载 |
| **Infinite Queries** | 3 | `useInfiniteQuery`、游标分页、双向无限滚动 |
| **SSR Integration** | 3 | `HydrationBoundary`、`dehydrate`/`hydrate` |
| **Parallel Queries** | 2 | `useQueries`、依赖查询 |
| **Performance** | 3 | `select` 转换、结构性共享、背景刷新 |
| **Offline Support** | 3 | 离线队列、持久化、网络状态感知 |

## 使用示例

### 安装

```bash
npx skills add deckardger/tanstack-agent-skills --skill tanstack-query-best-practices
```

### Query Key 工厂模式

```typescript
// queryKeys.ts
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
};
```

### 乐观更新

```typescript
const mutation = useMutation({
  mutationFn: updateUser,
  onMutate: async (newUser) => {
    // 取消进行中的查询
    await queryClient.cancelQueries({ queryKey: userKeys.detail(newUser.id) });

    // 保存快照用于回滚
    const previousUser = queryClient.getQueryData(userKeys.detail(newUser.id));

    // 乐观更新
    queryClient.setQueryData(userKeys.detail(newUser.id), newUser);

    return { previousUser };
  },
  onError: (err, newUser, context) => {
    // 回滚
    queryClient.setQueryData(userKeys.detail(newUser.id), context?.previousUser);
  },
  onSettled: (data) => {
    // 重新获取最新数据
    queryClient.invalidateQueries({ queryKey: userKeys.detail(data.id) });
  },
});
```

## 最佳实践

- **Query Key 工厂模式**：集中管理 Key 结构，避免硬编码字符串分散在各组件
- **`staleTime` > `gcTime`**：设置合理的 `staleTime`（默认 0）和 `gcTime`（默认 5 分钟）
- **乐观更新**：对已知结果的操作（如 toggle、排序拖拽）使用乐观更新提升体感速度
- **SSR 脱水/注水**：服务端使用 `dehydrate(queryClient)`，客户端用 `HydrationBoundary` 接收
- **使用 `select`**：在 `useQuery` 中用 `select` 做数据转换，利用结构性共享避免不必要的重渲染

## 注意事项

- TanStack Query v5 的 API 与 v4 有破坏性变更（如 `cacheTime` → `gcTime`），迁移前查阅官方迁移指南
- 不要在 `useEffect` 中手动触发查询 — 使用 `enabled` 选项控制查询启用条件
- 乐观更新应始终实现 `onError` 回滚逻辑，否则失败后 UI 将显示错误数据
- `staleTime` 设置为 `Infinity` 时，数据永远不会过期，适用于静态资源请求

## 相关 Skills

- [[vercel-react-best-practices]] — React 客户端数据获取优化
- [[next-best-practices]] — Next.js SSR 数据获取策略
- [[react-doctor]] — React Hook 质量检查

## 参考资源

- [deckardger/tanstack-agent-skills](https://github.com/deckardger/tanstack-agent-skills)
- [oakoss/agent-skills](https://github.com/oakoss/agent-skills)
- [TanStack Query v5 官方文档](https://tanstack.com/query/v5)
- [TKDodo's Blog（TanStack Query 维护者）](https://tkdodo.eu/blog/practical-react-query)
