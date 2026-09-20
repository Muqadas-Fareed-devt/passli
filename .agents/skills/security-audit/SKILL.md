---
name: security-audit
description: >-
  Security analysis, vulnerability scanning, OWASP Top 10 mitigation, encryption auditing,
  and authentication verification for password/vault and web applications. Use when auditing,
  securing, or reviewing authentication, sensitive data, or permissions.
---

# Security Audit & Hardening Workflow

This skill guides security analysis, secret detection, vault encryption validation, and web security compliance.

## Security Checklist

### 1. Secrets & Key Management
- Ensure no secret keys, API keys, or database credentials are hardcoded.
- Ensure `.env` is listed in `.gitignore` and `.env.example` contains only placeholder values.
- Verify cryptographic primitives (e.g. PBKDF2, Argon2, AES-GCM) use secure key derivation and randomized salts/IVs.

### 2. Access Control & Authorization (IDOR Prevention)
- Ensure every endpoint accessing private resources verifies ownership:
  ```python
  # Ensure the object belongs to the authenticated user
  document = get_object_or_404(Document, id=doc_id, user=request.user)
  ```
- Protect against privilege escalation: verify role or permission decorators (`@user_passes_test`, `LoginRequiredMixin`).

### 3. Web Vulnerabilities (OWASP Top 10)
- **SQL Injection**: Avoid raw SQL or string concatenation in queries; use ORM parameterized queries.
- **Cross-Site Scripting (XSS)**: Ensure template auto-escaping is active and mark strings `safe` only after strict sanitization.
- **Cross-Site Request Forgery (CSRF)**: Verify `{% csrf_token %}` on all POST/PUT forms and `CsrfViewMiddleware` is active in `MIDDLEWARE`.
- **Security Headers**: Ensure `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY/SAMEORIGIN`, and strict cookie settings (`SESSION_COOKIE_HTTPONLY = True`, `SESSION_COOKIE_SECURE = True`).

### 4. Audit Trail & Logging
- Log security-critical actions (logins, failed attempts, password changes, token revocations, item sharing).
- Do not log plaintext passwords, recovery codes, or sensitive payload data.
