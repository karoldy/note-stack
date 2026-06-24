---
name: rspress-best-practices
description: Rspress best practices for config, CLI workflow, content organization, frontmatter, MDX, themes, i18n, search, static assets, deployment, and debugging. Use when writing, reviewing, or troubleshooting Rspress documentation sites.
---

# Rspress Best Practices

Apply these rules when writing or reviewing Rspress (v2) sites.

## Configuration

- Use `rspress.config.ts` and `defineConfig` from `@rspress/core`
- Set `root` explicitly when docs are not under the default `docs/` directory
- Keep site-wide settings such as `title`, `description`, `icon`, `logo`, `base`, and `lang` in config instead of repeating them in page files
- Prefer first-class Rspress options before custom theme code or low-level bundler overrides
- Keep custom theme code in a top-level `theme/` directory and import original theme pieces from `@rspress/core/theme-original`

## CLI

- Use `rspress dev` for local development
- Use `rspress build` for production output
- Use `rspress preview` only for local preview of the built site
- Use `rspress eject` only when CSS variables, class overrides, or layout wrapping cannot solve the customization

## Docs Structure And Navigation

- Keep docs content under one clear docs root and group pages by topic or workflow, not by team ownership
- Use `_meta.json` or `_nav.json` to control sidebar and navigation labels/order instead of encoding order in filenames
- Put reusable MDX snippets or shared components in shared files instead of duplicating them across pages
- Keep landing pages concise and link to deeper task-oriented guides from them

## Writing And Frontmatter

- Add clear `title` and `description` frontmatter, and set `sidebar`, `outline`, `navbar`, or `footer` only when page defaults are not enough
- Use `pageType: home`, `doc`, `doc-wide`, `custom`, or `blank` intentionally based on layout needs
- Write task-first headings and short intros; avoid marketing-heavy copy in technical docs
- Prefer one topic per page and split overly long pages by workflow or feature area
- Keep code examples minimal, runnable, and version-accurate

## MDX And Components

- Use MDX for interactive docs and embedded components, but keep the main narrative understandable as plain markdown
- Prefer documented Rspress theme/runtime APIs over importing from internal source paths
- For app-wide UI or providers, use `globalUIComponents` or theme overrides instead of repeating imports in each page

### Container (Callout)

Use `:::` syntax to highlight important information. Six built-in types: `note`, `tip`, `info`, `warning`, `danger`, `details`.

- Use lowercase type names — `:::tip`, never `:::Tip`
- Append a title inline: `:::tip 自定义标题`
- Use `details` for collapsible content blocks
- Prefer containers over raw `>` blockquotes for callouts — they render with colored borders and icons
- In MDX files, prefer inline title (`:::tip 标题`) over curly-brace syntax to avoid escaping issues
- GitHub Alerts syntax (`> [!NOTE]`) is also supported, but `:::` is more concise for Rspress-first projects

> Full syntax and examples: `references/containers.md`

### Code Blocks

Rspress uses Shiki for compile-time syntax highlighting. Meta attributes can be freely combined.

| Meta | Purpose |
| --- | --- |
| `title="..."` | Display a header bar |
| `file="./path"` | Import external file content (relative to current file, `/`-rooted to docs dir, `<root>/` for project root) |
| `lineNumbers` | Enable per-block line numbers |
| `wrapCode` | Enable per-block code wrapping |
| `fold` | Collapsible block (expand button) |
| `height="300"` | Fixed height with scrollbar; combined with `fold` controls collapsed height |
| `{1,3-4}` | Highlight specific lines via `transformerCompatibleMetaHighlight` |

- Prefer notation highlighting (`// [!code highlight]`) over meta highlighting — it survives formatter line renumbering
- Configure Shiki transformers in `rspress.config.ts` → `markdown.shiki.transformers`
- Use `CodeBlockRuntime` from `@rspress/core/theme` only for dynamic code rendering (runtime cost)
- Name file-imported code files with `_` prefix to prevent route generation

> Full syntax and examples: `references/code-blocks.md`

### Links

Rspress supports two link forms: file path (`.md`/`.mdx` extension) and URL (no extension). Both render identically.

