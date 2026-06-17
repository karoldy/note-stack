---
description: codebase-to-course — 将任意代码仓库转化为自包含的交互式 HTML 课程，专为 Vibe Coder 设计，通过追踪运行时行为而非抽象概念来教授代码工作原理。
---

# codebase-to-course

## 概述

`codebase-to-course` 是由 Zara Zhang 开发的 Claude Code 社区 Skill，能将任意软件代码仓库转化为**单个自包含的交互式 HTML 课程**。它不依赖外部资源，可完全离线使用。

与传统 CS 教育"先背概念 → 多年后才实践"的路径相反，该 Skill 采用 **"先构建，再理解"** 的逆向教学法：通过追踪应用的**真实运行时行为**来教学，而非灌输抽象概念。

- **分类**：社区 Skill（教育 & 可视化）
- **调用方式**：触发短语自动匹配
- **来源**：[社区](https://github.com/zarazhangrui/codebase-to-course)（4.7k+ Stars）
- **安装路径**：`~/.claude/skills/` 或 `.claude/skills/`

## 触发条件

### 触发短语

以下表述会自动激活该 Skill：

- "Turn this codebase into an interactive course"
- "Explain this codebase interactively"
- "Make a course from this project"
- "Teach me how this code works"
- 任何将代码库转化为教程/课程的请求

### 适用场景

- 用 AI 工具构建了能跑起来的项目，但不理解内部原理
- 需要让非技术人员理解代码库的架构与数据流
- 为开源项目生成交互式文档
- 用视觉化方式梳理新接手的项目

### 不适用的场景

- 已经具备传统 CS 背景、只需要 API 参考文档的开发者
- 代码库过小（单文件脚本），不具备"课程化"的复杂度
- 需要实时协作编辑的教学场景

## 输入方式

首次调用时，Skill 会提供三种代码来源选择：

| 输入方式 | 说明 |
| --- | --- |
| 本地文件夹路径 | 直接分析当前项目 |
| GitHub URL | 自动 clone 到 `/tmp/` 后分析 |
| "this codebase" | 使用当前工作目录 |

## 处理流程（4 阶段）

### Phase 1 — 代码库分析

```
读取关键文件 → 追踪数据流 → 识别组件/模块 → 
映射通信模式 → 提取技术栈 → 发现工程巧思 → 标记潜在 Bug
```

Skill 通过**直接阅读代码**来理解应用功能，不会向用户提问。

### Phase 2 — 课程设计

产出 **4-6 个模块**（复杂代码库可达 7-8 个），遵循"由表及里"的 Zoom-in 结构：

| 模块 | 视角 |
| --- | --- |
| 1. 用户可见行为 | 从用户操作出发 |
| 2. 组件/模块拆解 | 前端组件或后端模块的划分 |
| 3. 数据流追踪 | 请求/数据在系统内的流转路径 |
| 4. 外部依赖 | 第三方服务、API、数据库交互 |
| 5. 巧妙模式 | 值得学习的工程技巧 |
| 6. 调试思路 | 常见问题排查路径 |
| 7. 架构全景 | 整体架构决策回顾 |

每个模块要求：3-6 个 Screen、至少 1 个 Code ↔ English 对照、至少 1 个交互元素、1-2 个 CS 洞察 Callout。

**复杂代码库额外步骤（Phase 2.5）**：为每个模块生成 Brief（含预提取的代码片段），供 Subagent 并行编写，无需重新阅读代码库。

### Phase 3 — 构建

产出**目录结构**（非单文件），包含以下文件：

```tree
course-output/
├── index.html              # 由 build.sh 组装
├── _base.html              # 自定义标题、主题色、导航点
├── _footer.html            # 直接复制自 references/
├── styles.css              # 直接复制（不可重新生成）
├── main.js                 # 直接复制（不可重新生成）
├── build.sh                # 直接复制，执行组装
└── modules/
    ├── 01-user-facing-behavior.html   # 仅含 <section class="module">
    ├── 02-components.html
    ├── 03-data-flow.html
    ├── 04-external-dependencies.html
    ├── 05-clever-patterns.html
    └── 06-debugging.html
```

**构建策略**：
- **简单代码库**：顺序编写模块（逐个完成）
- **复杂代码库**：并行分发（最多 3 个模块同时交给 Subagent，每个只收到自己的 Brief 和相关 Reference 片段）

### Phase 4 — 审查

在浏览器中打开 `index.html`，收集内容、设计、交互性三方面的反馈。

## 必选交互元素

每个课程**必须包含全部 5 类交互元素**，不可省略：

### 1. Group Chat 动画

iMessage/微信风格组件对话，消息逐条出现，带动画打字指示器。组件被赋予"角色"个性——不再是抽象方块。

### 2. Message/Data Flow 动画

数据包在组件之间逐步传递的动画，使用 `data-steps='[...]'` JSON 属性定义步骤序列。关键警告：步骤标签中的**单引号会破坏 JSON 解析**，必须避免或 HTML 转义。

### 3. Code ↔ English 翻译块

双栏布局：左栏真实代码（语法高亮），右栏逐行 Plain English 解释。两条硬规则：
- **不允许水平滚动条**——所有代码使用 `white-space: pre-wrap`
- **使用原始代码，一字不改**——学习者能在真实文件中找到完全相同的代码

### 4. 测验

每个模块至少 1 个测验，3-5 道题。**测验考察"做"的能力**，而非"回忆定义"：

- ✅ 场景题："你想添加收藏功能，应该改哪些文件？"
- ✅ 调试题："用户报告 X 坏了，根据你学到的，先查哪里？"
- ✅ 架构决策题："为什么把验证逻辑放在这一层？"
- ❌ 定义题："API 的全称是什么？"
- ❌ 文件名回忆
- ❌ 语法细节

### 5. Glossary Tooltips

**每个技术术语在每个模块首次出现时**必须加 Tooltip（虚线下面线 + `cursor: pointer`）。Hover 显示 1-2 句 Plain English 定义。

"即使只有 1% 的可能非技术用户不知道这个词，也要加 Tooltip。"包括：软件名称（Blender、GIMP）、开发者术语（REPL、JSON、CLI、API、SDK）、编程概念（function、variable、class、module）、基础设施术语（PATH、pip、namespace）、所有缩写。

## 设计系统

### 色彩

| 用途 | 说明 |
| --- | --- |
| 背景 | 暖色调米白（`--color-bg`），偶数/奇数模块交替 |
| 强调色 | 单一醒目暖色（Vermillion / Coral / Teal / Amber / Forest） |
| 代码块 | `#1E2E2E` 深色背景 + Catppuccin 风格语法高亮 |
| 阴影 | 暖色调 RGBA，**不使用纯黑阴影** |

:::danger 设计禁令
**禁止紫色渐变**——这是设计身份的核心约束。
:::

### 字体

| 用途 | 字体 |
| --- | --- |
| 标题 | Bricolage Grotesque（或类似 Bold Geometric 字体） |
| 正文 | DM Sans |
| 代码 | JetBrains Mono |

:::danger 字体禁令
**禁止使用**：Inter、Roboto、Arial、Space Grotesk
:::

### 布局

- 内容宽度：800px / 1000px
- 模块：`min-height: 100dvh`（`100vh` fallback）
- 滚动：`scroll-snap-type: y proximity`（**必须用 proximity，不能用 mandatory**）
- 导航：固定顶部导航栏 + 圆点指示器 + 进度条 + 键盘方向键翻页
- 动画：滚动触发 Reveal（Intersection Observer）+ 自定义缓动曲线

### 视觉密度

- 每段文字最多 2-3 句，需要第 4 句时转为视觉元素
- 每个 Screen 至少 **50% 非段落内容**（图表、代码块、卡片、动画、徽章）
- 3 个以上列表项 → 卡片
- 步骤序列 → 流程图或编号步骤卡片
- 组件交互 → 数据流动画或群聊可视化
- 代码解释 → Code ↔ English 翻译块（**禁止用段落描述代码**）

## 使用示例

### 基础用法

```bash
# 在 Claude Code 中，项目目录下直接说：
"Turn this codebase into an interactive course"

# 或指定 GitHub 仓库
"Make a course from https://github.com/xxx/yyy"
```

### 自定义主题色

Skill 生成课程时会自动选择强调色，但你可以在生成后手动修改 `_base.html` 中的 `--color-accent` CSS 变量：

```css
:root {
  --color-accent: #FF6B35;       /* Vermillion */
  /* 替代方案: #FF7F7F (Coral), #2EC4B6 (Teal), #F4A261 (Amber), #2D6A4F (Forest) */
}
```

## 最佳实践

### 对于 Skill 使用者

- **从小型项目开始**——先感受课程的结构和深度，再用于大型代码库
- **优先选择你参与构建的项目**——你对功能有直观理解，课程会帮你补齐"为什么这样实现"的部分
- **关注 Quiz**——这是检验你是否真正理解的关键环节，不要跳过
- **把课程当作"对话词典"**——和非技术同事或 AI 工具沟通时引用其中的术语

### 对于 Skill 开发者/贡献者

- `styles.css` 和 `main.js` **禁止重新生成**——始终从 references/ 原样复制
- 模块 HTML 文件只含 `<section class="module">` 内容——不包含 HTML 样板、`<style>`、`<script>`
- 交互 JS 通过 `data-*` 属性挂载，不要在各模块中内联脚本
- Chat 容器需要 `id` 属性；Flow 动画使用 `data-steps='[...]'`
- 每个模块使用**独特的、有机的隐喻**——"如果发现自己用了两次 restaurant/kitchen 比喻，停下来重新思考"
- 并行构建时必须使用 Module Brief——Subagent 不应重新阅读完整代码库

## 注意事项

### 已知限制

- **Tooltip 裁剪是 #1 Bug**——Translation 块的 `overflow: hidden` 会裁剪绝对定位的 Tooltip。`main.js` 使用 `position: fixed` + `getBoundingClientRect()` 解决，但仍需注意
- **单引号在 data-steps 中会破坏 JSON 解析**——Flow 动画的步骤标签必须避免或 HTML 转义单引号
- **模块质量衰减**——一次性写完所有模块会导致后期模块单薄。一次构建和验证一个模块；复杂代码库使用并行路径 + Module Brief
- **scroll-snap mandatory 会困住用户**——在长模块内无法自由滚动，始终使用 `proximity`
- **Tooltip 不足是最常见缺陷**——宁可过度标注，不要漏掉生僻术语

### 常见误区

- **修整代码片段**——不要为了简洁而修改原始代码。选择自然短小（5-10 行）的片段，而非截断长代码
- **测验考察记忆**——"API 的全称是什么？"测试的是回忆而非理解。每道题应呈现新场景，要求应用知识
- **文本墙**——如果看起来"像课本而非信息图"，说明视觉密度不达标
- **滥用 restaurant 隐喻**——每个概念需要自己独特的隐喻

## 相关 Skills

- [[claude-api]] — 底层依赖 Claude API 进行代码分析与内容生成
- [[web-artifacts-builder]] — 构建复杂 HTML Artifact，技术栈部分重叠
- [[frontend-design]] — 前端 UI 美学指导，课程的视觉设计参考
- [[skill-creator]] — 了解该 Skill 如何构建，创建类似的自定义 Skill

## 参考资源

- [GitHub 仓库](https://github.com/zarazhangrui/codebase-to-course)
- [SKILL.md 源码](https://raw.githubusercontent.com/zarazhangrui/codebase-to-course/main/SKILL.md)
- [作者 Zara Zhang](https://github.com/zarazhangrui)
