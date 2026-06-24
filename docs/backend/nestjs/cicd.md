---
description: NestJS 项目的 GitHub Actions CI Pipeline — lint、typecheck、test、Docker 四阶段并行流水线，附带 PostgreSQL Service Container 与构建缓存策略。
---

# CI/CD

## 概述

基于 GitHub Actions 构建 NestJS 项目的 CI Pipeline，每次 push 和 PR 自动执行 lint、类型检查（含 Prisma Generate + GraphQL Codegen）、单元测试、Docker 构建四个阶段。

## Pipeline 架构

```mermaid
graph LR
    A[Push / PR] --> B[lint]
    B --> C[typecheck]
    B --> D[test]
    C --> E[docker]
    D --> E
```

## GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [master, dev]
  pull_request:
    branches: [master]

jobs:
  # ─── Lint ────────────────────────────────────
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 10
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint

  # ─── Type Check + Prisma + Codegen ─────────
  typecheck:
    name: TypeScript & Codegen
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: nest-graphql-lab
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U postgres -d nest-graphql-lab"
          --health-interval 5s --health-timeout 5s --health-retries 5
    env:
      DATABASE_URL: postgresql://postgres:postgres@localhost:5432/nest-graphql-lab?schema=public
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 10
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - name: Prisma Generate
        run: npx prisma generate
      - name: TypeScript Check
        run: npx tsc --noEmit
      - name: Build
        run: pnpm build
      - name: GraphQL Codegen
        run: |
          timeout 15 node dist/main 2>/dev/null || true
          pnpm codegen

  # ─── Unit Tests ────────────────────────────
  test:
    name: Unit Tests
    runs-on: ubuntu-latest
    needs: [lint]
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 10
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - name: Run tests with coverage
        run: pnpm test:cov
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage
          path: coverage/
          retention-days: 7

  # ─── Docker Build ──────────────────────────
  docker:
    name: Docker Build
    runs-on: ubuntu-latest
    needs: [lint, typecheck, test]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      - name: Build Docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          push: false
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## CI 检查项

| 检查项 | Job | 失败条件 |
| --- | --- | --- |
| ESLint | `lint` | 有 error |
| Prisma Schema | `typecheck` → Prisma Generate | 生成失败 |
| TypeScript 编译 | `typecheck` → tsc --noEmit | 类型错误 |
| NestJS 构建 | `typecheck` → nest build | 构建失败 |
| GraphQL Codegen | `typecheck` → codegen | 生成失败 |
| 单元测试 | `test` → jest --coverage | 测试失败 |
| Docker 镜像 | `docker` → build | 构建失败 |

## 关键设计决策

| 决策 | 理由 |
| --- | --- |
| `lint` 先行 | 语法错误没有继续 typecheck/test 的意义 |
| `test` 和 `typecheck` 并行 | 二者互不依赖，并行缩短 CI 耗时 |
| `docker` 最后 | 所有质量门禁通过后再构建镜像 |
| `gha` cache | GitHub Actions Cache 加速 Docker layer 缓存命中 |
| PostgreSQL Service Container | typecheck 阶段需要数据库连接（Prisma Generate 依赖 DATABASE_URL） |
