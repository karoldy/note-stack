---
description: ui-ux-pro-max — 95k+ Stars 的设计智能 Skill，提供 67 种 UI 风格、161 套色彩方案、57 组字体搭配及设计系统自动生成引擎，支持跨平台 UI/UX 开发。
---

# UI UX Pro Max

## 概述

`ui-ux-pro-max` 是社区最受欢迎的设计智能 Skill（95k+ Stars），由 NextLevelBuilder 团队维护。它为 AI 编码助手注入专业级 UI/UX 设计知识，覆盖 67 种 UI 风格、161 套行业专属色彩方案、57 组字体搭配及 99 条 UX 准则。v2.0 新增**设计系统生成引擎**，可根据产品类型自动推理并输出完整的设计体系（布局模式、配色、字体、动效、反模式清单）。

- **分类**：前端 / 设计 & 创意
- **调用方式**：自动触发（提及 UI/UX 需求时）或 `/ui-ux-pro-max`
- **来源**：社区（[nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)）

## 触发条件

以下场景应调用该 Skill：

- 构建 Landing Page、Dashboard、SaaS 产品界面
- 设计移动端 App UI（iOS/Android）
- 创建作品集、博客、电商等网站视觉设计
- 改进现有 UI 的视觉风格或交互体验
- 为新项目确定设计系统（配色、字体、组件风格）
- UI/UX Review 或可访问性审计

以下场景**不应**使用：

- 纯后端 API 开发
- 不需要视觉设计的脚本/工具开发
- 已有成熟设计系统的企业级项目（可能冲突）

## 核心能力

### 设计智能数据库

| 类别 | 数量 | 说明 |
| --- | --- | --- |
| **推理规则** | 161 条 | 按行业分类的设计规则（SaaS、金融、医疗、电商等） |
| **UI 风格** | 67 种 | Glassmorphism、Brutalism、Neumorphism、Bento Grid、AI-Native 等 |
| **色彩方案** | 161 套 | 与 161 种产品类型 1:1 对齐的行业专属调色板 |
| **字体搭配** | 57 组 | 精选 Google Fonts 组合，含情绪标签 |
| **图表类型** | 25 种 | Dashboard 和分析面板的图表推荐 |
| **技术栈** | 16 种 | React、Vue、Svelte、SwiftUI、Flutter、Angular 等专属指南 |
| **UX 准则** | 99 条 | 最佳实践、反模式、无障碍规则 |

### 设计系统生成引擎（v2.0）

```
用户需求 → 5 路并行搜索 → 推理引擎 → 完整设计系统
              ├── 产品类型匹配（161 分类）
              ├── 风格推荐（67 风格 BM25 排序）
              ├── 色彩方案选择（161 调色板）
              ├── Landing Page 模式（24 种）
              └── 字体搭配（57 组组合）
```

输出内容：推荐布局模式 + UI 风格 + 配色方案 + 字体搭配 + 动效建议 + 反模式警告 + 交付前检查清单

## 安装

### CLI 安装（推荐）

```bash
# 全局安装 CLI
npm install -g uipro-cli

# 在项目中安装到指定 AI 助手
cd /path/to/your/project
uipro init --ai claude      # Claude Code
uipro init --ai cursor      # Cursor
uipro init --ai windsurf    # Windsurf
uipro init --ai copilot     # GitHub Copilot
uipro init --ai gemini      # Gemini CLI
uipro init --ai trae        # Trae
uipro init --ai qoder       # Qoder
uipro init --ai codex       # Codex CLI
uipro init --ai roocode     # Roo Code
uipro init --ai all         # 安装到所有检测到的 AI 助手
```

### Claude Code Marketplace

```bash
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```

### 全局安装

```bash
uipro init --ai claude --global   # 安装到 ~/.claude/skills/（对所有项目生效）
```

### 前置依赖

需要 Python 3.x（用于设计系统搜索脚本）：

```bash
python3 --version                # 检查版本
brew install python3             # macOS
sudo apt install python3         # Ubuntu/Debian
winget install Python.Python.3.12  # Windows
```

## 使用示例

### 基础用法（自动触发）

只需在对话中自然描述 UI/UX 需求：

```
Build a landing page for my SaaS product

Create a dashboard for healthcare analytics

Design a portfolio website with dark mode

Make a mobile app UI for e-commerce

Build a fintech banking app with dark theme
```

### 指定技术栈

在 Prompt 中提及偏好的技术栈即可：

```
Build a landing page with Next.js and shadcn/ui for my AI chatbot product

Create an iOS app UI with SwiftUI for a meditation app

Design a dashboard with Vue and Nuxt UI for an analytics platform
```

