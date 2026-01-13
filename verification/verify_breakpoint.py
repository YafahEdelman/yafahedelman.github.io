import os
from playwright.sync_api import sync_playwright

def verify_breakpoint_analysis():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Determine the file path
        cwd = os.getcwd()
        file_path = f"file://{cwd}/domain_eci.html"

        print(f"Navigating to {file_path}")
        page.goto(file_path)

        # Wait for page load
        page.wait_for_load_state("networkidle")

        # 1. Enable 'Frontier Breakpoint'
        print("Enabling Frontier Breakpoint...")
        page.check("#show-breakpoint-toggle")

        # 2. Select enough benchmarks to ensure we have data
        # Default is Math, which has many benchmarks.
        # Let's ensure 'GSM8K', 'MATH level 5', 'MMLU' are selected if they aren't by default (Math includes them usually)
        # But let's click 'Select All' for a domain just to be safe and get plenty of points.

        # Wait for list to render
        page.wait_for_selector("#benchmark-list > div")

        # Select "Coding" domain to mix things up or just stick to defaults if they work.
        # Let's just use the current selection if it yields points.
        # Check if chart has points.
        page.wait_for_timeout(2000)

        # Check if Breakpoint Analysis box is visible
        # It shows up if enough points are present.
        # "#breakpoint-stats"

        try:
            page.wait_for_selector("#breakpoint-stats", state="visible", timeout=5000)
            print("Breakpoint stats visible.")
        except:
            print("Breakpoint stats not visible yet. Selecting more benchmarks.")
            # Select 'Knowledge' domain
            page.select_option("#domain-selector", "Knowledge")
            page.click("#select-all")
            page.wait_for_timeout(2000)
            page.wait_for_selector("#breakpoint-stats", state="visible", timeout=5000)
            print("Breakpoint stats now visible.")

        # 3. Wait for analysis to complete (it says "Running statistical analysis..." then "Analysis complete.")
        # We can check the text content of #status-text or just wait a bit since we added async yields.
        print("Waiting for analysis...")
        page.wait_for_timeout(5000) # Give it time to run the 1000 bootstraps

        # 4. Take screenshot
        screenshot_path = f"{cwd}/verification/breakpoint_verification.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        page.screenshot(path=screenshot_path, full_page=False)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_breakpoint_analysis()
