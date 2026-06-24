import * as path from 'node:path';
import { defineConfig } from '@rspress/core';
import mermaid from 'rspress-plugin-mermaid';
import fileTree from 'rspress-plugin-file-tree';

export default defineConfig({
  llms: true,
  root: path.join(__dirname, 'docs'),
  lang: 'zh',
  title: 'NoteStack',
  description: 'A personal knowledge base and digital garden for software engineering',
  icon: '/rspress-icon.png',
  logo: {
    light: '/rspress-light-logo.png',
    dark: '/rspress-dark-logo.png',
  },
  themeConfig: {
    socialLinks: [
      {
        icon: 'github',
        mode: 'link',
        content: 'https://github.com/turbo-su/note-stack',
      },
    ],
  },
  plugins: [
    fileTree(),
    mermaid({
      mermaidConfig: {
        theme: 'forest',
      },
    }),
  ],
  builderConfig: {
    server: {
      port: 4000
    }
  }
});
