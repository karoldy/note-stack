---
description: React Bits — 41k+ Stars，最大的动画 React 组件库，130+ 个免费可定制的文本动效、背景特效和 UI 交互组件。
---

# React Bits

## 概述

[React Bits](https://reactbits.dev) 是 David Haz 创建的开源动画 React 组件库（41k+ Stars），提供 130+ 个免费、可定制的动画组件，覆盖文本动效、背景特效和 UI 交互。目标是用最小的依赖，帮助开发者快速构建令人印象深刻的网站。

- **官网**：[reactbits.dev](https://reactbits.dev)
- **仓库**：[github.com/DavidHDev/react-bits](https://github.com/DavidHDev/react-bits)
- **许可**：MIT + Commons Clause

## 组件分类

| 类别 | 说明 | 示例 |
|------|------|------|
| **💬 Text Animations** | 文本入场、循环和交互动效 | 模糊文本、打字机、字符飞入、渐变滚动 |
| **🌀 Animations** | 通用 UI 动画 | 折叠展开、卡片翻转、进度条、加载骨架 |
| **🧩 Components** | 完整 UI 组件 | 轮播图、遮罩层、拖拽、视差滚动 |
| **🖼️ Backgrounds** | 动态背景效果 | 粒子、网格线、波浪、星空、噪点 |

## 技术栈支持

每个组件提供 4 种变体，按需选择：

| 变体 | 适用场景 |
|------|----------|
| **JS-CSS** | 标准 JavaScript + CSS 项目 |
| **JS-TW** | JavaScript + Tailwind CSS 项目 |
| **TS-CSS** | TypeScript + CSS 项目 |
| **TS-TW** | TypeScript + Tailwind CSS 项目（推荐） |

## 安装

### shadcn CLI（推荐）

```bash
npx shadcn@latest add @react-bits/BlurText-TS-TW
```

每个组件页面都包含可直接复制的 CLI 命令。

### 手动复制

在 [reactbits.dev](https://reactbits.dev) 选择技术栈偏好后，直接复制组件源码到项目中。

## 使用示例

### 文本模糊入场

```tsx
import BlurText from "@/components/react-bits/BlurText";

export default function Hero() {
  return (
    <BlurText
      text="Build Something Beautiful"
      className="text-6xl font-bold"
      delay={100}
      animateBy="words"
      direction="top"
    />
  );
}
```

### 动态背景

```tsx
import { Particles } from "@/components/react-bits/Particles";

export default function Background() {
  return (
    <Particles
      particleColors={["#ffffff", "#ffffff"]}
      particleCount={200}
      particleSpread={10}
      speed={0.1}
      particleBaseSize={100}
    />
  );
}
```

## 配套创意工具

React Bits 提供三个免费的在线创意工具：

| 工具 | 功能 | 输出 |
|------|------|------|
| **Background Studio** | 可视化编辑动画背景 | 视频 / 图片 / 代码 |
| **Shape Magic** | 创建形状间内圆角 | SVG / React 代码 / clip-path |
| **Texture Lab** | 20+ 纹理特效（噪点、抖动、ASCII） | 高清导出图片/视频 |

## 生态移植

| 框架 | 地址 |
|------|------|
| React（主项目） | [reactbits.dev](https://reactbits.dev) |
| Vue.js | [vue-bits.dev](https://vue-bits.dev) |
| Svelte | [sveltebits.xyz](https://sveltebits.xyz) |

## 最佳实践

- 优先使用 **TS-TW** 变体，TypeScript + Tailwind 组合开发体验最佳
- 组件支持按需导入，无需引入整个库，打包体积友好
- 所有组件通过 props 完全可定制，也可直接编辑源码
- 对于复杂的动画编排，组合多个组件而非修改源码
- 与 shadcn/ui 生态天然兼容，可搭配使用构建完整 UI

## 参考资源

- [官网 & 文档](https://reactbits.dev)
- [GitHub 仓库](https://github.com/DavidHDev/react-bits)
- [安装指南](https://reactbits.dev/get-started/installation)
- [Background Studio](https://reactbits.dev/tools)
