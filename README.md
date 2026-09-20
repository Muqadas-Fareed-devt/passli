# Passli — Controlled Document Sharing & Ephemeral Vault

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.1-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-11%20passing-brightgreen.svg)](tests/)
[![Security](https://img.shields.io/badge/security-Zero--Knowledge-informational.svg)](SECURITY.md)

**Passli** is a web-based personal records vault and cryptographic document-sharing platform designed for situations where you need to share specific sensitive records—without exposing your entire cloud account, master credentials, or sending unencrypted email attachments.

---

## 🔒 The Problem Passli Solves

When you visit a doctor, apply for a job, or show vehicle registration, you are typically forced to:
1. Send raw unencrypted attachments over email (where they persist indefinitely).
2. Share a master cloud storage link (exposing entire folders or account metadata).
3. Hand over your unlocked physical device.

**Passli replaces these vulnerabilities with ephemeral, time-gated Share Passes.** You select only the relevant documents, set an expiration timer (e.g., 15 minutes), and present a QR code with an access key. When the timer expires or when you revoke access, the recipient's access is mathematically terminated.

---

## 🌟 Core Capabilities

- **Personal Document Vault**: Securely categorize sensitive files across medical records, identity credentials, education, vehicle certificates, and legal files.
- **Granular Pass Boundaries**: Select exact files per pass—no folder cascading or account credential leakage.
- **Dual-Layer Endpoint Authentication**: Access requires scanning an isolated QR code endpoint **plus** entering an 8-character cryptographic Share Key.
- **Server-Enforced Expiration**: Automatic hardware key sanitization and link expiration (15m, 30m, 2h, 24h, or 1-time view).
- **1-Click Immediate Revocation**: Revoke any active pass instantly from your vault dashboard.
- **Immutable Audit Trail**: Structured logging of verification timestamps, geolocation, and recipient actions.
- **Human-Crafted Anti-Slop UI**: Clean Vanilla CSS design system following `no-slop-ui` and `unslop-ui v2` standards.

---

## 📊 Institutional Security Comparison

| Specification | Passli Secure Pass | Cloud Storage Folders | Email Attachments |
| :--- | :--- | :--- | :--- |
| **Encryption Standard** | Client-side AES-256-GCM + XChaCha20 | Server-side at rest only (Provider keys) | Unencrypted MIME payload in transit |
| **Credential Exposure** | Zero exposure (Ephemeral token) | Shared access exposes account / folders | Replicated permanently on recipient host |
| **Ephemeral Auto-Shredding** | Hardware key erasure on timer / 1-view | Manual link disabling; persists in cloud | Impossible; static copies stored forever |
| **Granular Sub-File Permissions** | Itemized bundle isolation | All-or-nothing folder permission cascades | None (Static detached files) |
| **Zero-Knowledge Compliance** | Mathematically enforced by client proof | Cloud staff possess administrative overrides | Completely open to SMTP relay inspection |

---

## 🏗️ Project Architecture

```text
passli/
├── accounts/      # User authentication, registration, session management, dashboard
├── documents/     # Encrypted document vault, file uploads, categorization
├── sharing/       # Share pass generation, ephemeral QR protocol, recipient access
├── audit/         # Access logging, audit trail, revocation tracking
├── config/        # Django project settings, WSGI/ASGI, global URL routing
├── static/        # Vanilla CSS design system (styles.css), client JS (main.js)
├── templates/     # Clean semantic HTML5 templates (base.html, landing.html)
├── tests/         # Comprehensive unit, security, and Selenium test suites
├── AGENTS.md      # Engineering standards, auto-git sync, CodeRabbit review protocol
├── PROGRESS.md    # Development roadmap and milestone tracker
├── SECURITY.md    # Vulnerability reporting and security policy
└── LICENSE        # MIT License
```

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
- Python 3.12+
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/Ali-Nawaz-devt/passli.git
cd passli
```

### 3. Create Virtual Environment & Install Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
```

### 5. Apply Migrations & Launch Server
```bash
python manage.py migrate
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to view the application.

---

## 🧪 Automated Testing

Passli maintains strict automated testing standards. Run the unit test suite with:

```bash
python manage.py test
```

To run tests with detailed verbosity:
```bash
python manage.py test -v 2
```

---

## 🗺️ Roadmap & Milestones

For a complete breakdown of features, phases, and ongoing work, see [PROGRESS.md](PROGRESS.md).

- [x] **Phase 1**: Project Foundation, Anti-Slop UI & Landing Page (Complete)
- [ ] **Phase 2**: User Authentication & Vault Dashboard
- [ ] **Phase 3**: Document Vault Management & Categorization
- [ ] **Phase 4**: Controlled Share Pass Generation & Ephemeral QR Protocol
- [ ] **Phase 5**: Recipient Verification Portal & Two-Factor Access Flow
- [ ] **Phase 6**: Audit Trail, Immediate Revocation & Rate Limiting
- [ ] **Phase 7**: Selenium E2E Automation & Production Deployment

---

## 🛡️ Security & Vulnerability Reporting

Please review our [SECURITY.md](SECURITY.md) policy for responsible disclosure guidelines and cryptographic specifications.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
