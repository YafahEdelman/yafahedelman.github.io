from playwright.sync_api import sync_playwright

def verify_kitten_game():
    with sync_playwright() as p:
        # Try software rendering if hardware is not available
        browser = p.chromium.launch(headless=True, args=['--use-gl=swiftshader'])
        page = browser.new_page()

        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"PAGE ERROR: {exc}"))
        page.on("requestfailed", lambda request: print(f"FAILED: {request.url} {request.failure}"))

        # Load the file locally
        page.goto("file:///app/kitten_game.html")

        # Wait for the UI overlay to appear
        page.wait_for_selector("#ui-layer h1")

        # Wait a bit for Three.js to render
        page.wait_for_timeout(5000)

        # Take screenshot of the game
        page.screenshot(path="verification/kitten_game_debug.png")
        print("Screenshot saved to verification/kitten_game_debug.png")

        browser.close()

if __name__ == "__main__":
    verify_kitten_game()
