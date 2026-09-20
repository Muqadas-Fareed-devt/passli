# Passli — Secure Document Sharing Platform

> **Passli** is a web-based personal document vault and controlled document-sharing platform that allows users to store personal files securely and share specific documents using temporary, QR-based Share Passes protected by unique access keys.

---

## 🌟 Key Features

- **Personal Document Vault**: Upload and categorize sensitive documents (Medical, Education, Vehicle, Personal, Professional, Other).
- **Controlled Share Passes**: Choose exact documents to include rather than exposing your entire account.
- **Dual-Layer Access Control**: Access requires scanning a QR code endpoint **plus** entering a temporary, hashed Share Key.
- **Granular Permissions**: Restrict shared files to View-Only or allow Downloads.
- **Server-Enforced Expiration & Revocation**: Passes expire automatically after a set duration and can be revoked immediately by the owner.
- **Brute-force Protection & Audit Logs**: Rate limiting on key entry and activity logging.

---

## 🏗️ Project Architecture

```text
passli/
├── accounts/      # User authentication, registration, dashboard
├── documents/     # Vault management, document upload, categorization, storage
├── sharing/       # Share pass generation, QR code creation, recipient access
├── audit/         # Access logging, audit trail
├── config/        # Project settings & URL routing
├── static/        # CSS, JavaScript, assets
├── templates/     # HTML templates (Django templating)
├── tests/         # Unit, integration, and Selenium automation test suites
└── docs/          # Architecture and testing documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.12+
- Git

### 2. Setup Virtual Environment & Install Dependencies

```bash
python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```

### 4. Run Migrations & Start Development Server

```bash
python manage.py migrate
python manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🧪 Testing

Run standard Django test suite:
```bash
python manage.py test
```

Run Selenium automated UI tests:
```bash
python manage.py test tests.selenium
```

---

## 📄 License
MIT License
