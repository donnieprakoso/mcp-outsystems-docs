# Spec-First Test-Driven Development (SFTDD) Template

A workflow template for building applications with AI assistance while maintaining full control through Test-Driven Development.

## What is SFTDD?

Spec-First TDD combines the clarity of specifications with the control of Test-Driven Development, giving you back the power by:
- **Atomic Use Cases**: Work in tiny, digestible "beads" of functionality
- **Human-in-the-Loop**: You're the pilot, not just watching agents work
- **Evolutionary Specs**: The spec becomes airtight _because_ you built it, not before you started

## Quick Start

### 1. Clone this template
```bash
git clone https://github.com/donnieprakoso/spec-first-tdd.git
cd spec-first-tdd
```

### 2. Define your project context
Open `00-use-case.md` and fill in:
- Project name and description
- Tech stack (language, framework, testing tools)
- Architecture decisions
- Development environment

### 3. Prompt your AI assistant
```
Read 00-sftdd-workflow.md and understand its context.
Read 00-use-case.md. I've added a new use case: #1 [Your Use Case].
Process this use case.
```

### 4. Follow the TDD cycle
- **Red**: AI creates failing test
- **Green**: You write code (or ask AI) to pass the test
- **Enhancement**: AI suggests edge cases
- **Refactor**: You improve code quality (or ask AI)

### 5. Repeat for each use case

## Files in This Template

| File | Purpose |
|------|---------|
| `00-sftdd-workflow.md` | System prompt for AI (read this first) |
| `00-use-case.md` | Feature development tracker |
| `00-issues.md` | Production bug tracker |
| `README.md` | This file |

## The Three Modes

### 🔧 Feature Development
- Add use case to `00-use-case.md` (title + description only)
- AI creates tests and code
- You approve each phase

### 🐛 Issue Resolution
- Add issue to `00-issues.md` (title + description only)
- AI triages and fixes
- Same TDD cycle

### 💡 Brainstorming
- Say "Don't change anything yet"
- AI analyzes and proposes
- No code changes

## Example Workflow

```markdown
# In 00-use-case.md

## 1. User authentication
**Description**: User should be able to log in with email and password
```

Then prompt:
```
I've added use case #1. Process this use case.
```

AI responds:
```
🔧 Entering Feature Development Mode for Use Case #1: User authentication

Here's a failing test:
[test code]
```

You run the test, confirm it fails (Red), then continue through Green → Enhancement → Refactor.

## Prerequisites

- Understanding of unit testing and your chosen testing framework
- Comfortable with AI tools but want more control
- Willing to follow TDD discipline

## Contributing

Found an issue or have a suggestion? Open an issue or submit a PR!

## License

MIT License - feel free to use this template for your projects.

---

**Take the power back.** 🎸

— [Donnie Prakoso](https://github.com/donnieprakoso)
