---
description: NestJS 单元测试实战 — 使用 @nestjs/testing + Jest 对 Service、Resolver、Guard 层进行分层测试，覆盖 Mock 依赖注入与覆盖率配置。
---

# 单元测试

## 概述

NestJS 通过 `@nestjs/testing` 提供模块化的测试工具，支持 Service、Resolver、Guard 各层的独立单元测试。利用依赖注入系统，可以轻松 Mock 外部依赖（Prisma、JWT Service 等），实现真正的隔离测试。

## 技术栈

| 工具 | 版本 | 用途 |
| --- | --- | --- |
| `jest` | ^30 | 测试运行器 |
| `ts-jest` | ^29 | TypeScript 编译 |
| `@nestjs/testing` | ^11 | NestJS 测试工具 |

## jest.config.ts

```typescript
import type { Config } from 'jest';

const config: Config = {
  moduleFileExtensions: ['js', 'json', 'ts'],
  rootDir: '.',
  testRegex: '.*\\.spec\\.ts$',
  transform: { '^.+\\.(t|j)s$': 'ts-jest' },
  collectCoverageFrom: [
    'src/**/*.(t|j)s',
    '!src/main.ts',
    '!src/app.module.ts',
    '!src/**/*.module.ts',
    '!src/prisma/generated/**',
    '!src/generated/**',
  ],
  coverageDirectory: './coverage',
  testEnvironment: 'node',
};
```

## Service 层测试

```typescript
// src/user/user.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { UserService } from './user.service';
import { PrismaService } from '../prisma/prisma.service';

describe('UserService', () => {
  let service: UserService;
  let prisma: PrismaService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UserService,
        {
          provide: PrismaService,
          useValue: {
            user: {
              findMany: jest.fn(),
              findUnique: jest.fn(),
              create: jest.fn(),
              update: jest.fn(),
              delete: jest.fn(),
            },
          },
        },
      ],
    }).compile();

    service = module.get<UserService>(UserService);
    prisma = module.get<PrismaService>(PrismaService);
  });

  it('should return all users', async () => {
    const mockUsers = [{ id: 1, name: 'Test', email: 'test@test.com' }];
    (prisma.user.findMany as jest.Mock).mockResolvedValue(mockUsers);

    const result = await service.findAll();
    expect(result).toEqual(mockUsers);
    expect(prisma.user.findMany).toHaveBeenCalled();
  });
});
```

## Resolver 层测试

```typescript
// src/user/user.resolver.spec.ts
describe('UserResolver', () => {
  let resolver: UserResolver;
  let userService: UserService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UserResolver,
        {
          provide: UserService,
          useValue: {
            findAll: jest.fn(),
            findOne: jest.fn(),
            create: jest.fn(),
          },
        },
      ],
    }).compile();

    resolver = module.get<UserResolver>(UserResolver);
    userService = module.get<UserService>(UserService);
  });

  it('should call userService.findAll', async () => {
    await resolver.findAll();
    expect(userService.findAll).toHaveBeenCalled();
  });
});
```

## Guard 层测试

```typescript
// src/auth/guards/jwt-auth.guard.spec.ts
describe('JwtAuthGuard', () => {
  it('should return 401 for missing token', () => {
    const context = createMockExecutionContext({ headers: {} });
    const guard = new JwtAuthGuard();
    // guard.canActivate(context) → false
  });
});
```

## 最佳实践

- Service 测试 Mock 数据库层，Resolver 测试 Mock Service 层 —— 每层只测自己的逻辑
- 使用 `jest.fn()` 创建 Mock 函数，用 `mockResolvedValue` / `mockRejectedValue` 覆盖正常与异常路径
- `collectCoverageFrom` 排除入口文件、模块注册文件、自动生成的代码
- CI 中使用 `pnpm test:cov` 确保覆盖率不下降
