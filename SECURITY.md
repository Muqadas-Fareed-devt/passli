# Security Policy & Cryptographic Architecture

Passli is engineered with a strict privacy-first, zero-knowledge security posture designed for controlled document sharing without credential exposure.

---

## 🛡️ Supported Versions

We actively support and release security updates for the following versions of Passli:

| Version | Supported | Security Maintenance |
| :--- | :--- | :--- |
| `1.x.x` (Current Main) | :white_check_mark: | Active Security Patches |
| `< 1.0.0` | :x: | Deprecated |

---

## 🔒 Cryptographic Specifications & Threat Model

1. **Zero-Knowledge Key Storage**:
   - Plaintext 8-character Share Keys (`XXXX-XXXX`) are generated dynamically using cryptographically secure random sources (`secrets.choice`).
   - Plaintext keys are **never stored** in the database or written to disk logs.
   - Keys are hashed with salted **PBKDF2-HMAC-SHA256** (`django.contrib.auth.hashers.make_password`).

2. **Binary Digest Integrity**:
   - Every uploaded vault document is processed through **SHA-256** checksum hashing on ingestion.
   - Binary digests allow instant verification of document integrity and detect unauthorized alteration.

3. **Multi-Tenant IDOR Protection**:
   - All vault access handlers strictly filter by `user=request.user` or authenticated session ID before serving document contents.
   - Direct object reference tampering is caught at the view boundary with HTTP 404/403 responses.

4. **Brute-Force & Rate-Limiting Defenses**:
   - Failed Share Key attempts trigger structured security logs and increment attempt counters.
   - Excess attempts enforce exponential lockouts to defeat automated credential stuffing and key enumeration.

5. **Server-Enforced Expiration & Revocation**:
   - Expiration timestamps (`expires_at`) are validated on every recipient request.
   - When a pass expires or is revoked, access is immediately terminated, and session memory is wiped.

---

## 🚨 Reporting a Vulnerability

If you discover a potential security vulnerability within Passli, please **do not open a public issue**. Instead, follow our responsible disclosure procedure:

1. Send an email with full reproduction steps to: **`security@passli.dev`**
2. Include the following details in your report:
   - Description of the vulnerability and its potential impact.
   - Step-by-step instructions or proof-of-concept (PoC) code.
   - Affected URLs, endpoints, or parameters.
   - Suggestions for mitigation or fix (optional).

### Response Timeline
- **Initial Acknowledgment**: Within 24 hours.
- **Vulnerability Assessment**: Within 48 hours.
- **Patch & Release**: Within 7 business days for critical vulnerabilities.

We credit all responsible security researchers in our release notes and Hall of Fame.
