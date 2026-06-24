---
description: NestJS 应用的 Docker 多阶段构建与 Docker Compose 编排 — 分离 Build 与 Production 阶段，利用 pnpm layer caching 加速镜像构建，附带 PostgreSQL 服务编排。
---

# Docker 部署

## 概述

NestJS 应用适合使用 **多阶段构建（Multi-stage Build）** 打包为轻量 Docker 镜像。Build 阶段完成依赖安装和 TypeScript 编译，Production 阶段仅包含运行时必需文件，有效减小镜像体积。

## Dockerfile（多阶段构建）

```dockerfile
# ─── Build Stage ───────────────────────────────────────
FROM node:22-alpine AS builder

RUN corepack enable && corepack prepare pnpm@latest --activate
WORKDIR /app

# 层缓存优化：先装依赖
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# 复制源码 + Prisma schema
COPY tsconfig.json nest-cli.json ./
COPY src/ ./src/
COPY prisma/ ./prisma/

RUN npx prisma generate    # 生成 Prisma Client
RUN pnpm build             # 编译 NestJS → dist/

# ─── Production Stage ───────────────────────────────────
FROM node:22-alpine AS production

RUN corepack enable && corepack prepare pnpm@latest --activate
WORKDIR /app

# 仅安装生产依赖（不含 devDependencies）
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile --prod

# 复制构建产物
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules/.prisma ./node_modules/.prisma
COPY prisma/ ./prisma/

EXPOSE 3000

CMD ["node", "dist/main"]
```

## Docker Compose（PostgreSQL + App）

```yaml
# docker-compose.yml
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

  app:
    build: .
    ports:
      - '3000:3000'
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/nest-graphql-lab?schema=public
      JWT_SECRET: ${JWT_SECRET:-dev-secret}
    depends_on:
      - postgres

volumes:
  pgdata:
```

## 关键优化点

| 策略 | 说明 |
| --- | --- |
| **COPY 分层** | 先 `package.json` → `pnpm install`，后 `src/` → `pnpm build`，利用 Docker layer cache |
| **--frozen-lockfile** | 锁定依赖版本，CI 中避免 `pnpm install` 意外更新 lockfile |
| **--prod** | Production 阶段排除 devDependencies，`jest`、`ts-jest` 等不进入最终镜像 |
| **pnpm layer cache** | `corepack enable` + 固定 pnpm 版本，确保 CI 与本地构建一致 |
| **Prisma Client** | Build 阶段 `prisma generate` 生成 Client，Production 阶段复制 `.prisma/` 目录 |

## NPM Scripts

```json
{
  "docker:build": "docker build -t nest-graphql-lab .",
  "docker:up": "docker compose up -d",
  "docker:down": "docker compose down"
}
```
