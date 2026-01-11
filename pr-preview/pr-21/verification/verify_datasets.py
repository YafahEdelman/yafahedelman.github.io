
from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the HTML file directly
        # Use absolute path
        cwd = os.getcwd()
        url = f"file://{cwd}/ai_chart_page.html"
        print(f"Loading {url}")

        page.goto(url)

        # Wait for the dataset list to be populated
        page.wait_for_selector("#dataset-list")

        # Check if the text contains "AI Models"
        content = page.text_content("#dataset-list")
        print(f"Dataset list content: {content}")

        if "AI Models" in content and "Benchmarks" in content:
            print("Verification Successful: Dataset list is populated.")
        else:
            print("Verification Failed: Dataset list is missing expected items.")

        # Take a screenshot
        page.screenshot(path="verification/ai_chart_page_verification.png")

        browser.close()

if __name__ == "__main__":
    run()
