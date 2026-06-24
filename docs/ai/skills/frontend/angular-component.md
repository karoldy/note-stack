---
description: angular-component — Angular 组件开发 Skill，由 analogjs/angular-skills 社区维护，覆盖 Angular v20+ 的 Standalone Components、Signal Inputs/Outputs、OnPush、Signal Forms、RxJS Interop 等现代模式。
---

# Angular Component

## 概述

`angular-component` 是社区维护的 Angular 组件开发 Skill，最活跃的实现来自 **`analogjs/angular-skills`**（由 Angular 核心贡献者 Brandon Roberts 维护）。它覆盖 **Angular v20+ 的现代开发模式**：Standalone Components、Signal Inputs/Outputs、`OnPush` 变更检测、Content Projection、Signal Forms 等。另有 `inbharatai/claude-skills` 也提供基础版 Angular 组件 Skill。

- **分类**：开发 & 集成
- **调用方式**：自动触发（编辑 `.ts` / `.html` 文件且有 Angular 特征时）
- **来源**：社区（analogjs）

## 触发条件

以下场景应调用该 Skill：

- 创建或修改 Angular Standalone Component
- 使用 Signal Inputs/Outputs（`input()`、`output()`）
- 设计依赖注入（`inject()`、Injection Tokens）
- 实现 Signal Forms 或 Reactive Forms
- 从旧版 Angular（v14-）迁移至 v20+
- 使用 Angular Material / CDK 组件

以下场景**不应**使用：

- AngularJS（1.x）项目
- 非 Angular 框架（React、Vue、Svelte）
- 后端 NestJS 开发（语法相似但场景不同）

## analogjs/angular-skills 子模块

| 子 Skill | 内容 |
| --- | --- |
| `angular-component` | Standalone Components、Signal Inputs/Outputs、OnPush、Host Bindings、Content Projection |
| `angular-signals` | `signal()`、`computed()`、`effect()`、RxJS Interop |
| `angular-di` | `inject()`、Injection Tokens、Providers 层级 |
| `angular-forms` | Signal Forms、Schema-based Validation |
| `angular-http` | `httpResource()`、`resource()`、`HttpClient` |
| `angular-routing` | Lazy Loading、Functional Guards、`input.fromRoute()` |
| `angular-directives` | Attribute / Structural Directives |
| `angular-ssr` | SSR、Incremental Hydration |
| `angular-testing` | TestBed、Component Harnesses、Vitest |
| `angular-tooling` | CLI 命令、Schematics |

## 使用示例

### 安装

```bash
# 安装完整 analogjs/angular-skills 套件
npx skills add analogjs/angular-skills

# 或只安装 component 子 Skill
npx skills add analogjs/angular-skills --skill angular-component
```

### 现代 Angular 组件示例

```typescript
// user-card.component.ts
import { Component, input, output, effect } from '@angular/core';

@Component({
  selector: 'app-user-card',
  standalone: true,
  template: `
    <div class="card">
      <h3>{{ displayName() }}</h3>
      <p>{{ bio() }}</p>
      <button (click)="follow.emit(userId())">Follow</button>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UserCardComponent {
  // Signal Inputs（替代 @Input）
  readonly userId = input.required<string>();
  readonly displayName = input.required<string>();
  readonly bio = input('No bio yet');

  // Signal Outputs（替代 @Output）
  readonly follow = output<string>();

  constructor() {
    effect(() => {
      console.log(`User ${this.displayName()} loaded`);
    });
  }
}
```

## 最佳实践

- 默认使用 `Standalone Components`，避免 NgModules
- 使用 Signal Inputs/Outputs 替代传统 `@Input()` / `@Output()` 装饰器
- 开启 `OnPush` 变更检测策略以获得最佳性能
- 通过 `inject()` 函数替代构造函数注入
- 使用 `@defer` 实现组件级懒加载

## 注意事项

- Angular v20+ 的 Signal Forms 和 `resource()` 尚在 Preview 阶段，生产环境需评估
- `analogjs/angular-skills` 面向最新版 Angular，旧项目可能需渐进式迁移
- 使用 RxJS Interop（`toSignal` / `toObservable`）桥接旧的 RxJS 代码

## 相关 Skills

- [[frontend-ui-engineering]] — UI 工程化通用实践
- [[frontend-design]] — 视觉设计指导
- [[web-quality]] — 无障碍与性能审计

## 参考资源

- [analogjs/angular-skills](https://github.com/analogjs/angular-skills)
- [inbharatai/claude-skills](https://github.com/inbharatai/claude-skills)
- [Angular 官方文档](https://angular.dev)
- [Angular Signals 指南](https://angular.dev/guide/signals)
