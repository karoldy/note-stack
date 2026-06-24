---
description: GraphQL 进阶实战 — 覆盖 N+1 问题诊断、DataLoader 批量加载、Subscription 实时推送、Federation 微服务架构，框架无关的通用 GraphQL 最佳实践。
---

# GraphQL

## 概述

GraphQL 在生产环境中常见的四个进阶主题：查询性能优化（N+1 → DataLoader）、实时数据推送（Subscription）、微服务架构（Federation）。这些主题是框架无关的通用实践，示例代码基于 NestJS + Apollo Server。

## 核心主题

| 主题 | 文档 | 解决的问题 |
| --- | --- | --- |
| N+1 查询 | [[n-plus-one]] | GraphQL 嵌套查询导致数据库查询爆炸 |
| DataLoader | [[dataloader]] | 批量合并 + 请求级缓存 + 自动去重 |
| Subscription | [[subscription]] | WebSocket 实时数据推送 |
| Federation | [[federation]] | 微服务拆分后 Supergraph 聚合 |
