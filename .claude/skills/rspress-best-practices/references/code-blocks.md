# Rspress Code Blocks 语法参考

Rspress 使用 Shiki 在编译期完成语法高亮，支持丰富的 meta 属性控制代码块行为。

## 基本用法

````markdown
```js
console.log('Hello World');
```
````

## 代码块标题

````markdown
```tsx title="src/components/Button.tsx"
const Button = () => <button>Click</button>;
```
````

## 外部文件导入

通过 `file` 属性导入外部文件内容（代码块内容留空）：

````markdown
```ts file="./_example.ts"
```
````

| 路径前缀 | 解析基准 | 示例 |
| --- | --- | --- |
| `./` 或 `../` | 当前 MDX 文件所在目录 | `file="./_utils.ts"` |
| `/` | docs 目录根 | `file="/components/Button.tsx"` |
| `<root>/` | 项目根目录 | `file="<root>/src/types.ts"` |

> 导入的文件建议以 `_` 开头命名，防止 Rspress 为它们生成路由页面。

## 行高亮

### Notation 高亮（推荐）

使用 `// [!code highlight]` 注释标记，配合 `transformerNotationHighlight`：

````markdown
```ts
console.log('高亮行'); // [!code highlight]
// [!code highlight:2]  ← 高亮接下来 2 行
console.log('也会高亮');
console.log('同样高亮');
```
````

配置文件：

```ts
import { defineConfig } from '@rspress/core';
import { transformerNotationHighlight } from '@shikijs/transformers';

export default defineConfig({
  markdown: {
    shiki: {
      transformers: [transformerNotationHighlight()],
    },
  },
});
```

> **推荐原因**：formatter 可能改变行号，notation 注释随代码移动，不受影响。

### Meta 高亮

使用 `{行号}` 在 fence 上标记：

````markdown
```ts {1,3-4}
// 第 1 行高亮
// 第 2 行正常
// 第 3 行高亮
// 第 4 行高亮
```
````

需要导入 `transformerCompatibleMetaHighlight`：

```ts
import { transformerCompatibleMetaHighlight } from '@rspress/core/shiki-transformers';
```

## 行号

````markdown
```ts lineNumbers
```
````

全局启用时单块关闭：

````markdown
```ts lineNumbers=false
```
````

全局配置：

```ts
markdown: {
  showLineNumbers: true,
}
```

## 代码换行

````markdown
```ts wrapCode
```
````

全局配置：

```ts
markdown: {
  defaultWrapCode: true,
}
```

## 代码块高度控制

| Meta | 效果 |
| --- | --- |
| 无 | 完全展开 |
| `fold` | 可折叠，默认 300px，超出显示展开按钮 |
| `height="400"` | 固定高度 + 滚动条 |
| `fold height="400"` | 可折叠，折叠高度 400px（不用滚动条） |

## 其他 Shiki Transformers

```ts
import { defineConfig } from '@rspress/core';
import {
  transformerNotationHighlight,
  transformerNotationDiff,
  transformerNotationErrorLevel,
  transformerNotationFocus,
} from '@shikijs/transformers';

export default defineConfig({
  markdown: {
    shiki: {
      transformers: [
        transformerNotationHighlight(),   // [!code highlight]
        transformerNotationDiff(),         // [!code ++] / [!code --]
        transformerNotationErrorLevel(),   // [!code error] / [!code warning]
        transformerNotationFocus(),        // [!code focus]
      ],
    },
  },
});
```

| Transformer | 注释标记 | 效果 |
| --- | --- | --- |
| `transformerNotationHighlight` | `[!code highlight]` | 高亮行 |
| `transformerNotationDiff` | `[!code ++]` / `[!code --]` | 新增/删除行（绿/红） |
| `transformerNotationErrorLevel` | `[!code error]` / `[!code warning]` | 错误/警告标记 |
| `transformerNotationFocus` | `[!code focus]` | 聚焦行（其他行变暗） |

## Diff 代码块

````markdown
```diff
function test() {
- console.log('deleted');
+ console.log('added');
  console.log('unchanged');
}
```
````

## Twoslash

通过 `@rspress/plugin-twoslash` 插件启用 TypeScript 编译器级别的类型标注：

````markdown
```ts twoslash
const str: string = 'hello';
//       ^?
```
````

## Runtime 语法高亮

仅用于动态代码场景（交互式文档、远程内容），会增加运行时包体积：

```tsx
import { CodeBlockRuntime } from '@rspress/core/theme';

<CodeBlockRuntime
  lang="ts"
  title="example.ts"
  code={`console.log('Hello');`}
/>
```

> **警告**：仅在必要时使用，编译期高亮无运行时开销。

## Meta 属性速查

所有属性可自由组合，顺序不限：

```
```ts lineNumbers wrapCode title="example.ts" fold height="300" {1,3-4}
```
```
