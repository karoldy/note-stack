---
description: Refresh Token 轮换策略 — Access Token 15min + Refresh Token 7天双重令牌体系，UUID v4 防猜测、每次刷新撤销旧 Token（Rotation）、CASCADE 删除与完整生命周期管理。
---

# Refresh Token 轮换

## 概述

Access Token 短有效期（15min）保证泄露影响可控，Refresh Token 长有效期（7天）避免频繁登录。**Token 轮换（Rotation）** 是安全关键：每次刷新时撤销旧 RT 并签发新对，防止 Refresh Token 被盗用后长期有效。

## 策略设计

| Token 类型 | 有效期 | 存储位置 | 格式 |
| --- | --- | --- | --- |
| Access Token | 15 分钟 | 无（JWT 自包含） | JWT（`sub`, `iat`, `exp`） |
| Refresh Token | 7 天 | `refresh_tokens` 表（Prisma） | UUID v4 |

## 数据库模型

```prisma
model RefreshToken {
  id        String   @id @default(uuid())
  token     String   @unique
  userId    Int      @map("user_id")
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  expiresAt DateTime @map("expires_at")
  revoked   Boolean  @default(false)
  createdAt DateTime @default(now()) @map("created_at")

  @@index([userId])
  @@index([token])
  @@map("refresh_tokens")
}
```

## Token 生成

```typescript
// src/auth/auth.service.ts
private async generateTokens(userId: number): Promise<AuthPayload> {
  const accessToken = this.jwtService.sign({ sub: userId });

  const refreshToken = crypto.randomUUID();

  await this.prisma.refreshToken.create({
    data: {
      token: refreshToken,
      userId,
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
    },
  });

  return { accessToken, refreshToken };
}
```

## Token 轮换

```typescript
async refreshToken(token: string): Promise<AuthPayload> {
  const stored = await this.prisma.refreshToken.findUnique({
    where: { token },
  });

  if (!stored || stored.revoked) {
    throw new UnauthorizedException('Invalid refresh token');
  }

  if (new Date() > stored.expiresAt) {
    throw new UnauthorizedException('Refresh token expired');
  }

  // 撤销旧 Token
  await this.prisma.refreshToken.update({
    where: { id: stored.id },
    data: { revoked: true },
  });

  // 签发新对
  return this.generateTokens(stored.userId);
}
```

## 登出

```typescript
async logout(token: string) {
  const stored = await this.prisma.refreshToken.findUnique({
    where: { token },
  });
  if (stored && !stored.revoked) {
    await this.prisma.refreshToken.update({
      where: { id: stored.id },
      data: { revoked: true },
    });
  }
  return true;
}
```

## 完整生命周期

```text
signup/login → AT₁ + RT₁
refreshToken(RT₁) → RT₁ revoked, AT₂ + RT₂
refreshToken(RT₁) again → 401（已撤销）
refreshToken(RT₂) → RT₂ revoked, AT₃ + RT₃
logout(RT₃) → RT₃ revoked
refreshToken(RT₃) → 401（已注销）
```

## 安全特性

| 机制 | 说明 |
| --- | --- |
| Token 轮换 | 每次刷新撤销旧 RT，防止重放攻击 |
| 7 天过期 | `expiresAt` 超时自动失效，数据库无需额外清理 |
| CASCADE 删除 | 删除 User 时自动清理关联 RT |
| UUID v4 | `crypto.randomUUID()` 不可猜测 |
| 唯一索引 | `@unique` 防止 Token 碰撞 |

### API 一览

| 操作 | 类型 | 参数 | 鉴权 |
| --- | --- | --- | --- |
| `refreshToken` | Mutation | `token: String!` | 公开（RT 自身即鉴权凭证） |
| `logout` | Mutation | `token: String!` | `@UseGuards(JwtAuthGuard)` |

### cURL 测试

```bash
# 1. 登录获取双 Token
curl -X POST /graphql -H "Content-Type: application/json" \
  -d '{"query":"mutation { login(input: { email: \"user@test.com\", password: \"pass\" }) { accessToken refreshToken } }"}'

# 2. 刷新
curl -X POST /graphql -H "Content-Type: application/json" \
  -d '{"query":"mutation { refreshToken(token: \"<RT>\") { accessToken refreshToken } }"}'

# 3. 登出（需 Access Token）
curl -X POST /graphql -H "Content-Type: application/json" \
  -H "Authorization: Bearer <AT>" \
  -d '{"query":"mutation { logout(token: \"<RT>\") }"}'
```
