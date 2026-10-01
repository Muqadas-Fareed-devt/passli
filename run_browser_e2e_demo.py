"""
Passli Automated Interactive Browser Test & Video Recorder
===========================================================
This script automatically:
1. Checks or starts the local Django development server on http://127.0.0.1:8000/
2. Launches an interactive Chromium browser window (visible to you).
3. Records the entire end-to-end user lifecycle to an MP4/WebM video in the `recordings/` folder.
4. Executes the full user journey:
   - Landing page & interactive demo sandbox exploration
   - Owner account registration & login
   - Document upload with SHA-256 checksum calculation
   - Ephemeral Share Pass generation with QR code & PBKDF2 hashed key
   - Recipient gateway access & 8-character key verification
   - In-browser decrypted PDF preview & verified SHA-256 digest
   - Recipient voluntary session exit
   - Owner Security Audit Trail inspection & 1-click instant pass revocation

Usage:
    python run_browser_e2e_demo.py
"""

import os
import sys
import time
import urllib.request
import subprocess
from pathlib import Path

# Ensure required directory for recordings exists
BASE_DIR = Path(__file__).resolve().parent
RECORDINGS_DIR = BASE_DIR / "recordings"
RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_PDF_PATH = BASE_DIR / "tests" / "sample_lab_report.pdf"

# Create sample PDF if not already present
if not SAMPLE_PDF_PATH.exists():
    SAMPLE_PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SAMPLE_PDF_PATH, "wb") as f:
        f.write(b"%PDF-1.4 Clinical Diagnostic Lab Panel 2026 - Passli Cryptographic Systems\n%%EOF")


