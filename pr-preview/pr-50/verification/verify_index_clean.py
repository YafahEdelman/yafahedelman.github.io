
from playwright.sync_api import sync_playwright, expect
import os

def verify_index_page():
    cwd = os.getcwd()
    index_url = f"file://{cwd}/index.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Open index.html
        print(f"Navigating to {index_url}")
        page.goto(index_url)

        # 2. Verify "AI Research & Benchmarking" is NOT visible
        print("Checking that 'AI Research & Benchmarking' is NOT visible")

        # We can check if the text exists
        content = page.content()
        if "AI Research & Benchmarking" in content:
            print("ERROR: Found 'AI Research & Benchmarking' in page content!")
            # Fail the script
            expect(page.get_by_text("AI Research & Benchmarking")).not_to_be_visible()
        else:
            print("SUCCESS: Text not found in source.")

        # 3. Screenshot
        print("Taking screenshot")
        if not os.path.exists("verification"):
            os.makedirs("verification")
        screenshot_path = "verification/index_page_clean.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_index_page()
