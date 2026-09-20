---
name: git-workflow
description: >-
  Git workflow guidelines, conventional commit messaging, clean branching strategies,
  and release preparation. Use when preparing git commits, PR descriptions, or managing release notes.
---

# Git Workflow & Conventional Commits

This skill defines standardized Git practices for clean version history and team collaboration.

## Conventional Commit Format
Follow the standard conventional commits format:
`<type>(<scope>): <subject>`

### Commit Types:
- `feat`: A new user-facing or architectural feature.
- `fix`: A bug fix or security patch.
- `refactor`: Code change that neither fixes a bug nor adds a feature.
- `test`: Adding missing tests or correcting existing tests.
- `docs`: Documentation only changes.
- `style`: Changes that do not affect the meaning of the code (white-space, formatting).
- `chore`: Maintenance, dependency updates, build tasks.

### Commit Guidelines:
- Keep the subject line under 72 characters.
- Use the imperative mood ("add feature", not "added feature").
- Separate subject from body with a blank line when detailed rationale is required.
