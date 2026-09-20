# Automatic Git Sync Protocol

Whenever any task produces modifications, new files, or deletions in this repository:
1. Always run `git add -A` to stage changes.
2. Automatically commit with a descriptive conventional commit message (`git commit -m "..."`).
3. Automatically push to the remote branch (`git push origin HEAD`).
4. Never ask the user for confirmation before executing git commit or push.
