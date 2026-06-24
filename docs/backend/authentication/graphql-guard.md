---
description: GraphQL 权限守卫 — 将 Passport JWT AuthGuard 适配为 GraphQL 上下文，实现 Query/Mutation 级别的权限控制，附权限矩阵与 @CurrentUser 装饰器设计。
---

# GraphQL 权限守卫

## 概述

NestJS 的 `AuthGuard('jwt')` 默认处理 HTTP 请求上下文，GraphQL 请求需要将其适配为 `GqlExecutionContext`，使 JWT 校验逻辑能正确从 WebSocket/HTTP 升级的 GraphQL 请求中提取 `Authorization` 头。

## JwtStrategy

```typescript
// src/auth/strategies/jwt.strategy.ts
@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(private readonly authService: AuthService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      secretOrKey: process.env.JWT_SECRET ?? 'dev-secret',
    });
  }

  async validate(payload: { sub: number }) {
    return this.authService.validateUser(payload.sub);
  }
}
```

**解析流程**：

```text
Authorization: Bearer <token>
  → ExtractJwt.fromAuthHeaderAsBearerToken() 提取
    → jwtService.verify(token, secret) 校验签名与过期
      → validate({ sub: userId }) → Prisma 查库
        → req.user = User 对象
```

## JwtAuthGuard（GraphQL 适配版）

```typescript
// src/auth/guards/jwt-auth.guard.ts
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  getRequest(context: ExecutionContext) {
    const ctx = GqlExecutionContext.create(context);
    return ctx.getContext().req;
  }
}
```

关键点：`GqlExecutionContext.create(context)` 将 GraphQL 上下文适配为 HTTP 风格，让 `AuthGuard('jwt')` 能从 GraphQL 请求中提取 `Authorization` 头。

## @CurrentUser 装饰器

```typescript
// src/auth/decorators/current-user.decorator.ts
export const CurrentUser = createParamDecorator(
  (data: unknown, context: ExecutionContext) => {
    const ctx = GqlExecutionContext.create(context);
    return ctx.getContext().req.user;
  },
);
```

## 使用示例

### 保护 Query

```typescript
@Query(() => User)
@UseGuards(JwtAuthGuard)
me(@CurrentUser() user: User) {
  return user;  // 当前登录用户信息
}
```

### 保护 Mutation

```typescript
@Mutation(() => Post)
@UseGuards(JwtAuthGuard)
createPost(@Args('input') input: CreatePostInput) {
  return this.postService.create(input);
}
```

### 权限矩阵参考

| 模块 | 受保护操作 | 公开操作 |
| --- | --- | --- |
| Auth | `me` | `signup`, `login`, `refreshToken`, `logout` |
| User | `createUser`, `updateUser`, `deleteUser` | `users`, `user` |
| Post | `createPost`, `updatePost`, `deletePost` | `posts`, `post` |

## 测试验证

### 无 Token → 401

```bash
curl -X POST /graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ me { id } }"}'
# → { "errors": [{ "message": "Unauthorized" }] }
```

### 带 Token → 通过

```bash
TOKEN=$(curl -X POST /graphql ... login ... | jq -r '.data.login.accessToken')

curl -X POST /graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query":"{ me { id name email } }"}'
# → { "data": { "me": { "id": 3, "name": "Charlie", "email": "..." } } }
```
