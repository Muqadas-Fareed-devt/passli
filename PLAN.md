# Passli — Secure Document Sharing Platform

## 1. Project Overview

**Passli** is a web-based personal document vault and controlled document-sharing platform.

The core problem:
Users often need to carry multiple documents such as medical reports, certificates, vehicle documents, identity documents, and other files. Passli allows users to store these documents digitally and share selected documents without giving the recipient access to the user's full account.

### Core concept

```text
User Account
    |
    v
Personal Document Vault
    |
    | select documents
    v
Share Pass
    |
    +-- QR Code
    +-- Temporary Share Key
    +-- Permissions
    +-- Expiration
    +-- Revocation
    |
    v
Recipient scans QR
    |
    v
Share Access Page
    |
    v
Recipient enters Share Key
    |
    v
Key + Pass validation
    |
    v
Selected documents only
```

**Important:** The QR code does NOT directly grant document access. It only identifies the share-access endpoint. The recipient must also provide the Share Key.

---

## 2. Project Goals

### Primary goals

1. Allow users to create an account.
2. Allow users to upload and manage personal documents.
3. Organize documents into categories.
4. Allow users to select specific documents for sharing.
5. Generate a Share Pass containing:
   - QR code
   - temporary/random Share Key
   - selected documents
   - permissions
   - expiration
6. Allow recipients to scan the QR code and enter the Share Key.
7. Grant access only when the Share Key is valid and the Share Pass is active.
8. Allow the owner to revoke a Share Pass immediately.
9. Provide view/download permissions.
10. Keep owner account access completely separate from recipient share access.
11. Provide automated Selenium tests for the web application.
12. Deploy a usable public version and maintain the project in a public Git repository.

---

## 3. Scope — MVP

The first version should stay focused. Do NOT add unnecessary AI features, medical diagnosis, OCR, blockchain, or other unrelated functionality.

### A. Authentication

- User registration
- User login
- User logout
- Authenticated dashboard
- Password hashing using the framework's secure password system

### B. Document Management

Users can:

- Upload documents
- Give documents a name
- Select a category
- Add an optional description
- View document metadata
- Preview/view supported files
- Download documents
- Delete documents

Initial supported file types:

- PDF
- JPG/JPEG
- PNG

Initial categories:

- Medical
- Education
- Vehicle
- Personal
- Professional
- Other

### C. Share Pass

The owner can:

1. Select one or more documents.
2. Choose permissions.
3. Choose expiration.
4. Generate a Share Pass.

Example:

```text
Share Pass

Documents:
[X] Blood Test.pdf
[X] X-Ray.pdf
[X] Prescription.pdf
[ ] CNIC.pdf

Permissions:
[X] View
[X] Download

Expiration:
30 minutes

[Generate Share Pass]
```

### D. QR Code

The generated QR code should contain only a secure/random share URL or token.

It must NOT contain:

- The document files
- The user's password
- The Share Key in plaintext
- Sensitive personal information
- Predictable user/document IDs as the only security mechanism

Example concept:

```text
https://example.com/share/<random-token>
```

### E. Share Key

A random Share Key is generated separately from the QR code.

Example:

```text
8K7P-42XM
```

The Share Key should:

- Be unpredictable
- Be stored securely (preferably as a hash, not plaintext)
- Have a limited validity period when the pass is temporary
- Be validated server-side
- Have protection against brute-force attempts

### F. Recipient Access

Recipient flow:

```text
Scan QR
   |
   v
Share Access Page
   |
   v
Enter Share Key
   |
   v
Server validation
   |
   +---- invalid --> Access denied
   |
   +---- expired --> Access expired
   |
   +---- revoked --> Access revoked
   |
   +---- valid --> Shared documents
```

The recipient does NOT need a normal Passli account for MVP share access.

### G. Permissions

MVP permissions:

- View
- Download

Examples:

```text
View = allowed
Download = allowed
```

or:

```text
View = allowed
Download = denied
```

