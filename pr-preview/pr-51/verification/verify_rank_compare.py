import os
from playwright.sync_api import sync_playwright

def verify_rank_compare():
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

        # Wait for computation (there is a small delay)
        page.wait_for_timeout(2000)

        # Take screenshot
        page.screenshot(path="verification/rank_compare.png")

        browser.close()

if __name__ == "__main__":
    verify_rank_compare()
