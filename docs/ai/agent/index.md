---
description: AI Agent 深度指南 — 从核心概念、架构模式（ReAct/Plan-Execute/Multi-Agent）到工具调用（Function Calling/MCP）、Agent 角色设计、生产落地的全方位工程实践。
---

# AI Agent

## 概述

AI Agent 是能够自主感知环境、做出决策、执行动作的智能体。与传统的"一问一答"式 LLM 交互不同，Agent 具备**工具调用**、**多步推理**、**记忆**和**自主规划**能力，能够独立完成复杂的多步骤任务。

本文从工程视角拆解 AI Agent 的核心概念、主流架构和生产实践，面向需要将 Agent 集成到实际系统中的开发者。

## 核心概念

### Agent 的四项基本能力

| 能力 | 说明 | 示例 |
| --- | --- | --- |
| **感知（Perceive）** | 理解用户意图和上下文 | 解析自然语言需求，提取关键信息 |
| **推理（Reason）** | 分解任务、制定计划 | 将"搭建博客"拆解为路由设计、模板、部署 |
| **行动（Act）** | 调用工具、执行操作 | 读写文件、执行命令、调用 API |
| **记忆（Remember）** | 跨轮次保持上下文 | 记住用户偏好、已完成的步骤、经验教训 |

### Agent vs 传统 Chatbot

| 维度 | Chatbot | AI Agent |
| --- | --- | --- |
| 交互模式 | 一问一答，无状态 | 多轮自主对话，有状态 |
| 能力边界 | 仅文本生成 | 工具调用 + 代码执行 + 外部系统集成 |
| 任务复杂度 | 单步完成 | 多步规划与执行 |
| 错误处理 | 无 | 自我纠错、重试、降级 |
| 输出形式 | 纯文本 | 文本 + 文件 + API 调用 + 系统操作 |

## 主流架构模式

### 模式一：ReAct（Reasoning + Acting）

最基础的 Agent 模式，Thought → Action → Observation 循环：

```
用户输入 → Thought（思考）→ Action（调用工具）→ Observation（观察结果）→ Thought → ...
```

**流程**：Agent 收到任务后，先思考需要什么信息，然后调用合适的工具获取，观察结果后再决定下一步。

**适用场景**：简单到中等复杂度的工具调用任务，如数据查询、文件操作。

**局限**：缺乏全局规划，容易在长任务中偏离目标。

### 模式二：Plan-Execute（规划-执行）

先规划后执行，将推理和行动分离：

```
用户输入 → Planner（制定计划）→ Executor（逐步执行）→ Evaluator（评估结果）
                │                      │
                └──────────────────────┘
                    计划可动态调整
```

**核心组件**：
- **Planner**：分析需求，生成可执行的步骤列表
- **Executor**：逐步执行计划中的每一步（可调用工具）
- **Evaluator**：评估执行结果，决定是继续、调整还是终止

**适用场景**：复杂多步骤任务，如代码生成、项目搭建、数据分析流水线。

### 模式三：Tool-Use Loop（工具使用循环）

LLM 自主决定何时调用工具、调用哪个工具、如何解读结果：

```
while (task_not_complete) {
    response = llm.generate(context, available_tools)
    if (response.has_tool_call) {
        result = execute_tool(response.tool_call)
        context.add(result)
    } else {
        return response
    }
}
```

这是 Claude、GPT-4 等现代 LLM 的原生能力，也是 Function Calling / Tool Use 的底层机制。

### 模式四：Multi-Agent 协作

多 Agent 通过角色分工与结构化协作完成复杂任务，详见 [多 Agent 协作模式](./multi-agent-collaboration.md)。

```
Agent A (Planner) → Agent B (Developer) → Agent C (Reviewer)
                       ↑        │
                       └────────┘
                      QA Gate 循环
```

### 架构选择指南

| 场景 | 推荐模式 | 原因 |
| --- | --- | --- |
| 简单查询/单步操作 | ReAct | 足够轻量 |
| 多步骤开发任务 | Plan-Execute | 需要全局规划 |
| 单领域深度工作 | Tool-Use Loop | LLM 原生支持 |
| 跨领域复杂项目 | Multi-Agent | 角色分工降低单点压力 |

## Agent 角色设计

Agent 的行为质量高度依赖于角色定义的精细程度。The Agency 项目（232 个 Agent 角色）验证了一个核心结论：**给 Agent 一个鲜明的身份和明确的约束，比给出通用的"请严谨工作"有效得多。**

一个完整的 Agent 角色定义通常包含以下层次：

