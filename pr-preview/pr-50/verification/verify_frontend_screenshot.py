from playwright.sync_api import sync_playwright

def verify_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the file directly since it is static
        page.goto("file:///app/domain_eci.html")

        # Enable Breakpoint Analysis
        page.check("#show-breakpoint-toggle")

        # Wait for analysis to complete
        page.wait_for_timeout(3000)

        # Take a screenshot
        page.screenshot(path="verification/domain_eci_screenshot.png")

        browser.close()

if __name__ == "__main__":
    verify_frontend()
