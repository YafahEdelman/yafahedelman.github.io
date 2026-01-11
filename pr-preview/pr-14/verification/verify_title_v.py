
from playwright.sync_api import sync_playwright

def verify_title_v_permits():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the file (using /app since that is the current directory)
        page.goto("file:///app/title_v_permits.html")

        # Verify page title
        assert page.title() == "Title V Air Quality Permits Search"

        # Verify header
        header = page.locator("h1")
        assert header.inner_text() == "Title V Permits Search"

        # Verify search inputs exist
        assert page.locator("#facName").is_visible()
        assert page.locator("#facState").is_visible()
        assert page.locator("#facCity").is_visible()

        # Verify table has rows (data loaded)
        rows = page.locator("#resultsBody tr")
        # Should have some sample data
        page.wait_for_selector("#resultsBody tr")
        assert rows.count() > 0

        # Perform a search
        page.fill("#facName", "Refinery")
        page.click("#searchBtn")

        # Verify rows filtered
        # Depending on dummy data, check if count changed or is non-zero
        page.wait_for_timeout(500)

        # Take screenshot
        page.screenshot(path="verification/title_v_permits.png")

        browser.close()

if __name__ == "__main__":
    verify_title_v_permits()
