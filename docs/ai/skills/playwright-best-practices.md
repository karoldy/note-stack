---
description: playwright-best-practices — Currents.dev 维护的 Playwright 测试最佳实践 Skill，涵盖定位器选择、Web-First 断言、调试、API 测试、视觉回归、无障碍测试等完整测试领域。
---

# Playwright Best Practices

## 概述

`playwright-best-practices` 是 Currents.dev 团队维护的 Playwright 测试最佳实践 Skill（`currents-dev/playwright-best-practices-skill`，MIT 许可证）。它提供编写、调试、维护 Playwright 测试的专业知识，覆盖 E2E 测试、组件测试、API 测试、视觉回归测试、无障碍测试、安全测试等全场景，附带 `locators.md`、`assertions-waiting.md`、`debugging.md` 等专项参考文件。

- **分类**：开发 & 集成
- **调用方式**：自动触发（编写或修改 `.spec.ts` 文件时）
- **来源**：社区（Currents.dev）

## 触发条件

以下场景应调用该 Skill：

- 编写 Playwright E2E 测试用例
- 选择或重构定位器（Locator）策略
- 调试不稳定（Flaky）的测试
- 配置 Playwright 项目（`playwright.config.ts`）
- 实现视觉回归测试或无障碍测试
- 编写 API Mock 或网络拦截测试
- Playwright 版本升级（v1.x → 最新版）

以下场景**不应**使用：

- 使用 Cypress、Selenium、Puppeteer 等其他测试框架
- 纯单元测试（Jest/Vitest）
- 后端 API 测试（使用 Supertest 或类似工具）

## 专项参考文件

| 文件 | 内容 |
| --- | --- |
| `SKILL.md` | Skill 元数据与总体指南 |
| `locators.md` | 健壮的定位器策略（优先 `getByRole`、`getByLabel`） |
| `assertions-waiting.md` | Web-First 断言与自动等待机制 |
| `debugging.md` | Trace Viewer 使用、断点调试、故障排查 |

## 使用示例

### 安装

```bash
npx skills add https://github.com/currents-dev/playwright-best-practices-skill
```

### 测试编写示例

```typescript
// Skill 将引导生成如下风格的测试代码：
import { test, expect } from '@playwright/test';

test.describe('Login Page', () => {
  test('should display error for invalid credentials', async ({ page }) => {
    await page.goto('/login');

    // 优先使用 getByRole（无障碍友好）
    await page.getByRole('textbox', { name: 'Email' }).fill('bad@test.com');
    await page.getByRole('textbox', { name: 'Password' }).fill('wrong');
    await page.getByRole('button', { name: 'Sign in' }).click();

    // Web-First 断言（自动等待）
    await expect(page.getByRole('alert')).toContainText('Invalid credentials');
  });
});
```

## 最佳实践

- **定位器优先级**：`getByRole` > `getByLabel` > `getByTestId` > CSS 选择器
- **使用 Web-First 断言**：`expect(locator).toBeVisible()` 替代 `page.waitForSelector()`
- **测试隔离**：每个 `test` 独立运行，不依赖其他测试的状态
- **搭配 CI**：使用 Currents.dev 或 GitHub Actions 运行 Playwright 测试，获取 Trace 和截图
- 使用 Page Object Model 封装重复的页面交互逻辑

## 注意事项

- 不要混合使用 `page.waitForTimeout()` 做同步 — 使用 `expect` 的自动等待
- 避免使用脆弱的 CSS/XPath 选择器，优先使用语义化定位器
- Trace 文件体积可能较大，CI 环境需配置合适的保留策略
- Playwright 版本更新频繁，关注 Skill 仓库的更新日志

## 相关 Skills

- [[web-quality]] — Web 质量与性能审计
- [[shadcn]] — shadcn/ui 组件测试
- [[vercel-react-best-practices]] — React 应用 E2E 测试场景

## 参考资源

- [GitHub 仓库](https://github.com/currents-dev/playwright-best-practices-skill)
- [Currents.dev 官方文档](https://docs.currents.dev/ai/agent-skill-playwright-best-practices)
- [Playwright 官方文档](https://playwright.dev)