The backend must enforce these permissions.

### H. Expiration

Initial options:

- 10 minutes
- 30 minutes
- 1 hour
- 6 hours
- 24 hours
- Until revoked

Expiration must be enforced by the backend, not only by a frontend countdown.

### I. Revocation

The owner can revoke an active Share Pass.

After revocation:

```text
QR + valid-looking key
        |
        v
      DENIED
```

Revocation must take effect immediately.

### J. Access History

MVP should record basic share-access events:

- Share Pass
- Timestamp
- Success/failure
- Basic action such as view/download where appropriate

Avoid collecting unnecessary sensitive information.

---

## 4. Security Requirements

Security is a core part of Passli.

### Authentication

Use the framework's secure password hashing and session/authentication mechanisms.

### Authorization

Every document operation must verify that the authenticated user owns the document or has valid share authorization.

Never trust IDs supplied by the browser.

### Share tokens

Use cryptographically secure random tokens.

Do not use predictable IDs such as:

```text
/share/1
/share/2
/share/3
```

as the security mechanism.

### Share keys

Never store raw Share Keys if avoidable.

Preferred model:

```text
Generated Key
      |
      v
Secure Hash
      |
      v
Database
```

When the recipient submits a key, compare it securely against the stored hash.

### Brute-force protection

Repeated invalid Share Key attempts should be rate-limited or temporarily blocked.

### Expiration

Expiration must be checked on the server for every protected share request.

### Revocation

Revocation must be checked on every protected share request.

---

## 5. Recommended Architecture

For MVP, prioritize simplicity and maintainability.

### Backend

**Python + Django**

Recommended supporting components:

- Django REST Framework only if an API is needed
- Django authentication
- Django ORM
- Django file handling

### Frontend

For MVP:

- Django templates
- Tailwind CSS or clean CSS
- JavaScript only where needed

Do not introduce React/Next.js unless there is a clear reason.

### Database

Development:

```text
SQLite
```

Production:

```text
PostgreSQL
```

### File storage

Development:

```text
local media storage
```

Production:

```text
S3-compatible object storage
```

### QR generation

Use a maintained Python QR-code library.

---

## 6. Core Data Model

Initial conceptual models:

### User

```text
id
name
email
password_hash
created_at
```

### Document

```text
id
user_id
name
category
description
file_path
file_type
file_size
created_at
updated_at
```

### SharePass

```text
id
user_id
share_token
share_key_hash
expires_at
status
allow_view
allow_download
created_at
revoked_at
access_count
```

### SharePassDocument

Many-to-many relationship:

```text
share_pass_id
document_id
```

This allows one Share Pass to contain multiple selected documents.

### AccessLog

```text
id
share_pass_id
timestamp
action
success
```

The exact implementation can be refined during development.

---

## 7. Main Pages

### Public

```text
/
```

Landing page explaining Passli.

### Authentication

```text
/register
/login
/logout
```

### Authenticated user

```text
/dashboard
/documents
/documents/upload
/documents/<id>
/documents/<id>/download
/share/create
/share/passes
/share/passes/<id>
/share/passes/<id>/revoke
```

### Recipient

```text
/share/<random-token>
```

This page should NOT expose the owner's dashboard.

---

## 8. Dashboard

Suggested dashboard sections:

```text
Passli
--------------------------------

My Documents
  Medical       6
  Education     4
  Vehicle       3
  Personal      5

[Upload Document]

Active Share Passes

Doctor Visit
3 documents
Expires in 22 minutes

[View] [Show QR] [Revoke]

Recent Activity
...
```

The UI should be clean, modern, responsive, and suitable for a real public project.

---

## 9. Share Pass UX

### Step 1 — Select documents

```text
Create Share Pass

[X] Blood Test.pdf
[X] X-Ray.pdf
[X] Prescription.pdf
[ ] CNIC.pdf
```

### Step 2 — Permissions

```text
[X] View
[X] Download
```

### Step 3 — Expiration

