---
description: NestJS 框架概览 — 覆盖三层架构、依赖注入、模块化设计、CLI 工具链，以及与 GraphQL、Prisma、JWT、DataLoader 的集成生态。
---

# NestJS

## 概述

NestJS 是 Node.js 生态中最成熟的企业级后端框架，采用 **模块化 + 依赖注入 + 装饰器** 的架构风格，天然支持 TypeScript。它提供了开箱即用的 GraphQL、数据库、认证、测试、微服务等模块化集成能力。

**适用场景**：API 服务、GraphQL 后端、微服务、实时应用（WebSocket/Subscription）。

## 核心概念

- **模块（Module）**：`@Module()` 装饰器组织代码，每个功能领域一个模块
- **控制器（Controller）**：处理 HTTP 请求，路由分发
- **服务（Service）**：业务逻辑层，通过依赖注入消费
- **Resolver**：GraphQL 版本的 Controller，处理 Query / Mutation / Subscription
- **Guard**：权限守卫，请求级别的中间件
- **Pipe**：数据转换与校验管道
- **Interceptor**：面向切面的拦截器（日志、缓存、响应映射）

## 技术栈生态

| 领域 | 集成方案 | 文档 |
| --- | --- | --- |
| GraphQL | `@nestjs/graphql` + Apollo Server | [[graphql-code-first]] |
| 数据库 | Prisma ORM | [[../database/prisma-setup]] |
| 认证 | `@nestjs/jwt` + Passport | [[../authentication/jwt-auth]] |
| 校验 | `class-validator` + `ValidationPipe` | [[dto-validation]] |
| 测试 | `@nestjs/testing` + Jest | [[unit-testing]] |
| 部署 | Docker 多阶段构建 | [[docker-deploy]] |
| CI/CD | GitHub Actions Pipeline | [[cicd]] |
| 代码生成 | GraphQL Codegen | [[codegen]] |

## 快速开始

```bash
# 安装 CLI
pnpm add -D @nestjs/cli

# 创建新项目
nest new my-project
```

## 目录结构

```tree
src/
├── main.ts              # 应用入口，监听端口
├── app.module.ts        # 根模块
├── app.controller.ts    # 根控制器
├── app.service.ts       # 根服务
└── user/                # User 模块
    ├── user.module.ts
    ├── user.resolver.ts
    ├── user.service.ts
    ├── dto/
    │   ├── create-user.input.ts
    │   └── update-user.input.ts
    └── entities/
        └── user.entity.ts
```
