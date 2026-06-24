---
description: Claude Code CLI 配置体系全解 — .claude/ 目录结构、CLAUDE.md、settings.json、commands、rules、skills、agents 的用途、写法与实战示例。
---

# Claude Code

## 概述

Claude Code 是 Anthropic 推出的 CLI 编程助手，通过终端直接与代码库交互。其配置体系以项目根目录下的 `.claude/` 文件夹和 `CLAUDE.md` 文件为核心，遵循**约定优于配置**原则 —— 文件放到对应目录即可生效，无需显式注册。

本文覆盖 `.claude/` 目录下每一个组件的作用、写法规范、实际示例与最佳实践。

## 前置知识

- 已安装 Claude Code CLI
- 了解基本的命令行操作
- 熟悉 Markdown 语法

---

## .claude/ 目录结构总览

```tree
你的项目/
 ├── CLAUDE.md              # 项目级指令（随 Git 提交）
 ├── CLAUDE.local.md        # 本地私密指令（不提交）
 └── .claude/
     ├── settings.json       # 项目级配置
     ├── settings.local.json # 本地私密配置（不提交）
     ├── commands/           # 自定义 Slash Command
     │   ├── review.md
     │   ├── fix-issue.md
     │   └── deploy.md
     ├── rules/              # 编码规范与约束
     │   ├── code-style.md
     │   ├── testing.md
     │   └── api-conventions.md
     ├── skills/             # 自定义 Skill（领域知识 + 工具 + 工作流）
     │   ├── security-review/
     │   │   └── SKILL.md
     │   └── deploy/
     │       └── SKILL.md
     └── agents/             # 自定义 Subagent（专门化子任务处理器）
         ├── code-review.md
         └── security-auditor.md
```

### 优先级规则

Claude Code 加载配置时遵循以下优先级（后者覆盖前者）：

1. **内置默认值** → 项目级配置（`CLAUDE.md`、`.claude/`）→ 用户级配置（`~/.claude/`）→ 本地覆盖（`*.local.*`）
2. **更具体的配置**覆盖更通用的配置
3. **本地文件**（`*.local.*`）不提交到 Git，适合存放私密信息或个人偏好

---

## CLAUDE.md

### 作用

`CLAUDE.md` 是项目的"使用说明书"，Claude Code 在每次会话启动时自动读取。它告诉 Claude：

- 项目的技术栈和架构
- 编码规范和风格偏好
- 常见任务的执行方式
- 需要特别注意的约束

### 应该写什么

| 适合放入 | 不适合放入 |
| --- | --- |
| 项目技术栈概述 | 冗长的 API 文档（应链接） |
| 目录结构约定 | 可自动推导的信息 |
| 编码风格与命名规范 | 频繁变动的临时配置 |
| 测试运行方式 | 敏感信息（用 `.local.md`） |
| 构建/部署命令 | 大段复制的第三方文档 |
| 架构决策与约束 | |

### 示例

以下是一个典型的前端项目 `CLAUDE.md`：

```markdown
# CLAUDE.md

## 技术栈

- React 18 + TypeScript
- Vite 构建
- Tailwind CSS
- Zustand 状态管理
- React Router v6 路由

## 目录结构

- `src/components/` — 通用组件
- `src/features/` — 按功能模块组织的页面
- `src/hooks/` — 自定义 Hooks
- `src/stores/` — Zustand stores
- `src/utils/` — 工具函数

## 编码规范

- 组件使用函数式声明 + Hooks，禁止 Class Component
- 优先使用 `interface` 而非 `type`
- 文件名使用 kebab-case，组件名使用 PascalCase
- 每个文件不超过 300 行

## 常用命令

- `pnpm dev` — 启动开发服务器
- `pnpm test` — 运行单元测试
- `pnpm lint` — 代码检查
- `pnpm build` — 生产构建

## 注意事项

- API 基础 URL 通过 `VITE_API_BASE` 环境变量配置
- 所有网络请求必须处理 loading/error/success 三种状态
- 不要直接修改 `src/generated/` 目录下的文件
```

### CLAUDE.md vs CLAUDE.local.md

