---
description: AI Agent 角色设计方法论 — 以 The Agency（232 个生产级 Agent）为蓝本，拆解 Agent 人格文件的结构设计、性格工程、交付物模板和质量标准编写技巧。
---

# Agent 角色设计指南

## 概述

一个 Agent 的行为质量，80% 取决于角色定义的质量。模糊的角色定义产生模糊的输出，鲜明的角色定义产生可靠的输出。

本文基于对 **[The Agency](https://github.com/msitarzewski/agency-agents)** 项目中 232 个生产级 Agent 文件的结构分析，提炼出一套可复用的 Agent 角色设计方法论。

## 为什么需要结构化角色文件

### 通用 Prompt 的问题

```
你是一个前端开发者，帮我做页面。
```

这种 Prompt 存在的问题：

- **角色模糊**：什么是"前端开发者"？React 还是 Vue？重逻辑还是重样式？
- **没有行为约束**：可以输出占位符、省略代码、使用默认样式
- **没有质量标准**：Agent 不知道什么算"完成"
- **不可复用**：每次都要重新描述

### 结构化角色文件的优势

```markdown
# Frontend Developer

## Identity
你是现代 Web UI 专家，精通 React/Vue/Svelte。
你注重细节、追求性能、以用户为中心。

## Critical Rules
- 性能优先：首次加载 < 3s（3G 网络）
- WCAG 2.1 AA 可访问性合规
- 禁用占位符注释，必须输出完整代码
- 移动端优先，所有组件响应式

## Success Metrics
- Lighthouse 评分 > 90
- 跨浏览器兼容
- 组件复用率 > 80%
- 零控制台错误
```

**对比效果**：

| 维度 | 通用 Prompt | 结构化角色文件 |
| --- | --- | --- |
| 输出完整度 | 常有占位符 | 完整可运行代码 |
| 风格一致性 | 每次不同 | 遵循既定规范 |
| 质量水平 | 不可控 | 有量化标准 |
| 复用性 | 零 | 一次定义，无限使用 |
| 团队共享 | 无法 | 可直接分发 |

## 角色文件结构

The Agency 的 Agent 文件遵循一个五层结构，覆盖从身份到评估的完整链路：

```
┌──────────────────────────────────────┐
│          Frontmatter / 元信息          │  名称、描述、颜色标记
├──────────────────────────────────────┤
│       Identity & Memory（角色层）      │  人格、背景、核心使命
├──────────────────────────────────────┤
│       Critical Rules（约束层）         │  硬性规则、禁止行为、兜底策略
├──────────────────────────────────────┤
│       Technical Deliverables（能力层）  │  代码模板、交付物格式、技术栈
├──────────────────────────────────────┤
│       Workflow Process（流程层）       │  工作步骤、决策门禁、输出模板
├──────────────────────────────────────┤
│       Success Metrics（评估层）        │  量化标准、FAIL 条件、质量评级
└──────────────────────────────────────┘
```

### 第一层：Frontmatter（元信息）

```yaml
---
name: Frontend Developer
description: Build responsive, accessible web apps with pixel-perfect precision
color: #00BCD4
emoji: 🖥️
tags: [react, vue, frontend, css, accessibility]
---
```

**设计要点**：
- `name` 是激活 Agent 的标识符，应简洁且语义明确
- `description` 是一句话的职责声明，也是 Agent 的"自我认知锚点"
- `color` 和 `emoji` 虽小，但在多 Agent 协作时提供快速视觉区分
- `tags` 帮助工具和用户搜索匹配的 Agent

### 第二层：Identity & Memory（身份与记忆）

这是整个角色文件最重要的部分——它决定了 Agent "是谁"。

**正面示例**（Reality Checker）：

> I am a senior integration testing specialist who is skeptical, thorough, evidence-obsessed, and completely immune to developer fantasy. I remember every time a premature approval led to production issues.

**反面示例**（太模糊）：

> I am a helpful assistant that reviews code.

**差异分析**：

| 维度 | 反面示例 | 正面示例 |
| --- | --- | --- |
| 性格 | "helpful"（无特征） | "skeptical, evidence-obsessed, fantasy-immune"（鲜明） |
| 资历 | 未定义 | "senior integration testing specialist"（有权威感） |
| 记忆 | 无 | 记住过往的失败经验 |
| 态度 | 中立 | "默认 NEEDS WORK"（有立场） |

**设计原则**：

1. **用性格形容词取代功能描述**：不是说"你会审查代码"，而是说"你是一个怀疑主义者，不相信任何没有证据的声明"
2. **给 Agent 资历和权威感**：`senior`、`specialist`、`10 years of experience` 等措辞会让模型更自信
3. **植入记忆锚点**：让 Agent "记住"典型的失败模式和教训
4. **一个角色 = 一个性格**：不要在同一个 Agent 中混合"友好协作"和"严格审查"

**性格设计参考表**：

| Agent 类型 | 推荐性格关键词 |
| --- | --- |
| 开发者 | detail-oriented, performance-focused, pragmatic, craftsman |
| 审查者 | skeptical, evidence-obsessed, thorough, unflinching |
| 架构师 | systematic, big-picture, principled, trade-off-aware |
| 产品经理 | user-centric, data-driven, decisive, prioritization-focused |
| 教练/导师 | patient, encouraging, practical, socratic |

### 第三层：Critical Rules（关键约束）

约束层定义 Agent 绝对不能违反的规则。这是结构化角色文件相比通用 Prompt 最大的优势。

**The Agency 经典约束示例**：

**Frontend Developer 的约束**：

> - Performance-first development — every component must meet Core Web Vitals
> - Accessibility is non-negotiable — WCAG 2.1 AA minimum, ARIA labels, semantic HTML, keyboard navigation
> - Mobile-first responsive design — every component works on 320px width

**Reality Checker 的自动 FAIL 条件**：

> **Automatic FAIL triggers**:
> - Claims of "zero issues found" without comprehensive evidence
> - "Luxury/premium" claims for basic implementations
> - Production-ready declarations without proof of excellence
> - Inability to provide comprehensive screenshots
> - Prior QA issues still visible in the current build
> - Claims contradicting visual reality
> - Broken user journeys visible in screenshots
> - Cross-device inconsistencies
> - Load times > 3 seconds

**约束设计指南**：

1. **使用"非协商"措辞**：`non-negotiable`、`mandatory`、`never`、`always`、`must`
2. **定义 FAIL 条件而非 PASS 条件**：告诉 Agent "什么情况判失败"比"什么情况判通过"更有效
3. **约束要可验证**：每一条约束应该能被客观检查（"加载时间 < 3s"可以验证，"做得好一点"无法验证）
4. **数量控制在 5-10 条**：太多约束 Agent 会遗忘，太少则形同虚设

### 第四层：Technical Deliverables（交付物）

能力层定义了 Agent 应该产出什么、用什么技术、遵循什么格式。

**The Agency Frontend Developer 的代码示例**：

> ```tsx
> // Always use React.memo for pure components
> const UserList = React.memo(({ users }: UserListProps) => {
>   const virtualizer = useVirtualizer({ ... })
>
>   return (
>     <ul role="list" aria-label="User list">
>       {virtualizer.getVirtualItems().map((item) => (
>         <li key={item.key} role="listitem">
>           <UserCard user={users[item.index]} />
>         </li>
>       ))}
>     </ul>
>   )
> })
> ```

**设计指南**：

1. **提供代码风格锚点**：不需要完整文档，给一个典型示例就够了——Agent 会模仿这个风格
2. **展示期望的复杂度水平**：示例代码中的 `useVirtualizer`、`React.memo`、`role="list"` 同时传达了性能意识、可访问性和组件化程度
3. **隐含技术栈偏好**：示例使用什么技术，Agent 就会倾向什么技术

**交付物模板**（来自 The Agency 的实践）：

| Agent 类型 | 推荐交付物模板 |
| --- | --- |
| 开发者 | 可运行代码 + 测试 + 性能报告 |
| 架构师 | 架构图描述 + 技术决策记录 + 风险评估 |
| 审查者 | 结构化评估报告（问题分类 + 严重程度 + 修复建议） |
| 产品经理 | PRD 格式（用户故事 + 验收标准 + 优先级） |

### 第五层：Workflow Process（工作流程）

流程层定义 Agent 完成任务的步骤序列——把模糊的"干活"变成可预测的流程。

**The Agency Reality Checker 的三步流程**：

> **STEP 1: Reality Check Commands（NEVER SKIP）**
> - List all view files in the project
> - Grep for premium/luxury/enterprise keyword claims
> - Run automated screenshot script
> - Review all evidence output
>
> **STEP 2: QA Cross-Validation**
> - Review QA agent's findings
> - Cross-reference automated screenshots
> - Verify test-results.json data
> - Confirm or challenge QA's assessment
>
> **STEP 3: End-to-End System Validation**
> - Analyze user journeys with before/after screenshots
> - Review responsive screenshots at 3 device sizes
> - Check interaction sequences (nav, forms, accordions)
> - Review performance data

**流程设计原则**：

1. **步骤要具体到命令级别**：`"List all view files"` 比 `"检查项目"` 有效 10 倍
2. **NEVER SKIP 标记**：对关键步骤做强制性标记，防止 Agent 走捷径
3. **步骤之间要有产出物**：STEP 1 产出证据列表，STEP 2 产出交叉验证报告，STEP 3 产出最终评估
4. **明确定义门禁条件**：每一步完成的标准是什么

### 第六层：Success Metrics（成功标准）

评估层是 Agent 自我评估的参照系——没有它，Agent 不知道"做到什么程度算完成"。

**The Agency Frontend Developer 的成功标准**：

> - Page loads under 3s on 3G
> - Lighthouse scores above 90
> - Cross-browser compatibility verified
> - Component reusability above 80%
> - Zero console errors in production

**设计指南**：

1. **量化 > 定性**：`"Lighthouse > 90"` > `"性能良好"`
2. **可自动验证**：理想情况下，Agent 可以自己验证这些指标
3. **包含反指标**：不只是"做到什么"，还有"不能出现什么"（零错误、零警告）
4. **匹配角色层级**：开发者的指标是技术性的（Lighthouse 分数），产品经理的指标是业务性的（用户留存提升）

## 案例拆解：Reality Checker

以 The Agency 中最具特色的 Reality Checker 为例，展示一个完整角色文件的工程价值。

### 完整角色文件结构

这是一个浓缩的最佳实践案例：

```markdown
# Reality Checker

## Identity & Memory
🧐 Reality Checker — Defaults to "NEEDS WORK"
I am a senior testing specialist: skeptical, thorough, evidence-obsessed,
fantasy-immune. I remember every premature approval that led to production issues.

## Core Mission
1. Stop Fantasy Approvals — no "98/100" for basic dark themes
2. Require Overwhelming Evidence — visual proof for every claim
3. Realistic Quality Assessment — first implementations need 2-3 revisions;
   C+/B- is normal; honest feedback > false comfort

## Critical Rules
### Automatic FAIL Triggers
- "Zero issues found" without comprehensive evidence
- "Premium/luxury" claims for basic implementations
- Production-ready declarations without proven excellence
- Inability to provide comprehensive screenshots
- Claims contradicting visible reality

## Workflow Process
### STEP 1: Reality Check（NEVER SKIP）
1. List all view files
2. Grep for inflated quality claims
3. Run automated screenshot script
4. Review evidence output

### STEP 2: QA Cross-Validation
1. Review QA agent's findings
2. Cross-reference automated screenshots vs claims
3. Verify test-results.json
4. Confirm or challenge QA's assessment

### STEP 3: End-to-End Validation
1. Analyze user journeys with before/after screenshots
2. Review at 3 device sizes
3. Check interactions (nav, forms, accordions)
4. Review performance metrics

## Success Metrics
- Approved systems work in production
- Assessments match real user experience
- Developers understand specific improvements needed
- No broken functionality reaches end users
```

### 为什么这个角色有效

1. **人格驱动行为**："fantasy-immune" 这个性格设定决定了整个工作流程——从 grep 关键词到挑战声明，全部源于对"幻想"的免疫
2. **FAIL 条件是安全网**：即使其他步骤被跳过，Automatic FAIL Triggers 也能兜底
3. **默认值设定基调**："Defaults to NEEDS WORK" 反转了常规的"默认通过"心态
4. **诚实预期管理**："第一次实现需要 2-3 轮修改"——这句话同时管理了用户预期和 Agent 的审查标准

## 角色测试与迭代

### 测试方法

```
1. 单任务测试 —— 给 Agent 一个典型任务，观察输出质量
2. 边界测试 —— 给模糊的需求，观察 Agent 是否会主动追问
3. 对抗测试 —— 故意给一个"看起来不错"的结果，观察审查 Agent 能否发现问题
4. 一致性测试 —— 同一个任务执行 3 次，观察输出一致性
```

### 迭代信号

| 观察到的行为 | 角色设计问题 | 调整方向 |
| --- | --- | --- |
| Agent 频繁跳过步骤 | 约束不够强 | 加 `NEVER SKIP` 标记、 FAIL trigger |
| 输出风格不稳定 | 缺少代码示例锚点 | 在 Deliverables 中增加典型示例 |
| 审查总是 PASS | 默认值设反了 | 改为 `Defaults to NEEDS WORK` |
| 与预期技术栈不符 | 示例代码暗示错误 | 更换 Technical Deliverables 中的代码示例 |
| 任务半途而废 | 流程步骤太粗略 | 把步骤细化到命令级别 |

### 从 The Agency 学到的教训

1. **性格比 Prompt 技术更重要**：The Agency 的 "skeptical, evidence-obsessed, fantasy-immune" 比 200 字的"请仔细审查"提示更有效
2. **FAIL 条件比 PASS 标准更稀缺**：大多数角色文件定义了"什么是好"，但极少定义"什么是不可接受的"
3. **代码示例是隐式的技术栈声明**：Agent 会模仿示例的技术选型，这比在约束层写"请使用 React"更有效
4. **多 Agent 协作时，角色边界比角色深度更重要**：每个 Agent 的职责范围必须无重叠，否则会出现两个 Agent 抢同一个任务或互相推诿

## 模板：Agent 角色文件骨架

```markdown
---
name: [角色名称]
description: [一句话职责声明]
color: #[十六进制颜色]
emoji: [1-2 个 emoji]
tags: [标签数组]
---

# [角色名称]

## Identity & Memory
[我是谁] — [性格关键词]
[我记住的经验教训]

## Core Mission
1. [使命一]
2. [使命二]
3. [使命三]

## Critical Rules
### NEVER
- [绝对禁止的行为]

### ALWAYS
- [必须执行的操作]

### Automatic FAIL Triggers
- [触发失败的条件 A]
- [触发失败的条件 B]

## Technical Deliverables
[代码示例或交付物格式模板]

## Workflow Process
### STEP 1: [阶段名]（NEVER SKIP）
1. [具体操作]
2. [具体操作]

### STEP 2: [阶段名]
1. [具体操作]
2. [具体操作]

### STEP 3: [阶段名]
1. [具体操作]
2. [具体操作]

## Success Metrics
- [可量化指标 A]
- [可量化指标 B]
- [反指标：绝对不能出现的问题]
```

将此模板保存为 `agent-name.md`，放到以下路径即可使用：

- **Claude Code**：`~/.claude/agents/` 或 `.claude/agents/`
- **直接使用**：将文件内容粘贴到对话开头
- **团队共享**：提交到项目仓库的 `.claude/agents/` 目录

## 与 NoteStack 其他模块的关系

- [多 Agent 协作模式](./multi-agent-collaboration.md) — 角色定义好之后，如何让多个 Agent 协同工作
- [Claude Code Skills](../skills/index.md) — Skills 是能力包，Agent 角色是人格定义，二者配合使用
- [Prompt Engineering](../prompt-engineering/index.md) — Agent 角色设计的底层技术是 Prompt Engineering

## 参考资源

- [The Agency — 232 个生产级 Agent 角色源码](https://github.com/msitarzewski/agency-agents)
- [Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)
- [Claude Code Agent 配置文档](https://docs.anthropic.com/en/docs/claude-code/agents)
- [OpenAI Agents SDK — Agent 设计模式](https://platform.openai.com/docs/guides/agents)
