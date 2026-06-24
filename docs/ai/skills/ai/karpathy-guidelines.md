---
description: andrej-karpathy-skills — 181k Stars，将 Karpathy 对 LLM 编码陷阱的观察提炼为 4 条行为准则，从根本上改善 Claude Code 的输出质量。
---

# Karpathy 编码准则

## 概述

`andrej-karpathy-skills` 是 181k+ Stars 的行为准则 Skill，将 Andrej Karpathy 对 LLM 编码陷阱的观察提炼为 4 条核心准则，以单个 `CLAUDE.md` 文件的形式注入 Claude Code。它不教 AI 怎么写代码，而是教 AI **以什么态度**写代码 —— 先思考再动手、保持简单、精准手术、目标驱动验证。

Karpathy 的原观察：

> "模型会替你做出错误假设，然后一路执行下去。它们不管理自己的困惑，不寻求澄清，不暴露不一致，不呈现权衡，在该反驳时不反驳。"

> "它们真的喜欢过度复杂化代码和 API，臃肿的抽象，不清理死代码……用 1000 行实现一个 100 行就能搞定的东西。"

- **分类**：AI 工具 / Claude Code 工作流
- **调用方式**：作为 `CLAUDE.md` 自动加载，或通过 `/plugin` 安装
- **来源**：社区（[multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)）

## 触发条件

该 Skill 作为项目级行为准则，**始终生效**，尤其适用于：

- 非平凡的多文件修改任务
- 需要 AI 自行判断实现方式的开放式需求
- 大型代码库中的局部修改
- 容易过度工程化的功能开发

以下场景可**放宽**准则：

- 简单错字修复、单行改动
- 明确的机械化操作（重命名、格式修正）
- 用户已给出极详细的逐行实现指令

## 四条核心准则

### 1. Think Before Coding（先思考再编码）

**不要假设。不要隐藏困惑。暴露权衡。**

| 做法 | 说明 |
|------|------|
| 显式声明假设 | 如果不确定，提问而非猜测 |
| 呈现多种理解 | 存在歧义时，列出所有可能的解释 |
| 该反驳时反驳 | 如果有更简单的方法，直接说出来 |
| 困惑时停下来 | 明确指出哪里不清楚，请求澄清 |

**反面案例**：用户说"添加导出用户数据功能"，AI 默认导出全部用户、写入本地文件、自行决定字段，不询问权限、分页或格式。

**正面案例**：先确认导出范围（全部还是筛选）、导出方式（文件下载 / 后台任务 / API 端点）、敏感字段处理、数据量级。

### 2. Simplicity First（简单至上）

**用最少代码解决问题。不要投机。**

- 不添加未要求的额外功能
- 不为单次使用的代码创建抽象层
- 不添加未要求的"灵活性"或"可配置性"
- 不处理不可能发生的错误场景
- 200 行能写成 50 行，就重写

**自检问题**：资深工程师看到这段代码会说"太复杂了"吗？

**反面案例**：用户说"算折扣"，AI 创建 `DiscountStrategy` 抽象基类、`PercentageDiscount`/`FixedDiscount` 子类、`DiscountConfig` 数据类、`DiscountCalculator` 工厂类 —— 对应一行 `amount * (percent / 100)`。

**正面案例**：
```python
def calculate_discount(amount: float, percent: float) -> float:
    return amount * (percent / 100)
```

### 3. Surgical Changes（精准手术）

**只碰必须改的。只清理自己产生的烂摊子。**

| 编辑已有代码时 | 不做什么 |
|------|------|
| 不改动相邻代码、注释或格式 | ❌ "顺手优化"旁边的函数 |
| 不重构没坏的东西 | ❌ "这个地方应该用新 API" |
| 匹配已有风格，即使你更喜欢别的 | ❌ 把 `var` 全改成 `const` |
| 发现无关的死代码 → 提出来，不删 | ❌ 静默删除"看起来没用"的代码 |

**自检问题**：diff 中的每一行改动都能追溯回用户的需求吗？

### 4. Goal-Driven Execution（目标驱动执行）

**定义成功标准。循环直到验证通过。**

将命令式任务转化为可验证的目标：

| 不要... | 转化为... |
|------|------|
| "加个校验" | "为非法输入写测试，然后让测试通过" |
| "修这个 bug" | "写一个能复现 bug 的测试，然后修到通过" |
| "重构 X" | "确保前后测试都通过" |

多步骤任务先列出计划：

```
1. [步骤] → 验证: [检查项]
2. [步骤] → 验证: [检查项]
3. [步骤] → 验证: [检查项]
```

强成功标准让 AI 能自主循环；弱标准（"把它搞对"）需要持续澄清。

## 安装

### Claude Code 插件（推荐）

```bash
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills
```

跨项目全局生效。

### 手动安装（项目级）

```bash
# 新项目
curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md

# 已有项目（追加到已有 CLAUDE.md）
curl https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md >> CLAUDE.md
```

### Cursor

仓库包含 `.cursor/rules/karpathy-guidelines.mdc`，复制到项目即可。

## 效果验证

当以下现象出现时，说明准则生效：

- **diff 中的无关改动减少** —— 只出现被请求的修改
- **因过度复杂导致的重写减少** —— 第一次就写对
- **澄清问题在实现之前提出** —— 而不是改错之后再问
- **PR 干净、最小化** —— 没有顺手重构或"改进"

## 最佳实践

- **合并到已有的 `CLAUDE.md`**，而非单独使用。将这 4 条准则与项目特定规则共存
- **在大型项目中**准则严格执行；**在简单任务中**用常识灵活判断
- 对照 [[codebase-to-course]] 使用：准则保证代码质量，course 工具帮助理解代码库结构
- 定期回顾 PR diff，确认这些准则是否真正减少了噪声改动
- 项目特定规则示例（追加在 CLAUDE.md 末尾）：
  ```markdown
  ## Project-Specific Guidelines
  - Use TypeScript strict mode
  - All API endpoints must have tests
  - Follow existing error handling patterns in src/utils/errors.ts
  ```

## 注意事项

- 准则偏向**谨慎而非速度**，对简单任务（错字修复、单行改动）不应机械套用
- 目标是减少非平凡任务中的昂贵错误，而非拖慢所有操作
- 准则文件本身可能随项目需求演进，建议定期回顾和调整
- 不替代 Code Review —— 它是 AI 行为的护栏，不是人类判断的替代品

## 相关 Skills

- [[claude-api]] — Claude API 参考，与该准则互补（API 告诉你怎么调，准则告诉你怎么写）
- [[codebase-to-course]] — 代码库学习工具，理解代码结构后可配合准则做精准修改

## 参考资源

- [GitHub 仓库](https://github.com/multica-ai/andrej-karpathy-skills)
- [Karpathy 原始推文（英文）](https://x.com/karpathy/status/2015883857489522876)
- [Claude Code 插件安装文档](https://docs.anthropic.com/en/docs/claude-code/plugins)