- **Prefer relative file paths** — IDE autocomplete, file navigation, and automatic link updates on file moves
- Absolute paths start from the docs directory root
- Use `<root>/` prefix to reference files outside the docs directory
- External links automatically get `target="_blank" rel="noreferrer"`
- Use reference-style definitions for pages with many links to keep prose clean
- Custom anchor IDs: `## Heading \{#custom-id}`
- Enable `markdown.link.checkDeadLinks: true` to catch broken links at build time
- Enable `markdown.image.checkDeadImages: true` to catch missing local images
- Pick one link style (file path or URL) consistently across the project

> Full syntax and examples: `references/links.md`

### Mermaid Diagrams

Use ` ```mermaid` code blocks to render diagrams. Requires `rspress-plugin-mermaid`.

- Use `graph TD` / `graph LR` for flowcharts, `sequenceDiagram` for interactions, `graph TB` for architecture
- Pass Mermaid config via `mermaid({ mermaidConfig: { theme: 'forest' } })` in plugin options
- Prefer Mermaid over ASCII art for any architecture, flow, or sequence visualization
- Diagrams render at build time as SVG — no runtime cost

> Full syntax and examples: `references/mermaid.md`

### File Tree

Use ` ```tree` code blocks to render interactive directory structures. Requires `rspress-plugin-file-tree`.

- Use standard `tree` command output format (`├──`, `└──`, `│`)
- Configure `initialExpandDepth` to control default expansion (default `0`, `Infinity` for all)
- Use for documenting project structure, component hierarchies, or config file layouts
- The rendered output is an interactive component with collapsible folders

> Full syntax and examples: `references/file-tree.md`

## Theme And Styling

- Prefer CSS variables for brand colors, spacing, and surface styling
- Prefer BEM class overrides or `Layout` slots before ejecting built-in components
- In `theme/` files, keep `export * from '@rspress/core/theme-original'` unless intentionally replacing a named export
- Avoid full component ejection unless config, CSS, and wrapping cannot meet the requirement

## I18n, Search, And AI

- For multilingual sites, organize locale content under per-language directories and keep navigation mirrored where practical
- Keep descriptions and other frontmatter text in the same language as the page content
- Configure search intentionally: use local search for small or medium sites, and hosted search when scale or cross-version indexing requires it
- Enable `llms` or `ssgMd` only when the site benefits from machine-readable outputs, and keep descriptions accurate because those outputs surface page summaries

## Assets And Public Files

- Import source-managed images and components from docs/theme source when they belong to the content
- Use `public/` only for assets that must keep stable URL paths, such as favicons, social images, or download files
- Reference public assets by absolute site path and make sure they still work when `base` is set

## Plugins And Integration

- Prefer official Rspress plugins for search, preview, and API-doc scenarios before building custom solutions
- For component or library docs, use `@rspress/plugin-preview` and `@rspress/plugin-api-docgen` when interactive demos or API tables are needed
- Keep plugin usage explicit in config and remove unused plugins to reduce maintenance cost

### Community Plugins

| Plugin | Purpose | Code Block | Config |
| --- | --- | --- | --- |
| `rspress-plugin-mermaid` | Render Mermaid diagrams | ```` ```mermaid ```` | `mermaid({ mermaidConfig: {...} })` |
| `rspress-plugin-file-tree` | Render interactive file trees | ```` ```tree ```` | `fileTree({ initialExpandDepth: 0 })` |

```ts
// rspress.config.ts
import { defineConfig } from 'rspress/config';
import mermaid from 'rspress-plugin-mermaid';
import fileTree from 'rspress-plugin-file-tree';

export default defineConfig({
  plugins: [
    mermaid({ mermaidConfig: { theme: 'forest' } }),
    fileTree({ initialExpandDepth: Infinity }),
  ],
});
```

> Full reference: `references/mermaid.md` | `references/file-tree.md`

## Build, Deploy, And Debugging

- Validate both `rspress dev` and `rspress build`; a page that works in dev can still fail during static generation
- Verify broken links, missing assets, and wrong `base` handling before deployment
- Keep generated output out of source control unless the hosting workflow explicitly requires committed artifacts
- When debugging content issues, inspect the resolved docs root, frontmatter, and theme overrides before assuming a bundler problem

## Documentation

- For the latest Rspress docs, read https://rspress.rs/llms.txt
- Use the config and API docs when checking exact option names or current behavior
