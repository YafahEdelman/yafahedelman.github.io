import os
from playwright.sync_api import sync_playwright, expect

def verify_dataset_explorer():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the page
        file_path = os.path.abspath("ai_chart_page.html")
        page.goto(f"file://{file_path}")

        # Check title
        expect(page).to_have_title("Epoch AI Data Explorer")
        print("Page title verified.")

        # Check for dataset selector
        selector = page.locator("#dataset-select")
        expect(selector).to_be_visible()
        print("Dataset selector found.")

        # Verify default option is "AI Models"
        expect(selector).to_have_value("AI Models")
        print("Default dataset is AI Models.")

        # Select "ML Hardware"
        selector.select_option("ML Hardware")
        print("Selected ML Hardware.")

        # Check status message
        status = page.locator("#status-area")
        expect(status).to_be_visible()
        expect(status).to_contain_text("Switched to ML Hardware")
        print("Status message verified.")

        # Take screenshot
        screenshot_path = "verification/dataset_explorer.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_dataset_explorer()