```text
30 minutes
```

### Step 4 — Generate

System creates:

```text
Share URL
QR Code
Share Key
```

### Step 5 — Display

```text
Share Pass Created

[ QR CODE ]

Share Key:
8K7P-42XM

Expires:
30 minutes

[Download QR]
[Revoke Pass]
```

---

## 10. Recipient UX

After scanning:

```text
Passli
Secure Document Access

This Share Pass requires an access key.

Share Key:
[____________]

[Access Documents]
```

Success:

```text
Shared Documents

Blood Test.pdf
[View] [Download]

X-Ray.pdf
[View] [Download]

Prescription.pdf
[View] [Download]

Expires in: 18:32
```

Failure states:

```text
Invalid Share Key
Share Pass Expired
Share Pass Revoked
Share Pass Not Found
Download Not Permitted
```

---

## 11. Selenium Testing Scope

This project is also being built for a Software Engineering assignment requiring Selenium WebDriver testing.

The assignment requires testing:

1. Open website
2. Verify page title
3. Test navigation
4. Test text input
5. Test a button

It also requires:

- Complete Selenium source code
- Test case document
- Test steps
- Expected result
- Actual result
- Pass/Fail status
- Screenshots
- Short execution report
- Project presentation

### Required test cases

```text
TC01 — Open Passli
TC02 — Verify page title
TC03 — Test navigation
TC04 — Test text input
TC05 — Test button
```

### Extended product tests

```text
TC06 — Register user
TC07 — Login
TC08 — Upload document
TC09 — Verify uploaded document
TC10 — Create Share Pass
TC11 — Generate QR
TC12 — Invalid Share Key
TC13 — Valid Share Key
TC14 — View shared document
TC15 — Download shared document
TC16 — Revoke Share Pass
TC17 — Access revoked Share Pass
TC18 — Expired Share Pass
TC19 — Download denied when permission is disabled
```

Use stable element IDs/data attributes for Selenium selectors.

Example:

```html
data-testid="generate-share-pass"
data-testid="share-key-input"
data-testid="access-documents"
```

Avoid fragile selectors based on CSS layout or visible text where practical.

---

## 12. Development Phases

### Phase 0 — Naming and branding

- Finalize project name
- Create GitHub repository
- Create README skeleton
- Define visual identity

### Phase 1 — Project setup

- Django project
- Environment configuration
- Database
- Base layout
- Static/media handling

### Phase 2 — Authentication

- Registration
- Login
- Logout
- Protected dashboard

### Phase 3 — Documents

- Upload
- Categories
- Metadata
- View
- Download
- Delete

### Phase 4 — Share Pass

- Document selection
- Permissions
- Expiration
- Secure token
- Secure key
- Database models

### Phase 5 — QR

- QR generation
- QR display
- QR download

### Phase 6 — Recipient access

- Share URL
- Key verification
- Permission enforcement
- Document access

### Phase 7 — Security

- Authorization checks
- Key hashing
- Rate limiting
- Expiration checks
- Revocation
- Secure file access

### Phase 8 — Access history

- Access logs
- Owner activity page

### Phase 9 — UI/UX

- Responsive design
- Empty states
- Error states
- Loading states
- Success notifications
- Accessibility basics

### Phase 10 — Selenium

- Selenium test framework
- Required assignment tests
- Extended tests
- Screenshots
- Test report

### Phase 11 — Deployment

- Production database
- Production file storage
- Environment variables
- HTTPS
- Deployment
- Smoke tests

### Phase 12 — Documentation

- README
- Architecture diagram
- Setup instructions
- API/documentation if applicable
- Selenium test documentation
- Screenshots
- Demo instructions

---

## 13. MVP Definition of Done

MVP is complete when:

