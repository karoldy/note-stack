---
description: GraphQL N+1 查询问题详解 — 从嵌套查询的 SQL 执行日志入手，分析问题根因与后果，为 DataLoader 方案做知识铺垫。
---

# N+1 查询问题

## 概述

N+1 是 GraphQL 中最经典的性能陷阱：查询 N 个父对象时，每个父对象的关联子字段再发起一次独立查询，导致数据库请求次数从 1 爆炸为 1+N。

## 问题演示

### 正向查询：User → Posts（1:N）

```graphql
query {
  users {       # 1 次查询 → 返回 N 个 user
    name
    posts {     # N 次查询 → 每个 user 查一次 posts
      title
    }
  }
}
```

**SQL 执行日志**（假设 3 个 user）：

```sql
SELECT * FROM users;                     -- 1 次
SELECT * FROM posts WHERE authorId = 1;  -- User 1
SELECT * FROM posts WHERE authorId = 3;  -- User 3
SELECT * FROM posts WHERE authorId = 4;  -- User 4
                                         -- 总共：4 次
```

### 反向查询：Post → Author（N:1，含重复）

```graphql
query {
  posts {            # 1 次查询 → 返回 M 个 post
    title
    author {         # M 次查询 → 每个 post 查一次 author（含重复）
      name
    }
  }
}
```

**SQL 执行日志**（假设 7 个 post，3 个不同 author）：

```sql
SELECT * FROM posts;                     -- 1 次
SELECT * FROM users WHERE id = 1;        -- Post 1
SELECT * FROM users WHERE id = 3;        -- Post 3
SELECT * FROM users WHERE id = 3;        -- Post 4 (重复!)
SELECT * FROM users WHERE id = 3;        -- Post 5 (重复!)
SELECT * FROM users WHERE id = 3;        -- Post 6 (重复!)
SELECT * FROM users WHERE id = 4;        -- Post 7
SELECT * FROM users WHERE id = 4;        -- Post 8 (重复!)
                                         -- 总共：8 次（1+7，含 5 次重复查询）
```

## 后果

- **数据库连接压力**随嵌套深度指数增长
- **响应时间**线性增加（每次查询的 I/O 延迟累加）
- **重复查询**浪费数据库缓存和网络 I/O

## 根因

GraphQL 的 `@ResolveField` 执行模型：每个父对象独立调用一次 Resolver，没有批量处理机制。默认实现如下：

```typescript
// 默认的 @ResolveField — 每个 user 执行一次 prisma 查询
@ResolveField(() => [Post])
async posts(@Parent() user: User) {
  return this.prisma.post.findMany({
    where: { authorId: user.id },  // N 次
  });
}
```

## 解决方案

使用 [[dataloader|DataLoader]] 将 N 次查询合并为 1 次 `WHERE IN` 查询。
