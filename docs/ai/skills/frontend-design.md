---
description: frontend-design — Anthropic 官方出品的视觉设计 Skill，50K+ Stars，通过独特的美学方向、字体配对、色彩系统与非对称布局，生成脱离 AI 模板感的生产级前端界面。
---

# Frontend Design

## 概述

`frontend-design` 是 **Anthropic 官方**发布的 Claude Code 插件 Skill（`anthropics/skills`），在插件市场中拥有 **52K+ Stars**，被社区广泛认为是前端开发必装 Skill 之首。它的核心目标是让 AI 生成的 UI 脱离千篇一律的"AI Slop"风格 — 不再出现 Inter 字体、紫色渐变、居中卡片布局等模板化特征 — 而是生成具有**独特美学**、**精心设计的字体配对**、**非对称布局**与**有意义动效**的生产级界面。

- **分类**：设计 & 创意
- **调用方式**：`claude plugin add anthropic/frontend-design` 或自动触发
- **来源**：内置（Anthropic 官方）

## 触发条件

以下场景应调用该 Skill：

- 创建新的前端页面或组件
- 需要独特视觉风格的 UI（而非通用模板）
- 用户提到"好看"、"设计感"、"UI"、"界面"、"美化"等关键词
- 对现有界面进行重新设计或视觉升级
- 构建设计系统或主题

以下场景**不应**使用：

- 纯后端 API 开发
- 命令行工具或终端应用
- 不需要视觉设计的脚本或工具函数

## 设计方法论

在编写任何代码之前，Claude 会先确定设计方向：

### 1. 选择美学方向

| 风格 | 特征 |
| --- | --- |
| **Brutalist**（粗野主义） | 原始、大胆的排版，高对比度 |
| **Retro-futuristic**（复古未来） | 霓虹色调、几何形状、科技感 |
| **Editorial**（编辑风） | 优雅排版、宽阔留白、杂志感 |
| **Organic**（自然风） | 柔和的色彩、圆角、流动形态 |
| **Luxury**（奢华风） | 深色调、金色点缀、精致衬线字体 |
| **Nordic Minimal**（北欧极简） | 清冷色彩、大量留白、功能至上 |

### 2. 字体配对

- 避免 Inter、Roboto、Arial、系统默认字体
- 使用 Google Fonts 或自托管独特字体
- 衬线 + 无衬线对比配对
- 展示型字体用于标题，可读性字体用于正文

### 3. 色彩系统

- 使用 CSS 变量统一管理
- 主导色 + 鲜明强调色
- 避免紫色渐变作为默认配色

### 4. 布局策略

- 不对称布局（Asymmetric layouts）
- 元素重叠与越界（Overlap & grid-breaking）
- 宽阔留白（Generous whitespace）
- 不居中一切

### 5. 动效原则

- 交错入场动画（Staggered reveals）
- 滚动驱动的视差效果
- Hover 微交互
- 尊重 `prefers-reduced-motion`

## 使用示例

### 安装

```bash
# 方法 1：Claude Code 插件系统
claude plugin add anthropic/frontend-design

# 方法 2：npm 安装器
npx skills-installer install anthropics/claude-code/frontend-design

# 方法 3：通用更新器
uvx upd-skill anthropics/frontend-design
```

### 使用

Skill 安装后自动生效。当你在对话中描述 UI 需求时，Claude 会自动输出带有独特设计风格的界面代码。

```
"帮我做一个个人博客首页"
"为 SaaS 产品做一个 Landing Page"
"重构这个 Dashboard 让它看起来更专业"
```

## 最佳实践

- 结合 [[frontend-ui-engineering]] — 前者定方向，后者管落地
- 在项目 `CLAUDE.md` 中预设品牌色和字体偏好，让 Skill 在品牌约束下发挥
- 搭配 [[shadcn]] 使用 shadcn/ui 组件时，共同配置设计令牌（CSS 变量）
- 使用 Tailwind CSS 时开启 `@theme` 自定义，将 Skill 的配色建议映射为 Token

## 注意事项

- 该 Skill 倾向"设计优先"，功能实现需要你自己把关
- 复杂的动态交互需要额外的工程实现，Skill 主要指导视觉层面
- 不建议在已有成熟设计系统的项目中强制使用 — 可能在已有风格之上产生冲突
- 生成的设计建议需要结合项目实际约束（组件库、打包方案、浏览器兼容）

## 相关 Skills

- [[frontend-ui-engineering]] — UI 工程化落地
- [[shadcn]] — shadcn/ui 组件库
- [[web-quality]] — 无障碍与性能验证

## 参考资源

- [anthropics/skills 仓库](https://github.com/anthropics/skills/tree/main/skills/frontend-design)
- [Claude Plugins Marketplace](https://claude-plugins.dev/skills/@anthropics/claude-code/frontend-design)
- [Claude Code Frontend Design Toolkit](https://github.com/wilwaldon/Claude-Code-Frontend-Design-Toolkit)