### 设计系统命令行（高级）

```bash
# 生成 ASCII 格式设计系统
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness" \
  --design-system -p "Serenity Spa"

# 生成 Markdown 格式设计系统
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "fintech banking" \
  --design-system -f markdown

# 领域专项搜索
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "glassmorphism" --domain style
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "elegant serif" --domain typography
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "dashboard" --domain chart

# 技术栈专项指南
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "form validation" --stack react
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "responsive layout" --stack html-tailwind
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "enterprise tableview" --stack javafx
```

### 持久化设计系统

```bash
# 保存到 design-system/MASTER.md（跨会话复用）
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "SaaS dashboard" \
  --design-system --persist -p "MyApp"

# 同时创建页面级覆盖文件
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "SaaS dashboard" \
  --design-system --persist -p "MyApp" --page "dashboard"
```

生成的文件结构：

```
design-system/
├── MASTER.md           # 全局设计源码（颜色、字体、间距、组件）
└── pages/
    └── dashboard.md    # 页面级覆盖（仅记录与 Master 的差异）
```

检索优先级：`pages/[page-name].md` > `MASTER.md`

### 支持的技术栈

| 平台 | 技术栈 |
| --- | --- |
| **Web（默认）** | HTML + Tailwind |
| **React 生态** | React、Next.js、shadcn/ui |
| **Vue 生态** | Vue、Nuxt.js、Nuxt UI |
| **Angular** | Angular |
| **PHP** | Laravel（Blade、Livewire、Inertia.js） |
| **其他 Web** | Svelte、Astro |
| **桌面** | JavaFX |
| **iOS** | SwiftUI |
| **Android** | Jetpack Compose |
| **跨平台** | React Native、Flutter |

## 主要 UI 风格一览

| 风格 | 适用场景 |
| --- | --- |
| **Glassmorphism** | 现代 SaaS、金融 Dashboard |
| **Neumorphism** | 健康/冥想应用 |
| **Brutalism** | 设计作品集、艺术项目 |
| **Bento Box Grid** | Dashboard、产品页、作品集 |
| **AI-Native UI** | AI 产品、聊天机器人、Copilot |
| **Dark Mode (OLED)** | 夜间模式应用、开发工具 |
| **Claymorphism** | 教育应用、儿童应用 |
| **Minimalism & Swiss Style** | 企业应用、Dashboard、文档 |
| **Cyberpunk UI** | 游戏、科技产品、Crypto 应用 |
| **Soft UI Evolution** | 现代企业应用、SaaS |

## 最佳实践

- **先描述产品类型**，让设计系统引擎自动匹配风格，而非手动指定视觉参数
- **使用 `--persist` 持久化设计系统**，确保多页面项目视觉一致性
- 全局安装 CLI 后**为每个项目执行 `uipro init`**，而非复制技能文件
- 定期执行 `uipro update` 获取最新的设计规则和风格
- 将 `design-system/MASTER.md` 加入版本控制，团队共享设计规范
- 指定技术栈以获得框架专属的代码生成建议（而非仅 Tailwind 默认）

## 注意事项

- **Python 3.x 为必需依赖**，用于设计系统搜索脚本（`scripts/search.py`）
- 部分 AI 助手（Trae）需切换到 **SOLO 模式**才能自动激活 Skill
- 旧版本（v2.5.1 之前）可能存在符号链接兼容性问题，建议通过 CLI 安装
- Kiro、GitHub Copilot、Roo Code 需使用**工作流模式**手动调用 `/ui-ux-pro-max`
- 设计系统输出较长时可能被截断，可使用 `--max-length 0` 取消限制
- 该 Skill 偏向于设计指导与风格推荐，不替代完整的设计到代码工作流

## 相关 Skills

- [[frontend-design]] — 前端视觉设计指导，互补于 UI UX Pro Max 的风格数据库
- [[frontend-ui-engineering]] — 前端 UI 工程化实践
- [[shadcn]] — shadcn/ui 组件库，常与 UI UX Pro Max 的设计系统搭配使用
- [[next-best-practices]] — Next.js 最佳实践，Web 技术栈首选配合 Skill
- [[web-quality]] — Web 质量审计，可配合 UI UX Pro Max 的反模式检查使用

## 参考资源

- [官方文档网站](https://uupm.cc)
- [GitHub 仓库](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
- [npm CLI 包](https://www.npmjs.com/package/uipro-cli)
- [NextLevelBuilder 官网](https://nextlevelbuilder.io)
