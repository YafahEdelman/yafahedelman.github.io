from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 375, 'height': 812},
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True
        )
        page = context.new_page()

        page.goto(f"file://{os.getcwd()}/domain_eci.html")

        # 1. Verify Status Bar is hidden
        status_bar = page.locator('#status-text')
        if status_bar.is_visible():
            print("Status bar is visible (FAIL)")
        else:
            print("Status bar is hidden (PASS)")

        # 2. Verify Rank Comparison Mode UI
        page.click('#mobile-menu-btn')
        page.wait_for_timeout(500)
        page.click('#mobile-mode-rank-compare')
        page.wait_for_timeout(2000)
        page.screenshot(path="verification/mobile_rank_compare.png")

        # 3. Verify Standard Compare Mode UI
        page.click('#mobile-menu-btn')
        page.wait_for_timeout(500)
        page.click('#mobile-mode-compare')
        page.wait_for_timeout(2000)
        page.screenshot(path="verification/mobile_compare_hidden_stats.png")

        # 4. Verify Breakpoint Mode UI
        page.click('#mobile-menu-btn')
        page.wait_for_timeout(500)
        page.click('#mobile-mode-fixed') # Auto-closes sidebar
        page.wait_for_timeout(500)

        # Re-open sidebar to toggle breakpoint
        page.click('#mobile-menu-btn')
        page.wait_for_timeout(500)
        page.click('#mobile-show-breakpoint-toggle')

        # Close sidebar manually
        page.click('#sidebar-close-btn')
        page.wait_for_timeout(2000)

        page.screenshot(path="verification/mobile_breakpoint_stats.png")

        browser.close()

if __name__ == "__main__":
    run()
