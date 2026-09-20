# Pro Developer Engineering Rules

## 1. Codebase Integrity
- Before modifying any core files, check existing implementations and cross-references.
- Never remove existing tests or comment out failing assertions; fix the root cause.
- Adhere to the principle of least privilege in view permissions and model mutations.

## 2. Windows Environment Compatibility
- Use PowerShell-compatible syntax for command proposals.
- Use forward slashes (`/`) in markdown links and path representations where cross-platform tools parse paths.
- Ensure virtual environment paths (e.g. `.venv\Scripts\python.exe`) are respected during command execution.

## 3. Performance & Resource Safety
- Ensure heavy operations (like file hashing, bulk encryption, or PDF export) do not block main thread request handling.
- Use streaming responses or chunked file processing for large media/vault exports.
