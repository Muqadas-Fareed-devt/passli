# Security Policy

Passli is engineered with privacy and cryptographic security as core design tenets. We take all vulnerability reports seriously and appreciate responsible disclosure.

---

## Supported Versions

Security updates are actively maintained for the following branches and releases:

| Version | Supported          | Security Patches |
| ------- | ------------------ | ---------------- |
| `main`  | :white_check_mark: | Active           |
| `< 1.0` | :white_check_mark: | Development      |

---

## Cryptographic Architecture & Threat Model

Passli implements a defensive zero-knowledge architecture for sensitive document sharing:

1. **Client-Side Envelope Encryption**:
   - Files are encrypted on the client or in transit using AES-256-GCM / XChaCha20-Poly1305 before permanent storage.
   - Master account credentials are never shared with pass recipients.
2. **Ephemeral Share Keys**:
   - Share passes are protected by short-lived, randomly generated 8-character access keys.
   - Key hashes are validated server-side; raw keys are held strictly in recipient memory.
3. **Server-Enforced Expiration & Immediate Revocation**:
   - Time-to-live (TTL) counters are enforced by the server backend.
   - Once expired or manually revoked by the vault owner, access is permanently blocked and cryptographic keys are sanitized.
4. **Brute-Force & Rate Limiting**:
   - Ephemeral pass endpoints enforce strict rate limits on failed key attempts to eliminate brute-force attack vectors.
5. **Auditing & Immutable Access Logs**:
   - Every verification attempt, document access, and revocation is recorded in structured audit logs with timestamps and client metadata.

---

## Reporting a Vulnerability

If you discover a potential security vulnerability in Passli, please **do not** file a public GitHub issue.

### Reporting Procedure

1. Send an email to **security@passli.dev** (or open a Private Vulnerability Report on GitHub).
2. Include the following details in your report:
   - Type of vulnerability (e.g., IDOR, XSS, CSRF, cryptographic weakness, bypass).
   - Step-by-step instructions or Proof of Concept (PoC) to reproduce the issue.
   - Affected files, endpoints, or components.
   - Potential impact of exploitation.
3. We will acknowledge receipt of your report within **24 hours** and provide regular progress updates as we triage and patch the issue.

### Responsible Disclosure Guidelines

- Please allow us reasonable time to investigate and release a fix before disclosing any information publicly.
- Do not attempt to access, modify, or destroy user data during testing.
- Do not execute denial-of-service (DoS/DDoS) attacks against production infrastructure.

---

## Security Best Practices for Self-Hosting

When deploying Passli in production environments:
- Always set `DEBUG=False` in your `.env` configuration.
- Generate a cryptographically secure `SECRET_KEY` using `python -c 'import secrets; print(secrets.token_urlsafe(50))'`.
- Enforce HTTPS / TLS 1.3 across all incoming traffic.
- Configure secure session cookies (`SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True`, `SECURE_HSTS_SECONDS = 31536000`).
