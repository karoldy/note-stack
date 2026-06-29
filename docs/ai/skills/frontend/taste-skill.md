---
description: taste-skill — 52.6k+ Stars 的反 Slop 前端框架，提供 10+ 变体 Skill、3 个可调参数旋钮（设计方差/动效强度/视觉密度）及图片生成管线，让 AI 生成脱离模板化的生产级界面。
---

# Taste Skill

## 概述

`taste-skill` 是 **Leonxlnx** 打造的便携式 Agent Skill 集合（MIT 协议，**52.6k+ Stars**），核心理念是"Anti-Slop Frontend Framework"——防止 AI 编码 Agent 产出千篇一律的低质量界面。它通过多个专用变体 Skill、3 个可调参数旋钮以及图片生成管线，覆盖从绿场开发到旧项目重设计的完整前端工作流。

与 [[frontend-design]] 和 [[ui-ux-pro-max]] 不同，taste-skill 更强调**行为约束**而非风格推荐——它直接告诉 Agent "不要做什么"（禁用 Inter 字体、禁止紫色渐变、禁止占位符注释），并强制生成完整、可运行的代码。

- **分类**：前端 / 设计 & 创意
- **调用方式**：安装后自动触发，或显式引用 Skill 名称
- **来源**：社区（[Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)）

## 触发条件

以下场景应调用该 Skill：

- 创建新的前端页面、Landing Page 或 Dashboard
- 需要独特视觉风格而非通用 AI 模板的 UI
- 对现有项目进行 UI 重设计或视觉升级
- Agent 频繁输出截断代码、占位符注释（配合 output-skill）
- 需要先生成设计参考图再编码的图片驱动工作流
- 已确定视觉方向（极简/粗野主义/高端奢华），需要对应风格约束

以下场景**不应**使用：

- 纯后端 API 开发或命令行工具
- 已有成熟设计系统且不希望引入冲突的企业项目
- 仅需简单原型验证功能的快速迭代阶段

## 核心理念

taste-skill 的独特之处在于它不只是"建议"，而是**强制执行**设计约束：

```
设计意图推断 → 参数旋钮调节 → 反模式禁令 → 完整代码输出
     │               │                │              │
     读懂需求        调风格          禁模板         无截断
```

### 三大可调参数

主 Skill（v2）在文件顶部暴露三个 1–10 的数值旋钮，用户可按需调节：

| 参数 | 说明 | 低值 (1-3) | 高值 (8-10) |
| --- | --- | --- | --- |
| `DESIGN_VARIANCE` | 布局实验性 | 居中、规整、保守 | 不对称、重叠、现代感 |
| `MOTION_INTENSITY` | 动效深度 | 仅 hover 微交互 | 滚动驱动、磁吸效果、GSAP 动画 |
| `VISUAL_DENSITY` | 信息密度 | 宽敞、大量留白 | 密集 Dashboard、数据面板 |

### 反模式禁令

taste-skill 明确禁止以下 AI 常见陋习：

- **禁用 Inter/Roboto/Arial** 等系统默认字体
- **禁用紫色渐变**作为默认配色方案
- **禁止居中卡片布局**（默认不居中一切）
- **禁止占位符注释**（`// TODO`、`// Add your code here`）
- **禁止截断输出**（必须生成完整代码，不可用 `...` 省略）

## Skill 变体

taste-skill 提供 10+ 个专用变体，按场景选用：

### 代码生成类

| Skill | 安装名 | 适用场景 |
| --- | --- | --- |
| **taste-skill (v2)** | `design-taste-frontend` | **默认首选**，通用前端开发，自动推断设计语言 |
| **taste-skill-v1** | `design-taste-frontend-v1` | 依赖 v1 精确行为的存量项目 |
| **gpt-taste** | `gpt-taste` | GPT/Codex 专用，更高布局方差、更强 GSAP 方向 |
| **image-to-code** | `image-to-code` | 图片驱动管线：生成参考图 → 分析 → 编码 |
| **redesign-skill** | `redesign-existing-projects` | 存量项目 UI 审计 → 修复布局/间距/层级/样式 |
| **soft-skill** | `high-end-visual-design` | 高端精致 UI：柔和对比、大量留白、高级字体、弹性动效 |
| **minimalist-skill** | `minimalist-ui` | 编辑型产品风（Notion/Linear 既视感），克制配色、清晰结构 |
| **brutalist-skill** | `industrial-brutalist-ui` | 工业粗野风：瑞士字体、锐利对比、实验性布局 |
| **output-skill** | `full-output-enforcement` | Agent 频繁截断输出时使用，强制完整代码 |
| **stitch-skill** | `stitch-design-taste` | Google Stitch 兼容规则，支持导出 DESIGN.md |

### 图片生成类（产出设计图，不含代码）

| Skill | 安装名 | 适用场景 |
| --- | --- | --- |
| **imagegen-frontend-web** | `imagegen-frontend-web` | 网站设计稿：Hero、Landing、多段式页面 |
| **imagegen-frontend-mobile** | `imagegen-frontend-mobile` | 移动端界面：iOS/Android/跨平台 Mockup |
| **brandkit** | `brandkit` | 品牌套件：Logo 方向、配色板、字体、VI 应用 |

### 变体选择指南

