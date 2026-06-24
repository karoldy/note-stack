---
description: JWT 认证实战 — 使用 @nestjs/jwt + Passport 实现用户注册、登录、JWT Access Token 签发，附 bcrypt 密码哈希与 pnpm 构建脚本踩坑解决。
---

# JWT 认证

## 概述

JWT（JSON Web Token）是最广泛使用的无状态认证方案。结合 Passport 策略模式，NestJS 可通过 `@nestjs/jwt` + `@nestjs/passport` 快速搭建注册/登录/鉴权体系。Access Token 短有效期（15min），配合 [[refresh-token|Refresh Token]] 实现长期会话。

## 安装

```bash
pnpm add @nestjs/jwt @nestjs/passport passport-jwt passport bcrypt
pnpm add -D @types/passport-jwt @types/bcrypt
```

### 踩坑：bcrypt 构建脚本被 pnpm 忽略

**现象**：`pnpm install` 警告 `Ignored build scripts: bcrypt@6.0.0`

**解决**：在 `.npmrc` 中添加：

```ini
onlyBuiltDependencies[]=bcrypt
```

## AuthModule 配置

```typescript
// src/auth/auth.module.ts
import { Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';

@Module({
  imports: [
    PassportModule,
    JwtModule.register({
      secret: process.env.JWT_SECRET ?? 'dev-secret',
      signOptions: { expiresIn: '15m' },   // Access Token 15分钟
    }),
  ],
  providers: [AuthService, AuthResolver, JwtStrategy],
  exports: [AuthService],
})
export class AuthModule {}
```

## AuthService 实现

```typescript
// src/auth/auth.service.ts
@Injectable()
export class AuthService {
  constructor(
    private readonly prisma: PrismaService,
    private readonly jwtService: JwtService,
  ) {}

  async signup(input: AuthSignupInput): Promise<AuthPayload> {
    // 1. 检查邮箱是否已注册
    const existing = await this.prisma.user.findUnique({
      where: { email: input.email },
    });
    if (existing) throw new ConflictException('Email already in use');

    // 2. 哈希密码
    const hashedPassword = await bcrypt.hash(input.password, 10);

    // 3. 创建用户
    const user = await this.prisma.user.create({
      data: { ...input, password: hashedPassword },
    });

    // 4. 签发 Token
    return this.generateTokens(user.id);
  }

  async login(input: AuthLoginInput): Promise<AuthPayload> {
    const user = await this.prisma.user.findUnique({
      where: { email: input.email },
    });
    if (!user) throw new UnauthorizedException('Invalid credentials');

    const valid = await bcrypt.compare(input.password, user.password);
    if (!valid) throw new UnauthorizedException('Invalid credentials');

    return this.generateTokens(user.id);
  }

  async validateUser(userId: number) {
    return this.prisma.user.findUnique({ where: { id: userId } });
  }
}
```

## 最佳实践

- JWT `secret` 必须通过环境变量注入，严禁硬编码
- Access Token 15 分钟过期，减少泄露后的风险窗口
- 密码使用 `bcrypt.hash(password, 10)` — 10 轮 salt 是安全与性能的平衡点
- `validateUser` 从数据库查询完整 User 对象，确保 `req.user` 反映最新状态
