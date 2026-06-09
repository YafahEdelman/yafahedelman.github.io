import os
from playwright.sync_api import sync_playwright

def verify_rank_deviations():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load local file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/domain_eci.html")

        # Wait for initialization
        page.wait_for_timeout(1000)

        # Click Rank Comparison
        page.get_by_role("button", name="Rank Comparison").first.click()

        # Wait for computation and rendering
        page.wait_for_timeout(3000)

        # Verify overlay is visible
        overlay = page.locator("#breakpoint-stats")
        if overlay.is_visible():
            print("Overlay is visible.")
            text = overlay.inner_text()
            if "Rank Deviations" in text:
                print("Overlay contains 'Rank Deviations'.")
            else:
                print(f"Overlay text mismatch: {text}")
        else:
            print("Overlay is NOT visible.")

        # Verify Breakpoint Toggle is hidden
        toggle_container = page.locator("#show-breakpoint-toggle").evaluate("el => el.parentElement.classList.contains('hidden')")
        if toggle_container:
            print("Breakpoint toggle is hidden.")
        else:
            print("Breakpoint toggle is VISIBLE (Should be hidden).")

        # Take screenshot
        page.screenshot(path="verification/rank_deviations.png")

        browser.close()

if __name__ == "__main__":
    verify_rank_deviations()