```
绿场项目（无特殊风格要求） → taste-skill (v2)
绿场项目（已确定风格方向） → soft / minimalist / brutalist
存量项目重设计             → redesign-skill
Agent 频繁输出截断         → output-skill（叠加其他 Skill）
图片驱动工作流             → imagegen-* → image-to-code
GPT/Codex 环境             → gpt-taste
依赖 v1 行为               → taste-skill-v1
Google Stitch 集成         → stitch-skill
```

## 安装

### CLI 安装（推荐）

```bash
# 安装全部 Skill
npx skills add https://github.com/Leonxlnx/taste-skill

# 仅安装指定 Skill（使用安装名，非文件夹名）
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
npx skills add https://github.com/Leonxlnx/taste-skill --skill "high-end-visual-design"
npx skills add https://github.com/Leonxlnx/taste-skill --skill "redesign-existing-projects"
```

### 手动安装

将任意 `SKILL.md` 文件复制到项目或对话中：

```bash
# 项目级
cp skills/taste-skill/SKILL.md /path/to/project/.claude/skills/

# 用户级
cp skills/taste-skill/SKILL.md ~/.claude/skills/
```

### 版本升级

v1 → v2 升级无需脚本变更，重新执行安装命令即可（安装名 `design-taste-frontend` 未变）。如需锁定 v1：

```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend-v1"
```

## 使用示例

### 基础用法

安装后 Skill 自动生效，直接在对话中描述需求：

```
帮我做一个 AI 聊天产品的 Landing Page

做一个个人博客首页，要有独特的视觉风格

为 SaaS 产品设计一个 Analytics Dashboard
```

### 指定风格方向

```
做一个极简风格的作品集网站（触发 minimalist-skill）

做一个粗野主义风格的创意工作室首页（触发 brutalist-skill）

做一个高端奢侈品品牌官网，要精致、优雅（触发 soft-skill）
```

### 图片驱动工作流

```bash
# 第 1 步：生成设计参考图
# 对话中："follow imagegen-frontend-web: generate hero, features, and pricing sections for a SaaS landing page"

# 第 2 步：分析图片并编码
# 对话中："follow image-to-code-skill: analyze the generated images and implement the frontend"

# 或一步到位
# 对话中："follow the skill: generate images, then analyze, then code"
```

### 存量项目重设计

```bash
# 安装 redesign-skill
npx skills add https://github.com/Leonxlnx/taste-skill --skill "redesign-existing-projects"

# 在项目目录下启动 Claude Code，Skill 会：
# 1. 审计现有 UI（布局、间距、层级、样式）
# 2. 输出改进清单
# 3. 逐项修复
```

### 调参示例

在主 Skill 的 `SKILL.md` 文件中修改参数值：

```
DESIGN_VARIANCE = 8    # 更高布局实验性，不对称、重叠排版
MOTION_INTENSITY = 7   # 丰富动效：滚动视差、磁吸交互、GSAP 序列
VISUAL_DENSITY = 3     # 低信息密度：宽松留白，适合营销 Landing Page
```

## 最佳实践

- **默认从 v2 开始**，只有遇到兼容性问题时才回退到 v1
- **绿场项目用 taste-skill，存量项目用 redesign-skill**，不要混用
- 图片生成类 Skill（imagegen-*）产出的是设计图，需要配合 image-to-code 完成编码
- **output-skill 按需叠加**：当 Agent 频繁输出截断代码时，叠加安装 output-skill 强制执行完整输出
- 调参时**每次只改一个旋钮**，观察效果后再调下一个，避免参数组合不可控
- 在 `CLAUDE.md` 中声明项目默认的风格偏好和品牌约束，Skill 会在约束框架内发挥
- 搭配 [[frontend-design]] 和 [[ui-ux-pro-max]] 使用时，taste-skill 负责**行为约束**（不做什么），前者负责**风格推荐**（做什么）

## 注意事项

- **v2 仍在积极迭代中**（target v2.0.0 stable），API 可能微调，注意关注 CHANGELOG
- GPT/Codex/Codex CLI 环境下建议使用 **gpt-taste** 变体，规则更严格，动效方向更强
- ChatGPT 使用图片生成 Skill 时需**手动附加或粘贴 SKILL.md 内容**
- taste-skill 的设计约束**框架无关**，但具体代码实现质量取决于 Agent 对目标框架的掌握程度
- 与 [[frontend-design]] 同时安装时可能产生风格冲突（两者都禁止 Inter 字体、紫色渐变是协同的，但美学方向可能矛盾），建议明确主次
- **没有官方 Token 或加密货币项目**，任何以此名义发行的代币均为假冒

## 相关 Skills

- [[frontend-design]] — Anthropic 官方前端设计 Skill，互补于 taste-skill 的行为约束
- [[ui-ux-pro-max]] — 67 种 UI 风格 + 161 套配色数据库，与 taste-skill 的风格变体形成互补
- [[frontend-ui-engineering]] — UI 工程化落地，taste-skill 管设计约束，此 Skill 管工程质量
- [[web-quality]] — 无障碍与性能验证，可作为 taste-skill 产出代码的质量检查

## 参考资源

- [GitHub 仓库](https://github.com/Leonxlnx/taste-skill)
- [官方网站](https://tasteskill.dev)
- [CHANGELOG](https://github.com/Leonxlnx/taste-skill/blob/main/CHANGELOG.md)
- [Research 研究文档](https://github.com/Leonxlnx/taste-skill/tree/main/research)
- [作者 X (Twitter)](https://x.com/lexnlin)
