---
description: NestJS Code First 方式构建 GraphQL API — 从安装 @nestjs/graphql + Apollo Server 5 到 Resolver 实现，附 6 个踩坑记录与最终可用配置。
---

# GraphQL Code First

## 概述

NestJS 提供两种 GraphQL Schema 构建方式：**Code First** 和 Schema First。Code First 方式通过 TypeScript 装饰器定义类型，自动生成 `schema.gql`，无需手写 SDL。本文基于 **NestJS GraphQL 13 + Apollo Server 5 + graphql v16** 的实战配置。

## 安装

```bash
pnpm add @nestjs/graphql @nestjs/apollo @apollo/server graphql@^16.11.0
```

### 版本参考

| 包 | 版本 | 用途 |
| --- | --- | --- |
| `@nestjs/graphql` | 13.4.2 | NestJS GraphQL 模块 |
| `@nestjs/apollo` | 13.4.2 | Apollo 驱动适配器 |
| `@apollo/server` | 5.5.1 | Apollo Server 5 引擎 |
| `graphql` | 16.14.2 | GraphQL 核心 |
| `@as-integrations/express5` | 1.1.2 | Apollo Server 5 ↔ Express 桥接 |
| `class-validator` | 0.15.1 | DTO 校验装饰器 |
| `class-transformer` | 0.5.1 | DTO 类型转换 |

## 踩坑记录

### 错误 1：graphql v17 不兼容

**现象**：安装 `graphql` 默认拉取 v17.0.1，报 peer dependency 警告。

**根因**：graphql 17 是 2026 年最新版，NestJS GraphQL 生态尚未适配。

**解决**：锁定 v16

```bash
pnpm add graphql@^16.11.0
```

### 错误 2：Apollo Server 5 缺少 Express 桥接包

**现象**：启动报 `The "@as-integrations/express5" package is missing.`

**根因**：Apollo Server 5 将 Express/Koa/Fastify 集成拆分为独立包。

**解决**：

```bash
pnpm add @as-integrations/express5
```

### 错误 3：类属性初始化编译错误

**现象**：`TS2564: Property has no initializer`

**根因**：`@ObjectType()` / `@InputType()` 通过装饰器赋值，TypeScript 无法感知。

**解决**：在 `tsconfig.json` 中关闭严格属性初始化检查：

```json
{
  "compilerOptions": {
    "strictPropertyInitialization": false
  }
}
```

### 错误 4：TypeScript 6 `baseUrl` 已废弃

**现象**：`TS5101: Option 'baseUrl' is deprecated`

**解决**：移除 `baseUrl`，`paths` 中使用 `./` 前缀 `"@/*": ["./src/*"]`

### 错误 5：class-validator 未安装

**现象**：`TS2307: Cannot find module 'class-validator'`

**解决**：

```bash
pnpm add class-validator class-transformer
```

### 错误 6：浏览器访问 /graphql 显示 JSON 错误

**现象**：浏览器打开 `http://localhost:3000/graphql` 返回 JSON 错误而非 Playground。

```text
"GraphQL operations must contain a non-empty query or a persistedQuery extension."
```

**根因**：三层问题叠加：

1. **Apollo Server 代际差异**：AS3 内置 Playground → AS4 云端 Sandbox → AS5 云端嵌入
2. **@nestjs/apollo 对 AS5 处理缺陷**：`playground: true` 加载 AS4 Playground 插件（不兼容 AS5），`playground: false` 禁用全部着陆页
3. **AS5 的 `prefersHTML` 判断**：检查 `Accept` 头是否包含 `text/html`，curl 默认不包含

**解决**（三步组合）：

```typescript
// src/app.module.ts
import { ApolloServerPluginLandingPageLocalDefault } from '@apollo/server/plugin/landingPage/default';

GraphQLModule.forRoot<ApolloDriverConfig>({
  driver: ApolloDriver,
  autoSchemaFile: join(process.cwd(), 'schema.gql'),
  sortSchema: true,
  playground: false,       // 阻止不兼容的 AS4 Playground 插件
  csrfPrevention: false,   // 允许浏览器 GET /graphql
  plugins: [
    ApolloServerPluginLandingPageLocalDefault(),  // AS5 内置 Sandbox
  ],
}),
```

> **验证**：浏览器打开 `http://localhost:3000/graphql` 显示 Apollo Sandbox。curl 需加 `-H "Accept: text/html"`。

## 最终配置

```typescript
// src/app.module.ts
import { Module } from '@nestjs/common';
import { GraphQLModule } from '@nestjs/graphql';
import { ApolloDriver, ApolloDriverConfig } from '@nestjs/apollo';
import { ApolloServerPluginLandingPageLocalDefault } from '@apollo/server/plugin/landingPage/default';
import { join } from 'path';

@Module({
  imports: [
    GraphQLModule.forRoot<ApolloDriverConfig>({
      driver: ApolloDriver,
      autoSchemaFile: join(process.cwd(), 'schema.gql'),
      sortSchema: true,
      playground: false,
      csrfPrevention: false,
      plugins: [ApolloServerPluginLandingPageLocalDefault()],
    }),
  ],
})
export class AppModule {}
```

## 实体定义

```typescript
// src/user/entities/user.entity.ts
import { ObjectType, Field, Int } from '@nestjs/graphql';

@ObjectType()
export class User {
  @Field(() => Int)
  id: number;

  @Field()
  name: string;

  @Field()
  email: string;

  @Field()
  createdAt: string;

  @Field()
  updatedAt: string;
}
```

## Resolver 实现

```typescript
// src/user/user.resolver.ts
import { Resolver, Query, Mutation, Args, Int } from '@nestjs/graphql';

@Resolver(() => User)
export class UserResolver {
  constructor(private readonly userService: UserService) {}

  @Query(() => [User], { name: 'users' })
  findAll() {
    return this.userService.findAll();
  }

  @Query(() => User, { name: 'user' })
  findOne(@Args('id', { type: () => Int }) id: number) {
    return this.userService.findOne(id);
  }

  @Mutation(() => User)
  createUser(@Args('input') input: CreateUserInput) {
    return this.userService.create(input);
  }

  @Mutation(() => User)
  updateUser(@Args('input') input: UpdateUserInput) {
    return this.userService.update(input);
  }

  @Mutation(() => User)
  deleteUser(@Args('id', { type: () => Int }) id: number) {
    return this.userService.delete(id);
  }
}
```

## 全局启用 ValidationPipe

```typescript
// src/main.ts
import 'dotenv/config';
import { ValidationPipe } from '@nestjs/common';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(new ValidationPipe());
  await app.listen(3000);
}
bootstrap();
```

## 访问 GraphQL Endpoint

| 方式 | 说明 |
| --- | --- |
| 浏览器 | `http://localhost:3000/graphql` → Apollo Sandbox |
| curl Query | `curl -X POST /graphql -H "Content-Type: application/json" -d '{"query":"{ users { id name } }"}'` |
| curl Mutation | `curl -X POST /graphql -H "Content-Type: application/json" -d '{"query":"mutation { createUser(...) { id } }"}'` |

> `GET /graphql` 需要 `Accept: text/html` 头才返回 Sandbox 页面，API 调用务必用 `POST` + JSON。