| 特性 | `CLAUDE.md` | `CLAUDE.local.md` |
| --- | --- | --- |
| Git 提交 | ✅ 提交 | ❌ 不提交（已在 .gitignore） |
| 用途 | 团队共享的规范 | 个人偏好/私密信息 |
| 典型内容 | 编码规范、架构说明 | 个人快捷键偏好、本地路径 |

**示例 `CLAUDE.local.md`：**

```markdown
# 个人配置

- 我的本地数据库连接字符串：postgresql://localhost:5432/mydb
- 优先使用 pnpm 而非 npm
- 不要在回答中提及公司内部代号
```

---

## .claude/settings.json

### 作用

`settings.json` 是 Claude Code 的主配置文件，控制权限、Hook、环境变量和模型行为。

### 核心配置项

#### 权限管理 (permissions)

控制哪些操作需要用户确认：

```json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm run lint)",
      "Bash(git diff)",
      "Bash(git status)",
      "Read(/Users/turbo.su/Project/**)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force)",
      "Bash(curl *)"
    ]
  }
}
```

**最佳实践**：使用通配符 `**` 减少配置量，将常用读操作放开，危险操作显式拒绝。

#### Hook 系统

在特定事件触发时自动执行脚本：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(git commit*)",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint && npm test"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write $CLAUDE_TOOL_INPUT_FILE_PATH"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/osascript -e 'display notification \"Claude Code 任务完成\"'"
          }
        ]
      }
    ]
  }
}
```

**常用 Hook 事件**：

| 事件 | 触发时机 |
| --- | --- |
| `PreToolUse` | 工具执行前 |
| `PostToolUse` | 工具执行后 |
| `Notification` | 会话需要通知用户时 |
| `Stop` | 会话结束时 |

#### 环境变量

```json
{
  "env": {
    "NODE_ENV": "development",
    "DEBUG": "claude:*"
  }
}
```

#### 模型配置

```json
{
  "model": "claude-sonnet-4-6",
  "enableThinking": true,
  "permissionMode": "default"
}
```

### settings.json vs settings.local.json

与 CLAUDE.md 同理，`settings.local.json` 不提交到 Git，适合存放个人令牌、本地路径等敏感信息：

```json
{
  "env": {
    "GITHUB_TOKEN": "ghp_xxxxxxxxxxxx",
    "DATABASE_URL": "postgresql://localhost:5432/dev"
  }
}
```

---

## .claude/commands/

### 作用

自定义 Slash Command —— 项目特定的 `/command`，将常用操作封装为一键调用的指令。

### 文件结构

每个 `.md` 文件对应一个 `/命令名`：

```text
.claude/commands/
 ├── review.md      → /review
 ├── fix-issue.md   → /fix-issue
 └── deploy.md      → /deploy
```

### 写法

Command 文件就是一个 Markdown 文件，内容即为发送给 Claude 的 Prompt。支持 YAML frontmatter 定义元信息。

#### 示例：代码审查命令

`.claude/commands/review.md`：

```markdown
---
description: 对当前分支变更进行代码审查，输出 Bug 风险、性能问题和可维护性建议
---

请对当前分支的 diff 进行全面的代码审查，关注以下维度：

## 审查维度

1. **正确性** — 是否存在逻辑错误、边界条件遗漏、空值处理缺失
2. **安全性** — 是否存在注入风险、敏感信息泄露、权限校验缺陷
3. **性能** — 是否存在不必要的重渲染、内存泄漏、N+1 查询
4. **可维护性** — 命名是否清晰、函数是否过长、是否存在重复代码

## 输出格式

按严重程度分为 🔴 严重 / 🟡 建议 / 🟢 小优化，每条包含：
- **文件路径与行号**
- **问题描述**
- **修复建议**（含代码示例）
```

使用方式：

```bash
/review
```

#### 示例：自动修复 Issue

`.claude/commands/fix-issue.md`：

```markdown
---
description: 根据 GitHub Issue 编号，分析问题并自动提交修复 PR
argument-hint: <issue-number>
---

请执行以下步骤修复 Issue #$ARGUMENTS：

