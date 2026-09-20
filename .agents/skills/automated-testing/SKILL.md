---
name: automated-testing
description: >-
  Pro automated testing workflows, unit test creation, Django test suite execution,
  test database management, mock creation, and Selenium E2E test execution. Use when writing,
  running, or debugging tests.
---

# Automated Testing & QA Workflow

This skill outlines best practices for test-driven development (TDD), regression prevention, unit testing, and E2E browser automation.

## Test Strategy

### 1. Unit & Integration Testing (Django TestCase)
- **Django TestCase**: Runs tests inside database transactions for automated isolation and rollback.
- **Client Requests**: Use `self.client.get()` / `self.client.post()` to test status codes, context variables, and redirects.
- **Factory / Setup**: Use `setUpTestData(cls)` for expensive database setup that remains unchanged across test methods.

### 2. Running Test Suites
- Run all tests:
  ```powershell
  python manage.py test
  ```
- Run tests for a specific app:
  ```powershell
  python manage.py test accounts
  python manage.py test documents
  ```
- Run a specific test class or method:
  ```powershell
  python manage.py test accounts.tests.test_views.LoginViewTests.test_successful_login
  ```
- Fast execution (keep db between runs):
  ```powershell
  python manage.py test --keepdb
  ```

### 3. Selenium & Browser E2E Tests
- Use `StaticLiveServerTestCase` to serve static files correctly during browser automation.
- Use explicit waits (`WebDriverWait` with `expected_conditions`) rather than arbitrary `time.sleep()`.
- Ensure headless driver configuration for CI/terminal environments.

### 4. Quality Standard
- Every new feature must include corresponding test cases covering:
  - Happy path
  - Invalid/malformed input
  - Unauthorized access attempt (HTTP 403 / redirect to login)
  - Edge cases (null values, boundary conditions)
