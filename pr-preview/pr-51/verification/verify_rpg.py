
from playwright.sync_api import sync_playwright
import os

def test_rpg(page):
    # Load the local HTML file
    file_path = os.path.abspath('rpg_adventure.html')
    page.goto(f'file://{file_path}')

    # Wait for canvas to be present
    canvas = page.locator('canvas#gameCanvas')
    canvas.wait_for()

    # Take a screenshot
    page.screenshot(path='verification/rpg_screenshot.png')

    # Check for console errors
    # Note: This part is a bit tricky in sync mode without event listeners attached before navigation,
    # but we can check if the page loaded and elements are there.

    # Check if dialogue is present (initially hidden or queue)
    # The game init queues dialogue, so it should be visible after a brief moment
    dialogue_box = page.locator('#dialogue-box')
    # It might take a frame to appear
    page.wait_for_timeout(100)

    if dialogue_box.is_visible():
        print("Dialogue box is visible")
    else:
        print("Dialogue box is NOT visible (unexpected if init ran)")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Capture console logs
        page.on("console", lambda msg: print(f"Console: {msg.text}"))
        page.on("pageerror", lambda err: print(f"Page Error: {err}"))

        test_rpg(page)
        browser.close()
