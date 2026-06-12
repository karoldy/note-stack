# CLAUDE.md

## Project Overview

NoteStack is a personal knowledge base and digital garden built with Rspress.

The purpose of this repository is to collect, organize, and share knowledge related to:

* Frontend Engineering
* Backend Engineering
* DevOps
* AI & LLM
* Software Architecture
* Engineering Practices
* Career Development
* Productivity

This project prioritizes:

1. Practicality over theory
2. Long-term maintainability
3. Searchability
4. Clear examples
5. Developer-friendly documentation

---

## Tech Stack

* Rspress
* Markdown
* TypeScript
* React
* Node.js

---

## Writing Guidelines

When generating documentation:

### General Rules

* Use concise and professional language.
* Prefer Chinese unless explicitly requested otherwise.
* Avoid marketing language.
* Avoid unnecessary introductions.
* Focus on actionable information.

### Document Structure

Every document should follow this structure when applicable:

```md
# Title

## Overview

Brief introduction.

## Prerequisites

Required knowledge or setup.

## Steps

Detailed instructions.

## Examples

Practical examples.

## Best Practices

Recommended approaches.

## References

Related links and resources.
```

---

## Code Examples

### TypeScript

Prefer:

```ts
interface User {
  id: string;
  name: string;
}
```

Avoid:

```ts
type User = any;
```

### React

Prefer:

* Functional Components
* Hooks
* TypeScript
* Composition

Avoid:

* Class Components
* Deprecated APIs

### Next.js

Prefer:

* App Router
* Server Components when appropriate
* Route Handlers
* TypeScript

---

## Documentation Categories

New content should be placed in the most relevant category.

### Frontend

Path:

```text
docs/frontend/
```

Topics:

* React
* Vue
* Next.js
* Nuxt
* TypeScript
* Rspack
* Vite
* Webpack

---

### Backend

Path:

```text
docs/backend/
```

Topics:

* Node.js
* NestJS
* Express
* GraphQL
* Authentication
* Database

---

### DevOps

Path:

```text
docs/devops/
```

Topics:

* Docker
* Kubernetes
* CI/CD
* GitHub Actions
* Linux

---

### AI

Path:

```text
docs/ai/
```

Topics:

* LLM
* AI Engineering
* Prompt Engineering
* Claude Code
* OpenAI
* MCP

---

### Engineering

Path:

```text
docs/engineering/
```

Topics:

* Design Patterns
* Architecture
* Monorepo
* Project Structure
* Testing

---

### Career

Path:

```text
docs/career/
```

Topics:

* Interview Preparation
* Learning Notes
* Productivity
* Career Growth

---

## Content Style

Prefer:

* Step-by-step explanations
* Real-world examples
* Production-ready solutions
* Comparison tables
* Decision-making guidance

Avoid:

* Academic writing
* Excessive theory
* Placeholder examples
* Unverified information

---

## Repository Conventions

### File Naming

Use kebab-case.

Example:

```text
react-hooks-guide.md
nextjs-authentication.md
nestjs-graphql-jwt.md
```

Avoid:

```text
ReactGuide.md
MyNotes.md
```

### Directory Naming

Use lowercase and kebab-case.

Example:

```text
frontend/react/
backend/nestjs/
```

---

## Contribution Rules For Claude

When creating or updating content:

1. Follow existing folder structure.
2. Do not duplicate existing content.
3. Link related documents whenever possible.
4. Prefer practical examples.
5. Keep markdown formatting consistent.
6. Use TypeScript for code samples unless another language is explicitly requested.
7. Generate production-oriented examples instead of toy examples.

---

## Mission

Build a high-quality engineering knowledge base that remains useful years from now.

Every document should answer at least one real problem encountered during software development.
