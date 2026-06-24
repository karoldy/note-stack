# Rspress Links 语法参考

Rspress 支持两种链接形式，渲染结果完全相同，仅在代码约定上有差异。

## 文件路径形式

包含 `.md` / `.mdx` 扩展名，指向实际文件：

| 类型 | 示例 |
| --- | --- |
| 相对路径 | `[开始](../start/getting-started.mdx)` |
| 绝对路径 | `[开始](/guide/start/getting-started.mdx)` |
| 带 locale 绝对路径 | `[开始](/zh/guide/start/getting-started.mdx)` |
| 跨 locale 链接 | `[English](/en/guide/start/getting-started.mdx)` |

绝对路径的根是 docs 目录。启用 i18n 后，`markdown.link.autoPrefix` 自动补全 locale 前缀。

### 为什么推荐文件路径形式

1. **IDE 支持**：自动补全、文件导航、移动文件时自动更新链接
2. **GitHub 兼容**：GitHub 和其他 Markdown 编辑器能正确解析
3. **不依赖 `cleanUrls`**：无论 `cleanUrls` 如何配置都能正确跳转

## URL 形式

不带文件扩展名：

| 类型 | 示例 |
| --- | --- |
| 相对路径 | `[开始](../start/getting-started)` |
| 绝对路径 | `[开始](/guide/start/getting-started)` |
| 带 `.html` | `[开始](/guide/start/getting-started.html)` |
| 带 locale | `[开始](/zh/guide/start/getting-started.html)` |

Rspress 根据 `cleanUrls` 设置自动处理 `.html` 后缀。

## 外部链接

指向当前站点之外的链接自动添加 `target="_blank" rel="noreferrer"`，无需手动设置：

```markdown
[Rspack 文档](https://rspack.rs)
```

## 锚点链接

锚点 ID 由标题内容自动生成：

```markdown
[跳到代码块部分](#code-blocks)

[跳到另一个页面的锚点](../guide/config.mdx#build)
```

### 自定义锚点 ID

```markdown
## Hello world \{#custom-id}
```

## 引用式定义

页面内链接较多时，使用引用式语法保持正文整洁：

```markdown
Rspress 支持[文件路径形式]和 [URL 形式]。

[文件路径形式]: ../start/getting-started.mdx
[URL 形式]: /guide/start/getting-started
```

## 静态资源链接

`public/` 目录下的文件使用绝对路径引用：

```markdown
![OG Image](/og-image.png)
```

插件生成的文件（如 `@rspress/plugin-llms` 的 `/llms-full.txt`）同理。

## 死链检查

### 死链接检测

```ts
// rspress.config.ts
export default defineConfig({
  markdown: {
    link: {
      checkDeadLinks: true,
    },
  },
});
```

排除特定路径：

```ts
markdown: {
  link: {
    checkDeadLinks: {
      excludes: ['/og-image.png', '/llms-full.txt'],
    },
  },
},
```

### 死图片检测

```ts
markdown: {
  image: {
    checkDeadImages: true,
  },
},
```

## 关键规则

| 规则 | 说明 |
| --- | --- |
| 统一风格 | 整个项目选用文件路径或 URL 形式，保持一致 |
| IDE 优先 | 相对路径 + 文件扩展名 = 最佳 IDE 体验 |
| 外部链接自动处理 | 不用手动写 `target="_blank"` |
| 启用死链检查 | `checkDeadLinks: true` 在构建时发现问题 |
| `public/` 资源 | 绝对路径引用，添加到死链排除列表 |
| 自定义锚点 | 用 `\{#id}` 覆盖自动生成的标题 ID |
