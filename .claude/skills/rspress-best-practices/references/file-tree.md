# rspress-plugin-file-tree 参考

将 ` ```tree` 代码块渲染为交互式、可折叠的目录树组件。

## 安装

```bash
npm i rspress-plugin-file-tree
# or
pnpm add rspress-plugin-file-tree
```

## 配置

```ts
// rspress.config.ts
import { defineConfig } from 'rspress/config';
import fileTree from 'rspress-plugin-file-tree';

export default defineConfig({
  plugins: [
    fileTree({
      initialExpandDepth: 0,     // 默认展开层级。0 = 仅根节点展开
                                  // Infinity = 全部展开
    }),
  ],
});
```

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `initialExpandDepth` | `number` | `0` | 初始展开的目录层级，`Infinity` 展开全部节点 |

## 基础语法

使用 `tree` 作为语言标识符，内容为标准 `tree` 命令输出格式：

````markdown
```tree
.
├── rspress.config.ts
├── docs
│   ├── index.md
│   ├── guide
│   │   ├── introduction.md
│   │   └── configuration.md
│   └── public
│       └── favicon.ico
├── theme
│   └── index.tsx
└── package.json
```
````

## 渲染效果

代码块会渲染为交互式文件树：
- **文件夹**：带展开/折叠箭头，点击切换
- **文件**：带文件图标，不可展开
- **嵌套**：通过缩进层级自动识别父子关系

## 使用场景

| 场景 | 示例 |
| --- | --- |
| 项目结构说明 | 展示 `src/` 下的目录组织 |
| 配置文件布局 | 展示多环境配置文件关系 |
| 组件层级 | 展示组件树嵌套关系 |
| 路由结构 | 展示页面路由的文件对应关系 |

## 语法规则

1. **根节点**：以 `.` 或目录名开头
2. **树形连接符**：
   - `├──` — 中间节点（同级还有后续节点）
   - `└──` — 末尾节点（同级最后一个）
   - `│` — 纵向连接线（保持缩进层级）
3. **缩进**：使用空格（建议 4 个空格）表示层级关系
4. **注释**：在文件/目录名后可用 `#` 或 `//` 添加说明（取决于渲染器支持）

## 实际示例

### 典型前端项目结构

````markdown
```tree
.
├── src
│   ├── components
│   │   ├── Button
│   │   │   ├── index.tsx
│   │   │   ├── Button.module.css
│   │   │   └── Button.test.tsx
│   │   └── Modal
│   │       ├── index.tsx
│   │       └── Modal.module.css
│   ├── hooks
│   │   ├── useAuth.ts
│   │   └── useFetch.ts
│   ├── pages
│   │   ├── Home.tsx
│   │   └── About.tsx
│   ├── App.tsx
│   └── main.tsx
├── public
│   └── favicon.ico
├── package.json
└── tsconfig.json
```
````

### 配置多环境结构

````markdown
```tree
.
├── config
│   ├── default.json       # 默认配置
│   ├── development.json   # 开发环境
│   ├── staging.json       # 预发布环境
│   └── production.json    # 生产环境
└── secrets
    ├── .env.development
    └── .env.production
```
````

## 与普通代码块的对比

| 方式 | 渲染效果 | 交互性 |
| --- | --- | --- |
| ` ```text ` 手写树形 | 纯文本，无高亮 | 无 |
| ` ```tree ` 插件 | 带文件/文件夹图标的可视组件 | 可折叠展开 |
| ASCII 框图 | 依赖等宽字体，易错位 | 无 |

> **规则**：遇到需要展示目录结构的场景，使用 ` ```tree` 而非 ` ```text` 或 ASCII 框图。
