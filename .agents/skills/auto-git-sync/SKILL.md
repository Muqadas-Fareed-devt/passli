---
name: auto-git-sync
description: >-
  Automatically stages, commits with conventional commit messages, and pushes code changes to GitHub
  after completing any task or prompt without waiting for or asking the user. Use whenever code or files
  are modified or created.
---

# Automated Git Commit & Push Workflow

This skill ensures that all changes produced during an agent turn are immediately and safely committed to Git and pushed to the upstream GitHub remote repository without prompting the user.

## Automated Execution Procedure

Whenever files are created, modified, or deleted in the workspace:

1. **Inspect Working Directory**:
   ```powershell
   git status --porcelain
   ```

2. **Stage Changes**:
   Stage all modified, added, or deleted files (respecting `.gitignore`):
   ```powershell
   git add -A
   ```

3. **Generate Conventional Commit Message**:
   Analyze the changes and generate a clear, descriptive commit message:
   - Format: `<type>(<scope>): <concise action description>`
   - Examples:
     - `feat(auth): implement two-factor authentication views`
     - `fix(vault): sanitize document metadata export`
     - `chore(skills): install auto-git-sync and pro developer skills`

4. **Commit Changes**:
   ```powershell
   git commit -m "<type>(<scope>): <summary>"
   ```

5. **Push to Remote Branch**:
   ```powershell
   git push origin HEAD
   ```

6. **Safety Rules**:
   - Do NOT ask the user for confirmation before committing or pushing.
   - Ensure secrets, `.env` files, or `.sqlite3` runtime database files are never committed by verifying `.gitignore`.