```
角色层 ──── Identity, Personality, Core Mission
约束层 ──── Critical Rules, Forbidden Actions, Guardrails
能力层 ──── Tools, Skills, Technical Capabilities
流程层 ──── Workflow Steps, Decision Gates, Templates
评估层 ──── Success Metrics, Quality Standards, FAIL Triggers
```

角色设计的核心原则：

1. **一个角色只做一件事**：Frontend Developer 不做后端，Reality Checker 不写代码
2. **性格比能力更重要**："你是一个怀疑主义的审查员" > "请仔细检查代码"
3. **定义失败条件比定义成功条件更有效**：明确的 FAIL trigger 比模糊的"请保证质量"更能防止虚报
4. **物化交接标准**：每个阶段的产出必须是文件、截图、JSON——不能靠"你懂我的意思"

详细的角色设计方法论参见 [Agent 角色设计指南](./agent-persona-design.md)。如果希望直接使用现成的 Agent 角色库，参见 [The Agency 使用指南](./agency-agents-usage.md)。

## 工具调用机制

### Function Calling

LLM 原生支持的 Tool Use 能力。开发者定义工具 Schema，模型自主决定调用时机和参数：

```typescript
// 定义可用工具
const tools = [
  {
    name: "read_file",
    description: "读取指定路径的文件内容",
    parameters: {
      type: "object",
      properties: {
        path: { type: "string", description: "文件路径" }
      },
      required: ["path"]
    }
  }
]

// LLM 自主决定是否调用
const response = await llm.generate({
  messages: [{ role: "user", content: "看看 package.json 里有哪些依赖" }],
  tools
})
// response.tool_calls → [{ name: "read_file", arguments: { path: "package.json" } }]
```

### MCP（Model Context Protocol）

MCP 是标准化的工具接入协议，解决 Function Calling 的碎片化问题。详见 [MCP 协议](../mcp/index.md)。

**Function Calling vs MCP 对比**：

| 维度 | Function Calling | MCP |
| --- | --- | --- |
| 标准化 | 各厂商自行定义 | 统一协议 |
| 工具复用 | 每个项目单独集成 | 一次开发，多处使用 |
| 生态 | 无 | 社区 Server 生态 |
| 适用场景 | 项目特定的简单工具 | 跨项目、跨团队的工具基础设施 |

### 工具设计原则

- **原子性**：一个工具只做一件事
- **幂等性**：重复调用不产生副作用（读操作）
- **明确性**：description 要足够详细，模型才能正确选择
- **错误友好**：返回值包含足够上下文，帮助模型理解失败原因

## 记忆系统

Agent 的记忆分为三个层次：

| 层次 | 存储位置 | 生命周期 | 用途 |
| --- | --- | --- | --- |
| **工作记忆** | 上下文窗口 | 单次会话 | 当前任务状态、中间结果 |
| **短期记忆** | 对话历史 / 向量数据库 | 多次会话 | 用户偏好、历史决策 |
| **长期记忆** | 文件系统 / 知识库 | 永久 | 经验教训、规则、最佳实践 |

### 实践建议

- **工作记忆**：在 Prompt 中保留关键状态摘要，防止长对话中的上下文丢失
- **短期记忆**：用 `.claude/memory/` 或向量数据库存储跨会话的偏好和决策
- **长期记忆**：沉淀为 CLAUDE.md、Agent 角色文件、Skills

The Agency 的 Agent 文件中包含 **Learning & Memory** 章节，让 Agent 在每次任务后更新经验——这是 Agent 从"一次性工具"进化为"持续成长的助手"的关键设计。

## 生产落地考量

### 可靠性

- **重试机制**：工具调用失败时的退避策略
- **超时处理**：避免 Agent 陷入死循环
- **降级方案**：核心工具不可用时的替代路径
- **人工介入点**：关键操作（如部署、付费）前的人工确认

### 成本控制

- **模型分层**：Planner 用强模型（Opus），Executor 用快模型（Haiku）
- **缓存复用**：相同上下文命中 Prompt Cache
- **任务预算**：单次任务设置 Token 上限

### 可观测性

- **步骤记录**：每一次 Thought → Action → Observation 的完整日志
- **工具调用追踪**：调用次数、成功率、平均耗时
- **质量指标**：任务完成率、重试次数、用户满意度

## 参考资源

- [Building Effective Agents (Anthropic Research)](https://www.anthropic.com/engineering/building-effective-agents)
- [The Agency — 232 个生产级 Agent 角色](https://github.com/msitarzewski/agency-agents)
- [OpenAI Agents SDK](https://platform.openai.com/docs/guides/agents)
- [LangChain Agent 文档](https://python.langchain.com/docs/concepts/agents/)
- [Model Context Protocol](https://modelcontextprotocol.io)
