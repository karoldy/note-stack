---
description: Prisma ORM 在 NestJS 中的集成实践 — 封装 PrismaService 管理数据库连接生命周期，Docker Compose 本地 PostgreSQL，Prisma 7 构建脚本踩坑与解决方案。
---

# Prisma ORM 集成

## 概述

Prisma 7 是 Node.js 生态中类型安全、开发体验领先的 ORM。在 NestJS 中，通过封装 `PrismaService` 实现 `OnModuleInit` / `OnModuleDestroy` 生命周期管理，确保数据库连接在应用启动/关闭时正确初始化与释放。

## 安装

```bash
pnpm add @prisma/client @prisma/adapter-pg
pnpm add -D prisma dotenv
```

当前版本：**Prisma 7.8.0** / **@prisma/client 7.8.0** / **@prisma/adapter-pg 7.8.0**

## 踩坑记录

### 错误 1：Prisma 7 构建脚本被 pnpm 忽略

**现象**：安装 prisma 后警告：

```text
Ignored build scripts: @prisma/engines@7.8.0, prisma@7.8.0.
```

**根因**：pnpm v10 默认禁止未声明的构建脚本。

**解决**：在 `.npmrc` 中添加构建许可：

```ini
onlyBuiltDependencies[]=@prisma/engines
onlyBuiltDependencies[]=prisma
onlyBuiltDependencies[]=bcrypt
```

## PrismaService 封装

```typescript
// src/prisma/prisma.service.ts
import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService
  extends PrismaClient
  implements OnModuleInit, OnModuleDestroy
{
  async onModuleInit() {
    await this.$connect();
  }

  async onModuleDestroy() {
    await this.$disconnect();
  }
}
```

## PrismaModule

```typescript
// src/prisma/prisma.module.ts
import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
```

`@Global()` 装饰器使 PrismaService 在整个应用中无需在每个 Module 重复 imports。

## 数据库 Schema 示例

```prisma
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "client"
}

model User {
  id        Int      @id @default(autoincrement())
  name      String
  email     String   @unique
  password  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  posts Post[]
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  authorId  Int      @map("author_id")
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)
  createdAt DateTime @default(now())

  @@index([authorId])
}
```

## Docker Compose 本地 PostgreSQL

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: nest-graphql-lab
    ports:
      - '5432:5432'
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

## 常用命令

| 命令 | 说明 |
| --- | --- |
| `npx prisma generate` | 生成 Prisma Client，通常在 `postinstall` 钩子中自动执行 |
| `npx prisma migrate dev --name init` | 初始化数据库迁移 |
| `npx prisma migrate dev` | 自动生成增量迁移 |
| `npx prisma studio` | 打开 Prisma Studio 可视化数据库浏览器 |
| `npx prisma db seed` | 执行 `prisma/seed.ts` 填充种子数据 |

## 数据模型关系设计

### User ↔ Post（1:N）

```prisma
model User {
  id    Int    @id @default(autoincrement())
  posts Post[]
}

model Post {
  id       Int  @id @default(autoincrement())
  authorId Int  @map("author_id")
  author   User @relation(fields: [authorId], references: [id], onDelete: Cascade)
}
```

### User ↔ RefreshToken（1:N）

```prisma
model User {
  id            Int            @id @default(autoincrement())
  refreshTokens RefreshToken[]
}

model RefreshToken {
  id     String @id @default(uuid())
  userId Int    @map("user_id")
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
}
```

## 最佳实践

- 封装 `PrismaService` 实现生命周期接口，确保 `$connect()` / `$disconnect()` 被nestjs 的模块生命周期自动调用
- 使用 `@Global()` 注册 PrismaModule，避免在每个功能模块中重复导入
- 生产环境使用 `migrate deploy`，开发环境使用 `migrate dev`
- 利用 `@map()` 和 `@@map()` 使 Prisma 字段名（camelCase）与数据库列名（snake_case）保持独立
