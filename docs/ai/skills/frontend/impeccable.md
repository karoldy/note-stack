---
description: impeccable — 40k+ Stars 的设计语言 Skill，23 个设计命令 + 44 条确定性检测规则 + 设计系统初始化，让 AI 产出摆脱模板化的 UI。
---

# Impeccable

## 概述

`impeccable` 是 Paul Bakaus 创建的 AI 设计语言 Skill（40k+ Stars），为 AI 编码助手注入专业的 UI/UX 设计判断力。它以 Anthropic 的 `frontend-design` Skill 为起点，并大幅扩展：23 个统一的设计命令、一键项目初始化、44 条无需 LLM 即可运行的确定性检测规则，以及浏览器端实时视觉迭代能力。

核心理念：**所有 AI 模型都训练在相同的 SaaS 模板上**，不加引导就会产出千篇一律的 UI（Inter 字体、紫蓝渐变、卡片套卡片）。Impeccable 通过项目级设计上下文（`PRODUCT.md` + `DESIGN.md`）让 AI 产出有品味、有个性的设计。

- **分类**：前端 / 设计 & 创意
- **调用方式**：`/impeccable <command> <target>`
- **来源**：社区（[pbakaus/impeccable](https://github.com/pbakaus/impeccable)）

## 触发条件

以下场景应调用该 Skill：

- 新项目启动，需要建立设计系统与视觉方向
- 审查现有 UI 的设计质量、可访问性或性能
- 打磨即将上线的页面（最终设计对齐）
- 设计过于平淡需要放大，或过于张扬需要收敛
- 添加动效、微交互或视觉亮点
- 处理错误状态、空状态、国际化等边缘场景
- CI 中检测 AI 生成代码的设计反模式

以下场景**不应**使用：

- 纯后端逻辑开发
- 已有严格企业设计系统的项目（可能与 Impeccable 建议冲突）
- 仅修改文案内容，不涉及视觉变更

## 核心能力

### 23 个设计命令

所有命令通过 `/impeccable` 统一调用：

| 命令 | 功能 |
|------|------|
| `/impeccable init` | **一次性初始化**：收集设计上下文，生成 PRODUCT.md 和 DESIGN.md |
| `/impeccable craft` | 完整"塑形→构建→视觉迭代"流程 |
| `/impeccable shape` | 在写代码前规划 UX/UI |
| `/impeccable document` | 从现有项目代码反向生成 DESIGN.md |
| `/impeccable extract` | 将可复用组件和 Token 提取到设计系统 |
| `/impeccable critique` | UX 设计审查（层次、清晰度、情感共鸣） |
| `/impeccable audit` | 技术质量检查（可访问性、性能、响应式） |
| `/impeccable polish` | 最终打磨，设计系统对齐，交付就绪 |
| `/impeccable bolder` | 放大过于平淡的设计 |
| `/impeccable quieter` | 收敛过于张扬的设计 |
| `/impeccable distill` | 剥离到本质，去繁就简 |
| `/impeccable harden` | 错误处理、i18n、文本溢出、边缘情况 |
| `/impeccable onboard` | 首次运行流程、空状态、激活路径 |
| `/impeccable animate` | 添加有意义的动效 |
| `/impeccable colorize` | 引入战略性色彩 |
| `/impeccable typeset` | 修正字体选择、层次、尺寸 |
| `/impeccable layout` | 修正布局、间距、视觉节奏 |
| `/impeccable delight` | 添加令人愉悦的细节 |
| `/impeccable overdrive` | 添加技术上出众的效果 |
| `/impeccable clarify` | 改进不清晰的 UX 文案 |
| `/impeccable adapt` | 适配不同设备 |
| `/impeccable optimize` | 性能优化 |
| `/impeccable live` | 浏览器中实时迭代 UI 变体 |

使用 `/impeccable pin <command>` 可将常用命令固定为独立快捷键（如 `pin audit` → `/audit`）。

### 44 条确定性检测规则

CLI 和浏览器扩展可直接运行，无需 LLM 和 API Key：

```bash
npx impeccable detect src/              # 扫描目录
npx impeccable detect index.html        # 扫描 HTML 文件
npx impeccable detect https://example.com  # 扫描 URL（Puppeteer）
npx impeccable detect --json .          # CI 友好的 JSON 输出
```

检测范围覆盖：
- **AI 模板痕迹**：侧边标签边框、紫蓝渐变、bounce 缓动、暗色光晕
- **通用设计质量**：行长度、紧凑内边距、小触摸目标、跳级标题等

### 设计 Hook（自动检测）

安装时自动为 Claude Code、Cursor、Codex 配置 Hook：编辑 UI 文件后自动运行检测器，将发现的问题反馈到 Agent 流程中。

| 工具 | Hook 机制 |
|------|-----------|
| **Claude Code** | `.claude/settings.local.json` → `hook.mjs` |
| **GitHub Copilot** | `.github/hooks/impeccable.json` → `hook.mjs` |
| **Cursor** | `.cursor/hooks.json` → `hook-before-edit.mjs`（在错误写入前拦截） |
| **Codex** | `.codex/hooks.json` → `hook.mjs` |

## 安装

### CLI 安装（推荐）

```bash
# 从项目根目录运行
npx impeccable install

# 更新已有安装
npx impeccable update
```

安装程序自动检测已安装的 AI 工具（Claude Code、Cursor、Codex 等），支持项目级和全局安装两种模式。

### Git Submodule（团队共享）

```bash
git submodule add https://github.com/pbakaus/impeccable .impeccable
npx impeccable link --source=.impeccable --providers=claude,cursor
git add .gitmodules .impeccable .claude .cursor
git commit -m "Add Impeccable skills"
```

### 手动安装

```bash
# Claude Code（项目级）
cp -r dist/claude-code/.claude your-project/

# Claude Code（全局）
cp -r dist/claude-code/.claude/* ~/.claude/

# Cursor
cp -r dist/cursor/.cursor your-project/

# Codex CLI
cp -r dist/agents/.agents your-project/
mkdir -p your-project/.codex
cp dist/codex/.codex/hooks.json your-project/.codex/hooks.json
```

### 支持的 AI 工具

Claude Code、Cursor、GitHub Copilot、Gemini CLI、Codex CLI、OpenCode、Pi、Kiro、Trae、Rovo Dev、Qoder

## 使用示例

### 项目初始化

```
/impeccable init
```

`init` 会询问项目类型（品牌页 vs 产品页），然后生成设计上下文文件：

```
PRODUCT.md    # 受众、品牌调性、反参考
DESIGN.md     # 颜色、字体、组件规范
```

后续所有命令自动读取这些上下文，确保设计一致性。

### 日常使用

```
/impeccable audit blog             # 审计博客页面
/impeccable critique landing       # UX 设计审查
/impeccable polish settings        # 交付前最终打磨
/impeccable harden checkout        # 添加错误处理 + 边缘情况
/impeccable animate hero           # 为 Hero 区域添加动效
/impeccable bolder pricing         # 让定价页更有视觉冲击力
/impeccable distill dashboard      # 简化 Dashboard 的信息密度
```

### 自由描述模式

```
/impeccable redo this hero section
/impeccable make the CTA more compelling
/impeccable fix the spacing in the footer
```

### 固定快捷键

```
/impeccable pin audit    # 创建 /audit 独立快捷键
/impeccable pin polish   # 创建 /polish 独立快捷键
```

### CLI 检测器

```bash
# CI 集成
npx impeccable detect --json . > design-report.json

# 忽略特定规则
npx impeccable ignores add-value overused-font Inter --reason "Brand font"

# 文件中内联豁免
<!-- impeccable-disable overused-font: 导出的品牌文档 -->
```

## 反模式清单

Impeccable 明确指导 AI 避免以下常见问题：

- 不使用过度使用的字体（Arial、Inter、系统默认字体）
- 不在彩色背景上使用灰色文字
- 不滥用纯黑/纯灰（始终加色调）
- 不将所有内容包裹在卡片中或卡片套卡片
- 不使用 bounce/elastic 缓动（显得过时）
- 避免紫蓝渐变（AI 模板的标志性特征）
- 确保可点击元素有足够的触摸目标

## 最佳实践

- **每个新项目先运行 `/impeccable init`**，生成设计上下文是后续所有命令质量的基础
- **将 `PRODUCT.md` 和 `DESIGN.md` 提交到版本控制**，团队共享设计决策
- **CI 中集成 `npx impeccable detect --json .`**，自动化设计质量门禁
- **渐进式使用命令**：先 `audit` 发现问题 → `critique` 评估设计 → `polish` 最终打磨
- 对大型项目，用 `/impeccable document` 从现有代码反向生成设计系统，而非从零开始
- `bolder` / `quieter` 适合微调阶段，`distill` 适合信息架构重构

## 注意事项

- `init` 生成的设计文件会随时间演进，建议定期用 `/impeccable extract` 同步代码中的实际组件
- Codex 用户安装后需手动打开 `/hooks` 审批项目 Hook
- Cursor 的 Hook 在**写入前**运行（拦截错误），Claude Code 的 Hook 在**编辑后**运行（反馈问题）
- Git Submodule 方式需要 Node.js 环境运行 `npx impeccable link`
- 44 条确定性规则覆盖常见问题，但设计品味相关的审查仍依赖 LLM（`critique` 命令）
- `.impeccable/config.local.json` 是 gitignored 的个人偏好，`.impeccable/config.json` 可提交共享

## 相关 Skills

- [[frontend-design]] — Claude Code 内置设计 Skill，Impeccable 的起点与基础
- [[ui-ux-pro-max]] — 设计系统自动生成引擎，侧重风格数据库与推理，与 Impeccable 的命令式工作流互补
- [[frontend-ui-engineering]] — 前端 UI 工程化实践
- [[web-quality]] — Web 质量审计，Impeccable 的 `audit` 命令覆盖可访问性与性能维度

## 参考资源

- [官方网站](https://impeccable.style)
- [GitHub 仓库](https://github.com/pbakaus/impeccable)
- [npm 包](https://www.npmjs.com/package/impeccable)
- [设计检测器文档](https://impeccable.style/docs/detector)
- [设计 Hook 文档](https://impeccable.style/docs/hooks)