1. **理解问题**：读取 GitHub Issue 的描述和讨论
2. **定位代码**：在代码库中找到相关文件
3. **编写修复**：实现修复方案
4. **验证**：运行相关测试确保修复有效
5. **提交**：使用规范的 commit message 提交变更

Commit message 格式：`fix(#$ARGUMENTS): <简短描述>`
```

使用方式：

```bash
/fix-issue 42
```

### 参数传递

Command 通过 `$ARGUMENTS` 变量获取用户输入的参数。可以在 Prompt 中直接引用。

---

## .claude/rules/

### 作用

Rules 是编码规范的声明式定义，Claude Code 在生成代码时会主动遵循这些规则。与 CLAUDE.md 不同，Rules 更细粒度、可按场景加载。

### 与 CLAUDE.md 的区别

| | CLAUDE.md | rules/ |
| --- | --- | --- |
| 粒度 | 项目级总览 | 按领域拆分 |
| 加载方式 | 每次会话自动加载 | 按需/按文件类型加载 |
| 典型长度 | 50-200 行 | 10-50 行 |
| 组织方式 | 单文件 | 多文件分目录 |

### 示例

#### 代码风格规范

`.claude/rules/code-style.md`：

```markdown
# TypeScript 代码风格

## 命名规范

- 变量/函数：camelCase
- 类型/接口：PascalCase
- 常量：UPPER_SNAKE_CASE
- 文件名：kebab-case

## 类型使用

- 永远不要使用 `any`
- 优先使用 `interface` 而非 `type`
- 使用 `as` 类型断言时必须有注释说明原因

## 函数规范

- 单个函数不超过 50 行
- 参数超过 3 个时使用对象参数
- 异步函数必须返回 `Promise<T>` 类型
```

#### 测试规范

`.claude/rules/testing.md`：

```markdown
# 测试规范

## 通用规则

- 使用 Vitest 作为测试框架
- 测试文件与源文件同目录，命名为 `*.test.ts`
- 测试覆盖率目标：分支 80%+

## 测试结构

- 使用 `describe` / `it` 组织
- 测试命名：`should <期望行为> when <条件>`
- 每个测试独立，不依赖执行顺序

## 示例

\`\`\`ts
describe('parseConfig', () => {
  it('should return default config when input is empty', () => {
    expect(parseConfig({})).toEqual(DEFAULT_CONFIG);
  });

  it('should throw ValidationError when required field is missing', () => {
    expect(() => parseConfig({ name: '' })).toThrow(ValidationError);
  });
});
\`\`\`
```

#### API 规范

`.claude/rules/api-conventions.md`：

```markdown
# API 约定

## RESTful 设计

- URL 使用复数名词：`/api/users`，非 `/api/user`
- 分页参数统一使用 `page` + `pageSize`
- 错误响应格式：`{ error: { code: string, message: string } }`

## 请求处理

- 所有 API Handler 必须校验输入
- 使用 Zod 或类似库定义 Schema
- 敏感操作必须记录审计日志
```

---

## .claude/skills/

### 作用

Skill 是 Claude Code 的扩展单元，封装了特定领域的知识、工作流和工具集成。每个 Skill 包含一个 `SKILL.md` 文件，定义触发条件、执行流程和所需资源。

### 目录结构

```text
.claude/skills/
 ├── my-skill/
 │   └── SKILL.md          # 核心定义（唯一必需文件）
 └── another-skill/
     ├── SKILL.md
     ├── scripts/           # 辅助脚本
     │   └── validate.sh
     └── templates/         # 模板文件
         └── report.md
```

### SKILL.md 结构

```markdown
---
name: my-skill
description: 一句话描述 Skill 的功能
triggers:
  - 生成报告
  - generate report
  - /my-skill
---

# My Skill

## 概述

详细说明这个 Skill 解决什么问题。

## 触发条件

- 用户提到"生成报告"时自动触发
- 手动调用 `/my-skill`

## 工作流

1. 收集所需信息
2. 生成报告内容
3. 输出到指定目录

## 最佳实践

- 先用默认模板生成，再根据反馈调整
- 敏感数据不写入报告

## 注意事项

- 需要项目已安装 pandoc
```

### 实际示例：部署检查 Skill

`.claude/skills/deploy-check/SKILL.md`：

