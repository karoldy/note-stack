---
description: DataLoader 批量加载实战 — 解决 GraphQL N+1 问题，使用 NestJS REQUEST 作用域 Service 封装 DataLoader，实现请求内批量合并、自动去重与级缓存。
---

# DataLoader 批量加载

## 概述

DataLoader 是 Facebook 开源的通用数据加载工具，解决 GraphQL [[n-plus-one|N+1 查询问题]]。核心机制：同一个事件循环帧内的多次 `.load(key)` 自动合并为一次批量查询，同时对相同 key 自动去重。

## 安装

```bash
pnpm add dataloader
```

## 架构选择

| 方案 | 实现 | 权衡 |
| --- | --- | --- |
| GraphQL Context | `context: () => ({ loader })` | 需手动管理每个 loader |
| **NestJS Service + REQUEST 作用域** | `@Injectable({ scope: Scope.REQUEST })` | 利用 DI，注入任意 Resolver，请求结束自动释放 |

REQUEST 作用域 Service 的优势：每个 GraphQL 请求自动创建新实例，DataLoader 缓存在请求内有效，不同请求的缓存互不污染。

## DataLoaderService 实现

```typescript
// src/dataloader/dataloader.service.ts
import { Injectable, Scope } from '@nestjs/common';
import DataLoader from 'dataloader';
import { PrismaService } from '../prisma/prisma.service';

@Injectable({ scope: Scope.REQUEST })
export class DataLoaderService {
  constructor(private readonly prisma: PrismaService) {}

  // 批量加载 Post：多个 authorId → 合并为 WHERE IN
  readonly postsByAuthorLoader = new DataLoader<number, PostRecord[]>(
    async (authorIds: readonly number[]) => {
      const posts = await this.prisma.post.findMany({
        where: { authorId: { in: [...authorIds] } },
      });

      // 按 authorId 分组，返回顺序必须与 keys 一致
      return authorIds.map((id) =>
        posts.filter((p) => p.authorId === id),
      );
    },
  );

  // 批量加载 User：多个 userId → 合并为 WHERE IN
  readonly userByIdLoader = new DataLoader<number, UserRecord | null>(
    async (userIds: readonly number[]) => {
      const users = await this.prisma.user.findMany({
        where: { id: { in: [...userIds] } },
      });

      const map = new Map(users.map((u) => [u.id, u]));
      return userIds.map((id) => map.get(id) ?? null);
    },
  );
}
```

## 模块注册（全局）

```typescript
// src/dataloader/dataloader.module.ts
import { Global, Module } from '@nestjs/common';

@Global()
@Module({
  providers: [DataLoaderService],
  exports: [DataLoaderService],
})
export class DataLoaderModule {}
```

## @ResolveField 中使用

### User → Posts（1:N）

```typescript
// src/user/user.resolver.ts
@ResolveField(() => [Post])
posts(@Parent() user: User) {
  return this.dataLoader.postsByAuthorLoader.load(user.id);
}
```

### Post → Author（N:1）

```typescript
// src/post/post.resolver.ts
@ResolveField(() => User)
author(@Parent() post: Post) {
  return this.dataLoader.userByIdLoader.load(post.authorId);
}
```

## 工作机制

```text
同一 GraphQL 请求的 event loop 帧内：

User 1 → postsLoader.load(1) ──┐
User 3 → postsLoader.load(3) ──┼── 收集全部 keys → 单次 SQL
User 4 → postsLoader.load(4) ──┘  WHERE authorId IN (1,3,4)

对比优化前：
  SELECT * FROM posts WHERE authorId = 1
  SELECT * FROM posts WHERE authorId = 3
  SELECT * FROM posts WHERE authorId = 4
优化后：
  SELECT * FROM posts WHERE authorId IN (1, 3, 4)
```

**三个关键特性**：

1. **批量合并** — 同一帧内所有 `.load(key)` 合并为一次 `IN` 查询
2. **自动去重** — 相同 key 仅查询一次（7 篇文章 → 3 个唯一 author ID → 3 次数据库查询）
3. **请求级缓存** — `scope: REQUEST` 确保不同请求的缓存互不污染，请求结束自动释放

## 与 Prisma 集成注意事项

Batch 函数返回值顺序必须与 keys 顺序严格一致：

```typescript
const map = new Map(users.map((u) => [u.id, u]));
return userIds.map((id) => map.get(id) ?? null);
```

DataLoader 依靠**索引匹配**将结果路由回对应的 `.load()` 调用者，顺序错乱会导致数据错位。

## AppModule 注册

```typescript
// src/app.module.ts
imports: [
  GraphQLModule.forRoot(...),
  PrismaModule,
  UserModule,
  PostModule,
  AuthModule,
  DataLoaderModule,  // @Global(), 全应用可用
],
```
