---
name: django-pro
description: >-
  Expert guidance for Django web development, ORM query optimization, database migrations,
  authentication/authorization, and Django security hardening. Use when developing,
  refactoring, or troubleshooting Django applications.
---

# Django Pro Development Workflow

This skill equips Antigravity with senior Django engineering practices for architecture, ORM optimization, migrations, and clean application design.

## Core Best Practices

### 1. ORM & Database Performance
- **N+1 Prevention**: Always use `.select_related()` for ForeignKey/OneToOne and `.prefetch_related()` for ManyToMany/Reverse relations.
- **Bulk Operations**: Use `bulk_create()`, `bulk_update()`, and `QuerySet.update()` instead of looping `.save()`.
- **Field Selection**: Use `.only()` or `.values_list()` for read-heavy operations where full model instantiation is unnecessary.
- **Transactions**: Wrap multi-step database mutations in `django.db.transaction.atomic`.

### 2. Views & Architecture
- **Class-Based Views (CBVs)**: Prefer standard CBVs (`TemplateView`, `ListView`, `DetailView`, `CreateView`, `UpdateView`) or clean function-based views with explicit decorators (`@login_required`, `@require_http_methods`).
- **Authorization Checks**: Always verify object-level ownership (e.g. `obj.user == request.user`) before permitting read/update/delete operations.
- **Forms & Validation**: Encapsulate user input validation inside `django.forms.ModelForm` or clean methods.

### 3. Migrations Management
- Check migration state: `python manage.py makemigrations --dry-run`
- Generate migrations: `python manage.py makemigrations <app_name>`
- Apply migrations: `python manage.py migrate`
- Inspect SQL: `python manage.py sqlmigrate <app_name> <migration_number>`

### 4. Verification Checklist
- Run Django system checks: `python manage.py check`
- Run automated tests: `python manage.py test`