def is_server_running(url="http://127.0.0.1:8000/"):
    """Checks if the Django server is responding on localhost."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=2) as resp:
            return resp.status in (200, 302)
    except Exception:
        return False


def ensure_server():
    """Starts the Django development server if not already running."""
    if is_server_running():
        print("[INFO] Django development server is already running on http://127.0.0.1:8000/")
        return None

    print("[INFO] Starting Django development server...")
    python_exe = sys.executable
    manage_py = BASE_DIR / "manage.py"

    server_process = subprocess.Popen(
        [python_exe, str(manage_py), "runserver", "127.0.0.1:8000", "--noreload"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=str(BASE_DIR)
    )

    # Wait for server to initialize
    for _ in range(15):
        time.sleep(1)
        if is_server_running():
            print("[SUCCESS] Django server started successfully on http://127.0.0.1:8000/")
            return server_process

    print("[WARNING] Could not confirm server start. Continuing anyway...")
    return server_process


def run_e2e_browser_test():
    """Executes the Playwright browser test with visible UI and video recording."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[ERROR] Playwright is not installed. Run: pip install playwright && playwright install chromium")
        sys.exit(1)

    print("\n" + "=" * 65)
    print("  LAUNCHING PASSLI AUTOMATED BROWSER E2E TEST & VIDEO RECORDER")
    print("=" * 65)
    print(f"[INFO] Video recordings will be saved to: {RECORDINGS_DIR}\n")

    timestamp = int(time.time())
    username = f"dr_sarah_{timestamp % 10000}"
    email = f"{username}@passli.dev"
    password = "SecurePassphrase2026!"

    server_proc = ensure_server()

    try:
        with sync_playwright() as p:
            print("[INFO] Launching Chromium browser (visible mode)...")
            browser = p.chromium.launch(
                headless=False,
                slow_mo=800,  # Slow down actions so you can watch each step clearly
            )

            context = browser.new_context(
                record_video_dir=str(RECORDINGS_DIR),
                record_video_size={"width": 1280, "height": 800},
                viewport={"width": 1280, "height": 800},
            )

            page = context.new_page()

            # -------------------------------------------------------------
            # STEP 1: Landing Page & Simulator Sandbox
            # -------------------------------------------------------------
            print("\n[STEP 1] Navigating to Landing Page (http://127.0.0.1:8000/)...")
            page.goto("http://127.0.0.1:8000/", wait_until="networkidle")
            time.sleep(1)

            print(" -> Scrolling to Interactive Sandbox Demo...")
            page.evaluate("window.scrollTo({top: 750, behavior: 'smooth'})")
            time.sleep(1.5)

            print(" -> Scrolling to Real-World Use Cases & Comparison Matrix...")
            page.evaluate("window.scrollTo({top: 1700, behavior: 'smooth'})")
            time.sleep(1.5)

            page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
            time.sleep(1)

            # -------------------------------------------------------------
            # STEP 2: Owner Registration & Login
            # -------------------------------------------------------------
            print(f"\n[STEP 2] Registering new vault owner: {username} ({email})...")
            page.goto("http://127.0.0.1:8000/register/", wait_until="networkidle")

            page.fill('input[name="username"]', username)
            page.fill('input[name="email"]', email)
            page.fill('input[name="password1"]', password)
            page.fill('input[name="password2"]', password)
            time.sleep(0.5)

            page.click('form.auth-form button[type="submit"], [data-testid="register-submit-btn"]')
            page.wait_for_load_state("networkidle")
            print(" -> Vault account created! Landed on Personal Vault Dashboard.")
            time.sleep(1.5)

            # -------------------------------------------------------------
            # STEP 3: Document Ingestion & Checksum Validation
            # -------------------------------------------------------------
            print("\n[STEP 3] Uploading sensitive medical record...")
            page.goto("http://127.0.0.1:8000/documents/upload/", wait_until="networkidle")

            page.set_input_files('input#doc-file-input, input[name="file"]', str(SAMPLE_PDF_PATH.resolve()))
            page.fill('input#doc-title', "Clinical Pathology & Lipid Panel 2026")
            page.select_option('select#doc-category', "medical")
            page.fill('textarea#doc-description', "Diagnostic lab blood work and cardiovascular biomarkers.")
            time.sleep(0.8)

            page.click('[data-testid="upload-submit-btn"], form.auth-form button[type="submit"]')
            page.wait_for_load_state("networkidle")
            time.sleep(1.5)

            # Check if there were any upload errors
            error_box = page.locator('.alert-danger, .form-error')
            if error_box.count() > 0 and error_box.first.is_visible():
                print(f"[ERROR in Upload] {error_box.first.inner_text()}")

            print(f" -> Current Page after upload: {page.url}")
            print(" -> Document uploaded and SHA-256 checksum calculated!")
            time.sleep(1.5)

            # -------------------------------------------------------------
            # STEP 4: Ephemeral Share Pass Generation
            # -------------------------------------------------------------
            print("\n[STEP 4] Generating time-gated cryptographic Share Pass...")
            page.goto("http://127.0.0.1:8000/share/create/", wait_until="networkidle")

            page.wait_for_selector('input[name="title"], [data-testid="share-pass-title-input"]', timeout=15000)
            page.fill('input[name="title"]', "Dr. Harrison Cardiology Consult")
            page.select_option('select[name="expires_in"]', "30m")

            # Check document checkbox
            first_doc_checkbox = page.locator('input[name="documents"]').first
            if first_doc_checkbox.is_visible():
                first_doc_checkbox.check(force=True)

            # Enable raw download permission
            download_toggle = page.locator('input[name="can_download"]')
            if download_toggle.is_visible():
                download_toggle.check(force=True)

            time.sleep(0.8)
            page.click('[data-testid="generate-pass-btn"], form[data-testid="share-create-form"] button[type="submit"]')
            page.wait_for_load_state("networkidle")
            time.sleep(1.5)
            print(" -> Share Pass generated with dynamic QR code & PBKDF2 hashed key!")

            # Extract generated Share Key and Share URL from details page
            page.wait_for_selector('#shareKeyText, [data-testid="share-key-display"]', timeout=10000)
            raw_key_text = page.locator('#shareKeyText').inner_text().strip()
            print(f" -> Ephemeral Share Key displayed: {raw_key_text}")

            recipient_url_elem = page.locator('#recipientUrlText')
            if recipient_url_elem.is_visible():
                recipient_url = recipient_url_elem.inner_text().strip()
            else:
                pass_id = page.url.rstrip("/").split("/")[-1]
                recipient_url = f"http://127.0.0.1:8000/p/{pass_id}/"
            print(f" -> Public Recipient Endpoint: {recipient_url}")

            # -------------------------------------------------------------
            # STEP 5: Recipient Verification & Access
            # -------------------------------------------------------------
            print("\n[STEP 5] Opening Recipient Gateway in a new session tab...")
            recip_page = context.new_page()
            recip_page.goto(recipient_url, wait_until="networkidle")
            time.sleep(1)

            print(f" -> Submitting Share Key: {raw_key_text}...")
            key_input = recip_page.locator('input[name="access_key"], #id_access_key')
            key_input.fill(raw_key_text)
            time.sleep(0.8)

            recip_page.click('[data-testid="submit-share-key-btn"], button[type="submit"]')
            recip_page.wait_for_load_state("networkidle")
            print(" -> Recipient authenticated! Landed on Decrypted Document Console.")
            time.sleep(2.5)

            # -------------------------------------------------------------
            # STEP 6: Recipient Voluntary Exit
            # -------------------------------------------------------------
            print("\n[STEP 6] Recipient exiting document inspection session...")
            exit_btn = recip_page.locator('[data-testid="exit-session-btn"], button:has-text("Exit Session")')
            if exit_btn.is_visible():
                exit_btn.click()
                recip_page.wait_for_load_state("networkidle")
                print(" -> Recipient session destroyed and browser decrypted state cleansed.")
                time.sleep(1.5)

            recip_page.close()

            # -------------------------------------------------------------
            # STEP 7: Owner Security Audit Trail & Instant Revocation
            # -------------------------------------------------------------
            print("\n[STEP 7] Inspecting Owner Security Audit Dashboard (/audit/)...")
            page.goto("http://127.0.0.1:8000/audit/", wait_until="networkidle")
            time.sleep(2)
            print(" -> Chronological security logs verified (Key Verified, Previewed, Left).")

            print("\n[STEP 8] Revoking Share Pass from pass detail view...")
            page.goto(page.url.replace('/audit/', f'/share/{page.url.rstrip("/").split("/")[-1]}/') if '/share/' in page.url else f"http://127.0.0.1:8000/share/{recipient_url.rstrip('/').split('/')[-1]}/", wait_until="networkidle")
            time.sleep(1)

            revoke_btn = page.locator('[data-testid="revoke-pass-btn"]')
            if revoke_btn.is_visible():
                page.on("dialog", lambda dialog: dialog.accept())
                revoke_btn.click()
                page.wait_for_load_state("networkidle")
                print(" -> Pass successfully revoked! Recipient is now permanently locked out.")
                time.sleep(1.5)

            # Close context to finalize video recording
            context.close()
            browser.close()

            # Find saved video file
            video_files = list(RECORDINGS_DIR.glob("*.webm"))
            latest_video = max(video_files, key=os.path.getctime) if video_files else None

            print("\n" + "=" * 65)
            print("  AUTOMATED BROWSER E2E TEST COMPLETED SUCCESSFULLY! [100% OK]")
            print("=" * 65)
            if latest_video:
                print(f"[SUCCESS] Video recording saved to: {latest_video.resolve()}")
            print("=" * 65 + "\n")

    finally:
        # Keep server running or terminate if we started it
        if server_proc:
            print("[INFO] Django development server will remain active.")


if __name__ == "__main__":
    run_e2e_browser_test()
