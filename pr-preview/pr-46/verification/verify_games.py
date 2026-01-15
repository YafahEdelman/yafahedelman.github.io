
from playwright.sync_api import sync_playwright, expect
import os

def verify_games_page():
    cwd = os.getcwd()
    index_url = f"file://{cwd}/index.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Open index.html
        print(f"Navigating to {index_url}")
        page.goto(index_url)

        # 2. Check for the link
        print("Checking for 'AI Designed Tiny Games' link")
        link = page.get_by_role("link", name="AI Designed Tiny Games")
        expect(link).to_be_visible()

        # 3. Click the link
        print("Clicking the link")
        link.click()

        # 4. Verify we are on games.html
        # Since it's file://, we can check the URL or content
        print("Verifying navigation to games.html")
        expect(page).to_have_url(f"file://{cwd}/games.html")

        # Verify content on games.html
        expect(page.get_by_role("heading", name="AI Designed Tiny Games")).to_be_visible()
        expect(page.get_by_role("link", name="Play RoboQuest RPG")).to_be_visible()
        expect(page.get_by_role("link", name="Play Starship Sweets")).to_be_visible()

        # 5. Screenshot
        print("Taking screenshot")
        if not os.path.exists("verification"):
            os.makedirs("verification")
        screenshot_path = "verification/games_page.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_games_page()