```markdown
---
name: deploy-check
description: 在部署前检查关键项，确保安全上线
triggers:
  - 部署检查
  - deploy check
  - 准备上线
---

# Deploy Check

## 概述

在代码部署到生产环境前，对关键项进行系统检查，降低上线风险。

## 检查清单

### 代码质量
- [ ] `npm run lint` 通过
- [ ] `npm run test` 全部通过
- [ ] 无 TODO / FIXME 残留（需要转为 Issue）

### 数据库
- [ ] 迁移脚本已生成且可回滚
- [ ] 无破坏性 Schema 变更（如重命名列）

### 配置
- [ ] 环境变量已同步到部署平台
- [ ] 第三方 API Key 未过期

### 监控
- [ ] 关键指标已配置告警
- [ ] 错误追踪 SDK 版本最新

## 输出格式

按状态输出：
- ✅ 通过
- ❌ 阻塞（必须修复）
- ⚠️ 警告（建议修复）

阻塞项未修复前不得合并 PR。
```

详细 Skill 开发指南参见 [Skills 目录](../../skills/index.md)。

---

## .claude/agents/

### 作用

Agent 是预定义的专业化 Subagent —— 每个 Agent 有特定的角色定位和工具权限，适合执行类型化任务（如代码审查、安全审计、代码探索）。

### 与 Commands 的区别

| | commands/ | agents/ |
| --- | --- | --- |
| 执行方式 | `/command` 手动调用 | 被 Claude 按需调度 |
| 角色 | 任务模板 | 专业化角色 |
| 工具权限 | 继承主会话 | 可独立限制 |
| 适用场景 | 固定流程的任务 | 需要特定视角的分析 |

### 写法

Agent 文件是一个 Markdown 文件，内容为该 Agent 的角色定义。

#### 示例：代码审查 Agent

`.claude/agents/code-review.md`：

```markdown
# Code Reviewer

你是一位资深代码审查者，专注于发现代码中的逻辑错误、安全隐患和可维护性问题。

## 审查原则

1. **先理解，后评判** — 读懂代码意图再提出建议
2. **有数据支撑** — 性能问题需引用复杂度分析
3. **提供方案** — 每个问题附修复建议，而非仅指出问题
4. **区分严重性** — 明确标注阻断/警告/建议

## 审查维度

- 逻辑正确性：边界条件、异常处理、状态机完整性
- 安全性：注入、越权、敏感信息泄露
- 性能：不必要的分配、N+1 查询、内存泄漏模式
- 可维护性：命名、函数长度、重复代码、耦合度

## 输出格式

| 严重性 | 文件 | 行号 | 问题 | 建议 |
| --- | --- | --- | --- | --- |
| 🔴 阻断 | | | | |
| 🟡 警告 | | | | |
| 🟢 建议 | | | | |
```

#### 示例：安全审计 Agent

`.claude/agents/security-auditor.md`：

```markdown
# Security Auditor

你是应用安全专家，负责审查代码中的安全漏洞。你关注 OWASP Top 10 及以下领域：

## 审查重点

1. **注入攻击**：SQL、NoSQL、命令注入
2. **认证失效**：会话管理、JWT 配置、密码策略
3. **敏感数据暴露**：日志中的凭证、硬编码密钥、调试信息
4. **访问控制**：越权漏洞、缺少权限校验
5. **安全配置**：CORS 策略、CSP 头、依赖漏洞

## 判定标准

- 🔴 **确认漏洞**：存在可被利用的安全缺陷，必须立即修复
- 🟡 **潜在风险**：不安全的实践，在特定条件下可被利用
- 🟢 **加固建议**：当前无直接风险，但改进可增强安全性

## 输出要求

对每个问题输出：
- 风险描述与利用场景
- 受影响的代码位置
- 修复方案（含代码示例）
- CWE 编号（如适用）
```

---

## 实践指南

### 项目规模与配置策略

#### 小型项目（个人/原型）

最小化配置，只需一个 `CLAUDE.md`：

```text
my-project/
 └── CLAUDE.md    # 包含技术栈 + 基本规范
```

#### 中型项目（5-20 人团队）

按领域拆分规则：

