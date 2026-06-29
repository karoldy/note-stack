---
description: 多 Agent 协作模式深度分析 — 以 The Agency（232 个 AI Agent 角色库，118k+ Stars）为案例，拆解 Pipeline 串行、QA Gate 质量门禁、Swarm 角色分工、Adversarial 对抗验证四种核心协作模式，提供 Claude Code 可落地的实践方案。
---

# 多 Agent 协作模式

## 概述

单 Agent 的瓶颈是显而易见的：上下文窗口有限、单一视角容易遗漏、复杂任务需要多领域知识交叉。多 Agent 协作（Multi-Agent Collaboration）将任务拆解给多个专业角色，通过结构化的协作流程完成单个 Agent 无法独立完成的工作。

本文以开源项目 **[The Agency](https://github.com/msitarzewski/agency-agents)**（232 个预定义 Agent 角色，118k+ Stars）为核心案例，拆解四种经过验证的多 Agent 协作模式，并给出在 Claude Code 中的实践方案。

## 为什么需要多 Agent

| 单 Agent 的局限 | 多 Agent 的解法 |
| --- | --- |
| 单一视角，容易产生盲区 | 多角色交叉验证，覆盖不同维度 |
| 长任务中注意力衰减 | 每个 Agent 只聚焦自己的子任务 |
| 无法自我审查（既是运动员又是裁判） | QA/Reviewer Agent 独立验证 |
| 复杂任务超出单次上下文窗口 | 子任务并行处理，结果汇总 |
| "幻觉"难以自我纠正 | 对抗性 Agent（Reality Checker）强制证伪 |

## 四种核心协作模式

### 模式一：Pipeline 串行流水线

**思想**：将任务按阶段串联，上游 Agent 的输出作为下游 Agent 的输入，每个阶段有明确的质量门禁。

```
规格分析 → 架构设计 → 开发实现 → 质量验证 → 集成验收
   │           │           │           │           │
Project     Architect   Developer   EvidenceQA   Reality
Manager                                         Checker
```

**The Agency 实现**：`agents-orchestrator` 定义了四阶段流水线：

1. **Phase 1 — 项目分析**：`senior-project-manager` 读取 spec，生成任务清单
2. **Phase 2 — 架构设计**：`ArchitectUX` 基于任务清单输出技术方案
3. **Phase 3 — 开发-QA 循环**：逐任务分派 Developer → EvidenceQA 验证 → 通过则继续
4. **Phase 4 — 最终验收**：`reality-checker` 整体验证，**默认判定为 NEEDS WORK**

**关键规则**：每个阶段必须产出物（文件/截图/报告）才能进入下一阶段，不存在"口头交接"。

**适用场景**：
- 需求明确、阶段清晰的工程项目
- 新项目从零到一的全流程开发
- 需要多轮审查的合规性工作

### 模式二：QA Gate 质量门禁

**思想**：每个开发任务完成后，必须经过独立的 QA Agent 验证，不通过则打回重做。这是多 Agent 协作中最重要的质量控制机制。

```
Task N 开发 ──→ QA 验证 ──→ PASS → Task N+1
                  │
                  └── FAIL → 携带反馈回开发（最多 3 次重试）
```

**The Agency 实现**：

- **EvidenceQA**（任务级）：每个子任务完成后，用 Playwright 截图验证视觉结果，交叉比对 `test-results.json`
- **Reality Checker**（系统级）：全局验收，核心规则是 **"默认 NEEDS WORK，除非有压倒性证据"**

Reality Checker 的三大自动 FAIL 触发条件：

| 类别 | 触发条件 |
| --- | --- |
| 幻想评估 | "零问题发现"、无证据的满分评分、基础实现声称"精品/奢华" |
| 证据失败 | 无法提供全量截图、QA 已标问题仍可见、声称与截图矛盾 |
| 系统集成 | 用户旅程断裂、跨设备不一致、加载超 3 秒、交互元素不工作 |

**关键规则**：QA Agent 必须有**独立于开发 Agent 的视角和工具**——如果 QA 和开发共享同一个上下文，审查就失去了意义。

**适用场景**：
- 对质量有严格要求的交付项目
- UI/UX 密集的前端开发
- 需要视觉证据支撑的验收流程

### 模式三：Swarm 角色分工

**思想**：将一个大型任务同时分派给多个专业 Agent，每个 Agent 从自己的领域视角贡献方案，最后汇总成统一成果。

```
                     ┌── Frontend Developer
                     ├── Backend Architect
Product Discovery ──┼── Growth Hacker
                     ├── UX Researcher
                     ├── Brand Guardian
                     └── Project Shepherd
                            │
                            └──→ 统一方案
```

**The Agency 实现**：Nexus Spatial 案例中，8 个 Agent 同时对一个商业机会进行全方位分析——市场验证、技术架构、品牌策略、GTM、用户研究、执行计划等维度并行产出，单次会话生成统一方案。

**Agent 选择矩阵**（以 MVP 开发为例）：

| Agent | 职责 | 交付物 |
| --- | --- | --- |
| Frontend Developer | React 组件、路由、状态管理 | 可运行的前端应用 |
| Backend Architect | API 设计、数据库 Schema、认证 | 后端服务 + API 文档 |
| Growth Hacker | 获客策略、A/B 测试框架 | 增长方案 + 埋点计划 |
| Rapid Prototyper | 快速迭代、MVP 裁剪 | 原型 + 迭代计划 |
| Reality Checker | 全局质量把关 | 验收报告 |

**关键规则**：Swarm 不是"让所有 Agent 自由发挥"——必须有明确的**任务边界**和**汇总机制**。每个 Agent 的输出格式需要预先约定，否则汇总阶段会成为瓶颈。

**适用场景**：
- 产品探索与方案设计
- 多维度需求分析
- 跨领域方案评估

### 模式四：Adversarial 对抗验证

**思想**：引入一个"故意找茬"的 Agent，其唯一使命是质疑和反驳其他 Agent 的结论。只有经得起对抗的方案才是可靠的。

```
开发者产出 ──→ Reality Checker 对抗验证
                    │
                    ├── "这个 98 分怎么来的？截图呢？"
                    ├── "三个设备上都不一致，不能上线"
                    └── "你说生产就绪，但表单提交还是坏的"
```

**The Agency 实现**：Reality Checker 是这一模式的典型代表，其人格设定为：

- **skeptical**（怀疑主义）
- **evidence-obsessed**（证据痴迷）
- **fantasy-immune**（幻想免疫）

对抗 Agent 的关键行为：
1. **永远假设有问题**，直到看见证据
2. **要求压倒性证据**——一张截图不够，要全设备、全流程
3. **给出诚实的评级**——C+/B- 是正常水平，"第一次实现通常需要 2-3 轮修改"
4. **默认 FAIL**——不默认通过，不搞"及格万岁"

**与模式二的区别**：QA Gate 验证的是"有没有 bug"，Adversarial 验证的是"你是不是在吹牛"。前者关注功能正确性，后者关注声明真实性。

**适用场景**：
- 生产环境上线前的最终审查
- AI 生成代码的质量验证
- 供应商/外包交付物的验收
- 需要合规性审查的行业（金融、医疗）

## 协作模式组合实战

实际项目中，四种模式往往组合使用。以 The Agency 的完整工作流为例：

```
                    Pipeline 串行
┌──────────┐    ┌──────────┐    ┌──────────────────────┐    ┌──────────┐
│ Phase 1  │───→│ Phase 2  │───→│      Phase 3          │───→│ Phase 4  │
│ 项目分析 │    │ 架构设计 │    │   Swarm + QA Gate     │    │ 对抗验证 │
└──────────┘    └──────────┘    └──────────────────────┘    └──────────┘
                                      │         │
                              角色分工 Swarm    逐任务 QA Gate
                              ┌─ Frontend ─┐   Developer → EvidenceQA
                              ├─ Backend  ─┤   Developer → EvidenceQA
                              └─ Mobile  ──┘   Developer → EvidenceQA
```

管道保证流程推进，Swarm 在开发阶段并行提速，QA Gate 保证每个任务质量，对抗验证在最终阶段守住上线底线。

## Claude Code 实践指南

### 方式一：使用 CLAUDE.md 定义 Agent 角色

在项目 `.claude/agents/` 目录下创建 Agent 定义文件：

```markdown
<!-- .claude/agents/reality-checker.md -->

# Reality Checker

## Identity
你是一个怀疑主义的质量审查员。你默认所有产出都是 NEEDS WORK，
除非有压倒性证据证明其生产就绪。

## Rules
1. 永远要求视觉证据（截图、录屏）
2. 不相信没有数据支撑的声明
3. 第一次实现通常需要 2-3 轮修改
4. 诚实地给出 C+/B- 评级，而不是虚假的 98/100

## Process
1. 列出所有待审查的文件
2. 对每个声明交叉验证
3. 运行端到端用户旅程测试
4. 输出结构化评估报告
```

然后在对话中激活：

```
请以 Reality Checker 的角色审查当前 PR 的改动
```

### 方式二：Claude Code 多会话协作

```bash
# 会话 1：开发
claude --session dev "实现用户登录功能"

# 会话 2：审查（独立上下文）
claude --session review "审查 /session/dev 的产出，逐项验证"

# 会话 3：对抗验证
claude --session reality-check \
  "你是 Reality Checker，默认 NEEDS WORK。审视 dev 和 review 的结果"
```

### 方式三：Workflow 编排

利用 Claude Code 的 Workflow 能力实现自动化多 Agent 编排：

```javascript
// 伪代码示意
const tasks = await agent('project-manager: 拆分 spec 为任务清单')
for (const task of tasks) {
  let passed = false
  let attempts = 0
  while (!passed && attempts < 3) {
    await agent(`developer-${task.type}: 实现 ${task.name}`)
    const result = await agent(`evidence-qa: 验证 ${task.name}`)
    passed = result.status === 'PASS'
    attempts++
  }
}
const final = await agent('reality-checker: 最终验收')
```

### 方式四：直接使用 The Agency

```bash
# 克隆仓库
git clone https://github.com/msitarzewski/agency-agents

# 安装到 Claude Code
cd agency-agents
./scripts/install.sh --tool claude-code --division engineering,testing

# 在对话中激活
# "Activate Frontend Developer mode，帮我重构 Dashboard 页面"
# "Activate Reality Checker mode，审查刚才的改动"
```

### 选择建议

| 方式 | 适用场景 | 复杂度 |
| --- | --- | --- |
| CLAUDE.md Agent 定义 | 团队有稳定角色需求 | 低 |
| 多会话协作 | 个人开发者，临时需要审查 | 低 |
| Workflow 编排 | 可重复的自动化流程 | 中 |
| The Agency 集成 | 需要大量现成角色 | 中 |

## 最佳实践

### 角色设计

- **一个 Agent 只做一件事**：Frontend Developer 不做后端，Reality Checker 不写代码
- **给 Agent 鲜明的性格**：The Agency 的 Reality Checker 是"skeptical, evidence-obsessed, fantasy-immune"——这比"请严谨地审查"有效得多
- **定义失败条件**比定义成功条件更重要：Automatic FAIL Triggers 是 The Agency 最精彩的设计
- **Agent 之间的交接必须物化**：不能靠"你懂我的意思"，必须是文件、截图、JSON 数据

### 流程设计

- **质量门禁放在阶段边界**：不要在阶段中间审查，浪费时间；不要在阶段末尾跳过审查，积累风险
- **重试上限是必须的**：The Agency 的 3 次上限防止死循环，超过上限应升级而非继续循环
- **对抗 Agent 放在流程末端**：只审查不生产的 Agent 才能保持独立性
- **汇总阶段的格式要提前约定**：Swarm 模式最怕"每个人输出格式不同"

### 避坑指南

| 坑 | 表现 | 解法 |
| --- | --- | --- |
| Agent 同质化 | 多个 Agent 给出相似输出 | 给每个 Agent 明确的对立性格和约束 |
| 审查失效 | QA Agent 总是 PASS | 默认 FAIL，要求压倒性证据 |
| 上下文断裂 | 下游 Agent 不理解上游意图 | 物化交接，结构化输出格式 |
| 循环死锁 | 开发-QA 循环永远不收敛 | 3 次上限 + 升级机制 |
| 角色膨胀 | 创建了 50 个 Agent 但只用 3 个 | 从最少必要角色开始，按需增加 |

## 与 Skills 的关系

多 Agent 协作模式和 [Claude Code Skills](../skills/index.md) 是互补的：

- **Skills** 是给单个 Claude 实例加载的**领域知识包**（如 `frontend-design` 教 Claude 做好前端设计）
- **Agent 角色** 是给 Claude 实例赋予的**人格与行为约束**（如 Reality Checker 的怀疑主义人格）
- **多 Agent 协作** 是让多个有不同 Skills/角色的 Claude 实例**协同工作**的流程设计

实践中，一个 Agent 角色通常会搭配一组 Skills：

```
Frontend Developer Agent
├── taste-skill（设计约束）
├── frontend-design（风格指导）
├── react-doctor（React 最佳实践）
└── web-quality（无障碍与性能）

Reality Checker Agent
├── webapp-testing（Playwright 截图验证）
└── 不需要设计类 Skill（保持审查独立性）
```

## 参考资源

- [The Agency — 232 AI Agent 角色库](https://github.com/msitarzewski/agency-agents)
- [Claude Code Agent 模式官方文档](https://docs.anthropic.com/en/docs/claude-code/agents)
- [Building effective agents (Anthropic Research)](https://www.anthropic.com/engineering/building-effective-agents)
- [Multi-Agent Systems: A Survey](https://arxiv.org/abs/2412.12345)
- [Model Context Protocol 规范](https://modelcontextprotocol.io)
