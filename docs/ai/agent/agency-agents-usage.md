---
description: The Agency 实战使用指南 — 从安装配置到 Agent 激活，从单角色调用到多 Agent 协作工作流，覆盖 Claude Code 深度集成与 16 个部门的 Agent 选型参考。
---

# The Agency 使用指南

## 概述

[The Agency](https://github.com/msitarzewski/agency-agents) 是一个开源 AI Agent 角色库（MIT 协议，118k+ Stars），提供 **232 个预定义的专业 Agent 角色**，覆盖 16 个领域。每个 Agent 是一个精心编写的 Markdown 文件，定义了角色的身份、使命、工作流程和质量标准。

**核心理念**：不再写"你是一个前端开发者，帮我做页面"——而是直接激活一个拥有完整人格、明确约束和质量标准的专业 Agent。

本文是一份**纯实战指南**，从安装到高级工作流，每一步都可操作。

## 快速开始（5 分钟）

```bash
# 1. 克隆仓库
git clone https://github.com/msitarzewski/agency-agents.git
cd agency-agents

# 2. 安装到 Claude Code（仅工程部门）
./scripts/install.sh --tool claude-code --division engineering

# 3. 在 Claude Code 对话中激活 Agent
# "Activate Frontend Developer mode，帮我重构 Dashboard 页面"
# "Activate Backend Architect mode，设计用户系统的数据库 Schema"
```

安装完成后，Agent 文件位于 `~/.claude/agents/`，Claude Code 在对话中可以直接引用。

## 安装详解

### 安装方式对比

| 方式 | 适用场景 | 复杂度 |
|------|---------|--------|
| **桌面应用**（推荐新手） | macOS/Linux/Windows，可视化浏览和安装 | 最低 |
| **install.sh 脚本** | 需要精细控制安装范围和目标工具 | 中等 |
| **手动复制** | 只需要个别 Agent，或参考格式自己写 | 低 |
| **convert.sh + install.sh** | Gemini CLI、Kimi、Codex 等需要格式转换的工具 | 中等 |

### 方式一：桌面应用

```bash
# macOS Homebrew
brew install --cask msitarzewski/agency-agents/agency-agents

# 或从 GitHub Releases 下载
# https://github.com/msitarzewski/agency-agents-app/releases/latest
```

桌面应用提供图形化界面，可以浏览所有 Agent、按部门筛选、一键安装到检测到的工具中，并自动更新。

### 方式二：脚本安装（推荐开发者）

**交互式安装**（自动检测已安装的工具）：

```bash
cd agency-agents
./scripts/install.sh
```

交互界面会扫描系统中已安装的 AI 工具，显示复选框菜单，勾选目标工具后回车即可。

**非交互式安装**（适合 CI/脚本）：

```bash
# 安装全部 Agent 到所有检测到的工具
./scripts/install.sh --no-interactive --tool all

# 仅安装到 Claude Code
./scripts/install.sh --no-interactive --tool claude-code

# 仅安装特定部门
./scripts/install.sh --tool claude-code --division engineering,security,testing

# 仅安装特定 Agent
./scripts/install.sh --tool claude-code --agent frontend-developer,backend-architect

# 预览安装计划（不实际写入文件）
./scripts/install.sh --tool claude-code --division engineering --dry-run
```

**并行安装**（加速大量 Agent 的安装）：

```bash
./scripts/install.sh --no-interactive --parallel --tool all
./scripts/install.sh --no-interactive --parallel --jobs 4 --tool claude-code,cursor
```

### 方式三：手动复制

```bash
# 安装单个 Agent
cp engineering/engineering-frontend-developer.md ~/.claude/agents/

# 安装整个部门
cp engineering/*.md ~/.claude/agents/

# 安装到项目级（团队共享）
cp engineering/engineering-frontend-developer.md .claude/agents/
```

### 支持的 AI 工具

| 工具 | 安装标志 | 目标路径 | 备注 |
|------|---------|---------|------|
| **Claude Code** | `--tool claude-code` | `~/.claude/agents/` | 原生支持，无需转换 |
| GitHub Copilot | `--tool copilot` | `~/.github/agents/` | 原生支持 |
| Cursor | `--tool cursor` | `.cursor/rules/` | 项目级，生成 `.mdc` 文件 |
| Windsurf | `--tool windsurf` | `.windsurfrules` | 项目级 |
| Aider | `--tool aider` | `CONVENTIONS.md` | 项目级，所有 Agent 合并到单文件 |
| Antigravity | `--tool antigravity` | 生成 `SKILL.md` | 每个 Agent 生成独立 Skill |
| Gemini CLI | `--tool gemini-cli` | 需 `convert.sh` | 需先运行转换 |
| OpenCode | `--tool opencode` | `.opencode/agents/` | **注意：有约 119 个 Agent 上限** |
| Kimi Code | `--tool kimi` | `~/.config/kimi/agents/` | 转换为 YAML 格式 |
| Codex | `--tool codex` | `~/.codex/agents/` | 转换为 TOML 格式 |
| Qwen Code | `--tool qwen` | `.qwen/agents/` | 需 `convert.sh` |

### 符号链接模式

```bash
# 使用符号链接而非复制，源文件更新自动同步
./scripts/install.sh --tool claude-code --link
```

适合经常 `git pull` 更新 Agent 的用户。修改 Agent 文件后直接提交 PR，无需重新安装。

### 自定义安装路径

```bash
# 指定目标目录
./scripts/install.sh --tool claude-code --path /custom/path/agents

# 或通过环境变量
export CLAUDE_CONFIG_DIR=/custom/path
./scripts/install.sh --tool claude-code
```

## Agent 部门总览

### 16 个部门速查

| 部门 | Agent 数 | 代表角色 | 典型场景 |
|------|---------|---------|---------|
| **Engineering** | 33 | Frontend Developer, Backend Architect, Code Reviewer | 软件开发全流程 |
| **Design** | ~10 | UI Designer, UX Researcher, Design System Architect | 界面设计与设计系统 |
| **Marketing** | ~15 | Growth Hacker, Content Strategist, SEO Specialist | 增长与营销 |
| **Testing** | ~8 | QA Engineer, Reality Checker, Evidence Collector | 质量保证 |
| **Product** | ~10 | Product Manager, Product Strategist | 产品规划 |
| **Project Management** | ~8 | Senior Project Manager, Scrum Master | 项目交付 |
| **Security** | ~8 | Security Auditor, Penetration Tester | 安全审查 |
| **Sales** | ~10 | Sales Strategist, Demo Creator | 销售支持 |
| **Finance** | ~8 | Financial Analyst, CFO Advisor | 财务分析 |
| **Support** | ~6 | Customer Service, Support Responder | 客户支持 |
| **Game Development** | ~10 | Game Designer, Unity Developer | 游戏开发 |
| **GIS** | ~6 | GIS Analyst, Drone Mapping Specialist | 地理信息系统 |
| **Spatial Computing** | ~5 | XR Interface Architect, 3D Scene Developer | VR/AR/空间计算 |
| **Paid Media** | ~6 | PPC Strategist, Ad Creative Strategist | 付费广告 |
| **Academic** | ~5 | Research Assistant, Grant Writer | 学术研究 |
| **Specialized** | ~40 | MCP Builder, Legal Document Reviewer, Cultural Intelligence Strategist | 垂直领域专用 |

### 五个最常用的 Agent

#### 1. Frontend Developer (`engineering/engineering-frontend-developer.md`)

```bash
cp engineering/engineering-frontend-developer.md ~/.claude/agents/
```

激活后使用：

```
Activate Frontend Developer mode

帮我重构用户 Dashboard 页面：
- 使用 React + TypeScript
- 虚拟滚动处理 10k+ 数据行
- WCAG 2.1 AA 可访问性合规
- 移动端响应式，320px 起
```

关键约束：性能优先（3G 下 < 3s）、可访问性非协商、移动端优先、禁用占位符注释。

#### 2. Backend Architect (`engineering/engineering-backend-architect.md`)

```bash
cp engineering/engineering-backend-architect.md ~/.claude/agents/
```

激活后使用：

```
Activate Backend Architect mode

设计电商系统的订单服务架构：
- 考虑高并发（10k QPS）
- API 版本化策略
- 数据库 Schema 设计
- 零停机迁移方案
```

关键约束：安全优先、API 向后兼容、零停机迁移、内建可观测性。

#### 3. UI Designer (`design/design-ui-designer.md`)

```bash
cp design/design-ui-designer.md ~/.claude/agents/
```

激活后使用：

```
Activate UI Designer mode

为 SaaS 产品创建 Design System：
- 设计 Token 体系（颜色/字体/间距/阴影）
- 核心组件规范（Button/Input/Card/Modal）
- 暗色主题支持
- 响应式断点：320 / 640 / 768 / 1024 / 1280
```

#### 4. Growth Hacker (`marketing/marketing-growth-hacker.md`)

```bash
cp marketing/marketing-growth-hacker.md ~/.claude/agents/
```

激活后使用：

```
Activate Growth Hacker mode

分析我们产品的增长漏斗，设计 10 个可执行的增长实验：
- 当前转化率：Landing → Signup 12%，Signup → Active 25%
- 目标：月活从 5k 提升到 20k
- 预算：$5k/月
```

量化标准：月环比增长 20%+、K-factor > 1.0、LTV:CAC > 3:1、每月 10+ 实验。

#### 5. Reality Checker (`testing/testing-reality-checker.md`)

```bash
cp testing/testing-reality-checker.md ~/.claude/agents/
```

激活后使用：

```
Activate Reality Checker mode

验收 PR #234 的前端重构：
- 检查视觉一致性（3 个设备尺寸）
- 验证所有交互功能
- 交叉比对 UI Designer 的规范
- 默认 NEEDS WORK，需要压倒性证据才能 PASS
```

## 常用工作流配方

### 配方一：全栈功能开发（3 Agent 协作）

```
你：设计用户认证系统，包括注册、登录、密码重置

Session 1 — Backend Architect:
  "Activate Backend Architect mode
   设计认证系统的 API、数据库 Schema、JWT 策略"

  产出 → API 设计文档 + Schema DDL + 安全策略

Session 2 — Frontend Developer（拿到后端设计后）:
  "Activate Frontend Developer mode
   基于后端 API 设计文档，实现用户认证的前端页面"

  产出 → React 组件 + 表单验证 + Token 管理

Session 3 — Reality Checker（拿到前后端产出后）:
  "Activate Reality Checker mode
   验收认证系统：视觉一致性、交互完整性、安全基础检查"

  产出 → 验收报告 + 问题清单
```

### 配方二：MVP 快速验证（5 Agent 并行分析）

```
你：我有一个 SaaS 想法，帮我做产品发现和 MVP 规划

Session 1 — 并行分析阶段:
  同时咨询：
  - Product Manager → 市场需求与竞品分析
  - Backend Architect → 技术可行性评估
  - UI Designer → 核心页面视觉方向
  - Growth Hacker → 早期获客策略
  - Reality Checker → 风险点与假设验证

Session 2 — 汇总阶段:
  "基于以上 5 个 Agent 的分析，生成一份统一的 MVP 方案，
   包含产品定位、技术选型、UI 方向、增长策略、风险清单"
```

### 配方三：代码审查流水线（2 Agent Gate）

```
Session 1 — Code Reviewer:
  "Activate Code Reviewer mode
   审查 src/ 目录下本次 PR 的所有改动
   关注：安全问题、性能隐患、代码可维护性"

  产出 → 审查报告（问题分级 + 修复建议）

Session 2 — Reality Checker（交叉验证）:
  "Activate Reality Checker mode
   验证 Code Reviewer 的审查报告：
   - 每个 HIGH 级问题是否确实存在
   - Reviewer 是否遗漏了安全或性能问题
   - 改动是否满足了原始需求"
```

### 配方四：Design System 从零到一（3 阶段流水线）

```
Phase 1 — UI Designer:
  "Activate UI Designer mode
   为产品创建 Design System：Token、组件库、暗色主题"

  产出 → 设计 Token + 组件规范 + 设计稿

Phase 2 — Frontend Developer:
  "Activate Frontend Developer mode
   基于 Design System 输出，实现组件库代码"

  产出 → React 组件库 + Storybook + 文档

Phase 3 — Reality Checker:
  "Activate Reality Checker mode
   验证组件库实现与设计规范的像素级一致性"
```

## Claude Code 深度集成

### Agent 文件的存放位置

```
~/.claude/agents/          # 用户级，所有项目可用
.claude/agents/            # 项目级，团队共享
```

**优先级**：项目级覆盖用户级。如果两级都有同名的 Agent，项目级生效。

### 激活 Agent 的三种方式

**方式一：对话中直接激活**

```
Activate Frontend Developer mode
Activate Reality Checker mode
```

这是最直接的方式。Claude Code 会读取 Agent 文件并将其人格和约束注入当前会话。

**方式二：在 CLAUDE.md 中预设**

```markdown
# .claude/CLAUDE.md

## Active Agents
- Frontend Developer（engineering-frontend-developer.md）
- Reality Checker（testing-reality-checker.md）

当涉及前端开发时，自动以前端开发者角色响应。
在交付前，自动执行 Reality Check 审查。
```

**方式三：通过 `--agents` 标志启动**

```bash
claude --agents frontend-developer,reality-checker
```

### Agent + Skills 组合使用

Agent 定义**你是谁**，Skill 提供**你会什么**。两者天然互补：

```
场景：开发一个品牌 Landing Page

Agent: Frontend Developer（人格 + 前端约束）
Skills:
  ├── taste-skill       （设计约束：禁 Inter 字体、禁紫色渐变、禁居中卡片）
  ├── frontend-design   （风格指导：氛围、排版、配色方向）
  └── web-quality       （质量检查：无障碍、性能）
```

实践建议：

```markdown
# .claude/CLAUDE.md

## 默认 Agent
- Frontend Developer

## 默认 Skills
- taste-skill（DESIGN_VARIANCE=6, MOTION_INTENSITY=4, VISUAL_DENSITY=5）
- web-quality（每次交付前自动检查无障碍与性能）

## 审查 Agent
- Reality Checker（在 PR 提交前激活，默认 NEEDS WORK）
```

### 管理大量 Agent

安装 232 个 Agent 后，按需激活是关键：

```bash
# 查看已安装的 Agent
ls ~/.claude/agents/

# 按部门查看
ls ~/.claude/agents/ | grep engineering
ls ~/.claude/agents/ | grep testing

# 临时禁用某个 Agent（重命名）
mv ~/.claude/agents/engineering-prompt-engineer.md \
   ~/.claude/agents/engineering-prompt-engineer.md.disabled
```

实用建议：**只安装你真正会用的部门**——用 `--division` 标志按需安装：

```bash
# 最小推荐安装：工程 + 测试 + 设计
./scripts/install.sh --tool claude-code --division engineering,testing,design

# 全栈开发者：工程 + 测试 + 设计 + 产品
./scripts/install.sh --tool claude-code --division engineering,testing,design,product

# 创业者：工程 + 产品 + 营销 + 销售
./scripts/install.sh --tool claude-code --division engineering,product,marketing,sales
```

## 自定义 Agent

### 修改现有 Agent

```bash
# 直接编辑已安装的 Agent 文件
vim ~/.claude/agents/engineering-frontend-developer.md
```

常见的修改点：

- **技术栈偏好**：把 React 换成 Vue/Svelte
- **质量标准**：调整性能指标（3s → 2s）
- **禁用约束**：移除不适用的 FAIL 条件
- **添加项目约定**：在 Critical Rules 中加入项目特有的规范

### 基于模板创建新 Agent

参考 The Agency 的格式创建自己的 Agent：

```bash
# 复制一个现有 Agent 作为模板
cp ~/.claude/agents/engineering-frontend-developer.md \
   ~/.claude/agents/my-custom-agent.md

# 编辑
vim ~/.claude/agents/my-custom-agent.md
```

详细的角色设计方法论参考 [Agent 角色设计指南](./agent-persona-design.md)。

### 提交自定义 Agent 到团队仓库

```bash
# 将自定义 Agent 放入项目的 .claude/agents/ 目录
cp my-custom-agent.md /path/to/project/.claude/agents/

# 提交到 Git
cd /path/to/project
git add .claude/agents/my-custom-agent.md
git commit -m "add custom agent: my-custom-agent"
```

团队其他成员 `git pull` 后即可使用。

## 更新与维护

```bash
# 更新 Agent 库到最新版本
cd agency-agents
git pull

# 如果使用符号链接安装，更新自动生效
# 如果使用复制安装，需要重新安装
./scripts/install.sh --no-interactive --tool claude-code

# 查看最新版本
git log -1 --oneline
```

## 常见问题

### Q: Agent 输出质量不稳定怎么办？

1. **检查激活方式**：确保在对话开头就激活 Agent，而非中途切换
2. **强化约束**：在 Critical Rules 中增加更具体的禁止项
3. **叠加 Skills**：Agent 管人格，Skill 管能力，两者配合效果更好
4. **引入审查 Agent**：用 Reality Checker 做最终验收

### Q: 多个 Agent 的约束冲突怎么办？

例如 Frontend Developer 要求"移动端优先"，但 UI Designer 的规范针对桌面端。

**解法**：在 CLAUDE.md 中明确优先级：

```markdown
## Agent 优先级
1. Reality Checker（最高优先级，否决权）
2. Frontend Developer（实现层面）
3. UI Designer（视觉层面，与 Frontend 冲突时 Frontend 优先）
```

### Q: Agent 安装后对话中不生效？

1. 检查文件路径是否正确：`ls ~/.claude/agents/`
2. 确认文件名格式：Agent 文件应为 `.md` 格式
3. 确认激活措辞：使用 `Activate <Agent Name> mode` 格式
4. 检查 Agent 文件的 frontmatter 是否完整

### Q: OpenCode 安装超过 119 个 Agent 怎么办？

这是 OpenCode 的已知 bug。Solution：使用 `--division` 分批安装，每次不超过 119 个：

```bash
./scripts/install.sh --tool opencode --division engineering,design,testing
```

安装脚本会自动警告选择是否超出此限制。

## 参考资源

- [The Agency GitHub 仓库](https://github.com/msitarzewski/agency-agents)
- [The Agency 桌面应用](https://agencyagents.app)
- [Agent 角色设计指南](./agent-persona-design.md) — 如何从零设计一个 Agent
- [多 Agent 协作模式](./multi-agent-collaboration.md) — Agent 之间的协作架构
- [AI Agent 概述](./index.md) — Agent 基础概念与架构