- [ ] User can register/login.
- [ ] User can upload supported documents.
- [ ] User can categorize documents.
- [ ] User can view/download/delete owned documents.
- [ ] User can select specific documents.
- [ ] User can create a Share Pass.
- [ ] Share Pass generates a secure QR URL.
- [ ] Share Pass generates a separate Share Key.
- [ ] Share Key is securely stored.
- [ ] Recipient can scan/open the QR URL.
- [ ] Recipient must provide the Share Key.
- [ ] Invalid keys are rejected.
- [ ] Expired passes are rejected.
- [ ] Revoked passes are rejected.
- [ ] View permission is enforced.
- [ ] Download permission is enforced.
- [ ] Owner account is never exposed through recipient access.
- [ ] Basic access events are recorded.
- [ ] Selenium tests pass.
- [ ] Test screenshots are captured.
- [ ] Application is deployable.
- [ ] README explains setup and architecture.

---

## 14. Explicit Non-Goals for MVP

Do NOT implement these unless they are intentionally added in a future version:

- Medical diagnosis
- Medical recommendations
- AI document analysis
- OCR
- Blockchain
- Cryptocurrency
- Facial recognition
- Complex enterprise organization management
- Full hospital/EHR integration
- Social networking
- Chat system
- Automatic document classification using AI
- Mobile native application

The product's value comes from **secure document storage and controlled sharing**, not from adding unrelated AI features.

---

## 15. Future Roadmap

Potential future versions:

### v1.1

- One-time Share Keys
- Maximum-use limits
- Better access logs
- Document preview improvements
- Bulk download

### v1.2

- Two-factor authentication
- Email verification
- Password reset
- Multiple active Share Passes
- Custom Share Pass names

### v2

- PWA/mobile experience
- Organization accounts
- Doctor/clinic sharing workflows
- University certificate sharing
- Business document rooms
- API access

---

## 16. Project Principles

All AI agents/developers working on Passli should follow these rules:

1. **Security before convenience** for document sharing.
2. Never expose private documents through predictable URLs.
3. Never treat a QR code alone as authorization.
4. Never store Share Keys in plaintext.
5. Always enforce authorization server-side.
6. Always enforce expiration server-side.
7. Always enforce revocation server-side.
8. Keep recipient access separate from owner authentication.
9. Keep the MVP focused.
10. Do not add AI features merely for marketing.
11. Prefer simple, maintainable architecture.
12. Write tests for important functionality.
13. Use stable selectors for Selenium.
14. Do not commit secrets, credentials, uploaded private files, or production environment variables to Git.
15. Treat medical and identity documents as highly sensitive data.

---

## 17. Product Positioning

### Short description

> **Passli is a secure personal document vault that lets users share selected documents through QR-based Share Passes protected by temporary access keys.**

### Core differentiator

```text
Store documents
      +
Select exactly what to share
      +
QR as the access endpoint
      +
Separate temporary Share Key
      +
Granular permissions
      +
Expiration
      +
Revocation
```

The goal is not simply to make a QR-code document viewer. The goal is to build a small, security-conscious **controlled document-sharing platform**.

---

## 18. Suggested Repository Structure

```text
passli/
│
├── README.md
├── PLAN.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── manage.py
│
├── config/
│   ├── settings/
│   ├── urls.py
│   └── ...
│
├── accounts/
├── documents/
├── sharing/
├── audit/
│
├── templates/
├── static/
├── media/                 # local development only; ignored by Git
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── selenium/
│
└── docs/
    ├── architecture.md
    ├── testing.md
    └── screenshots/
```

**Note:** The exact Django app structure can be adjusted during implementation. The functional scope above should remain stable unless explicitly changed.

---

## 19. First Development Task

Before implementing features, the next agent should:

1. Confirm the final project/repository name.
2. Initialize the Git repository.
3. Create the Django project.
4. Configure development settings.
5. Create the initial apps:
   - `accounts`
   - `documents`
   - `sharing`
   - `audit`
6. Configure the database.
7. Create the base layout and landing page.
8. Run the project locally.
9. Commit the clean initial scaffold.

Do not implement Share Pass functionality until the authentication and document ownership model are established.