```text
my-project/
 ├── CLAUDE.md
 └── .claude/
     ├── settings.json
     ├── rules/
     │   ├── code-style.md
     │   └── testing.md
     └── commands/
         └── review.md
```

#### 大型项目（20+ 人，多团队）

完整配置体系：

```text
my-project/
 ├── CLAUDE.md                        # 项目总览 + 全局约定
 ├── packages/
 │   └── web/
 │       ├── CLAUDE.md                # 子项目特定指令
 │       └── .claude/
 │           ├── rules/               # 前端特有规则
 │           └── commands/            # 前端特有命令
 └── .claude/
     ├── settings.json
     ├── rules/                       # 全局规则
     ├── commands/                    # 全局命令
     ├── skills/                      # 共享 Skill
     └── agents/                      # 共享 Agent
```

### 团队协作最佳实践

#### 1. CLAUDE.md 分层策略

**根目录 `CLAUDE.md`** 写全局约定（Git 提交、目录命名、通用工具链），**子目录 `CLAUDE.md`** 写包/服务特有的规则。Claude Code 会递归读取当前工作目录下的所有 `CLAUDE.md`。

#### 2. Rules 的"为什么"原则

每条规则都应说明原因。对比：

```markdown
<!-- ❌ 不好：只说了规则，没解释原因 -->
- 禁止使用 any

<!-- ✅ 好：解释了原因，帮助 Claude 理解意图 -->
- 禁止使用 any — 会绕过类型检查，导致运行时错误难以追踪
  如果确实需要动态类型，使用 unknown + 类型守卫
```

#### 3. Command 的幂等性

每个 Command 应该被设计为可以安全地重复执行。在指令中加入检查逻辑：

```markdown
## 步骤

1. 检查是否已有未合并的 PR，如有则跳过创建
2. 生成变更摘要
3. 创建 PR（如不存在）
4. 添加标签和 Reviewer
```

#### 4. 渐进式完善

不要一次性写完所有配置。推荐的工作流：

1. 从 `CLAUDE.md` 开始，使用一周
2. 发现 Claude 频繁犯同样的错误 → 补充一条 Rule
3. 发现某个操作反复手动执行 → 封装为 Command
4. 发现某个复杂任务需要专门化 → 创建 Skill 或 Agent

#### 5. 配置即文档

`.claude/` 目录本身就是一份活的团队规范文档：

- 新成员通过阅读 `rules/` 了解编码规范
- 通过 `commands/` 了解常用工作流
- 通过 `CLAUDE.md` 快速上手项目

---

## 常见问题

### CLAUDE.md 和 .claude/rules/ 有什么区别？

`CLAUDE.md` 是面向整个项目的综合指令，包含技术栈、架构概述、常用命令等上下文信息。`rules/` 是按领域拆分的编码约束，粒度更细，可以按需加载。

实际使用建议：**用 CLAUDE.md 写"是什么"，用 rules/ 写"怎么做"**。

### 多个 CLAUDE.md 如何合并？

Claude Code 从工作目录向上遍历，加载路径上所有 `CLAUDE.md`。子目录的 `CLAUDE.md` 与父目录的会拼接在一起，但不会覆盖。

Monorepo 场景下的典型布局：

```text
monorepo/
 ├── CLAUDE.md                # "所有包的通用规范"
 ├── packages/web/CLAUDE.md   # "Web 包的技术栈与约定"
 └── packages/api/CLAUDE.md   # "API 包的技术栈与约定"
```

当你在 `packages/web/` 下工作时，两个文件都会被加载。

### Skill 和 Command 有什么区别？

| | Command | Skill |
| --- | --- | --- |
| 复杂度 | 单一对话轮次 | 多步骤工作流 |
| 定义方式 | 单个 Markdown Prompt | SKILL.md + 可选资源文件 |
| 触发方式 | `/command-name` | 自动关键词触发 或 `/skill-name` |
| 适用场景 | 固定流程（审查、部署） | 领域专长（PDF 处理、安全审计） |

---

## 参考资源

- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code CLI 源码](https://github.com/anthropics/claude-code)
- [Skills 使用指南](../../skills/index.md)
- [Claude API 参考](../../skills/claude-api.md)
