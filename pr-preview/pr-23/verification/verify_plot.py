
from playwright.sync_api import sync_playwright
import os

def test_rpg_plot(page):
    # Load the local HTML file
    file_path = os.path.abspath('rpg_adventure.html')
    page.goto(f'file://{file_path}')

    # Wait for canvas to be present
    canvas = page.locator('canvas#gameCanvas')
    canvas.wait_for()

    # Wait for initial dialogue to appear
    dialogue_box = page.locator('#dialogue-box')
    page.wait_for_timeout(500)

    # Click through initial dialogue
    # "Systems online..."
    if dialogue_box.is_visible():
        dialogue_box.click()
        page.wait_for_timeout(300)

    # "Station deserted..."
    if dialogue_box.is_visible():
        dialogue_box.click()
        page.wait_for_timeout(300)

    # "Objective..."
    if dialogue_box.is_visible():
        dialogue_box.click()
        page.wait_for_timeout(300)

    # Dialogue should be gone now
    if dialogue_box.is_visible():
        dialogue_box.click()
        page.wait_for_timeout(300)

    # Move player to the first terminal at (2, 2)
    # Player starts at (2.5, 2.5) tiles => (100, 100)
    # Terminal is at (2, 2) => (80, 80)
    # The terminal is effectively to the left of the player (column 2 vs column 2.5)

    # Press Left Arrow to move left towards terminal
    page.keyboard.down('ArrowLeft')
    page.wait_for_timeout(300) # Move for 300ms
    page.keyboard.up('ArrowLeft')

    # Now we should be near the terminal.
    # Take screenshot to see "SPACE" prompt or similar
    page.screenshot(path='verification/rpg_near_terminal.png')

    # Press Space to interact
    page.keyboard.press('Space')
    page.wait_for_timeout(500) # Wait for dialogue to appear

    # Verify dialogue box is visible again with plot text
    # We expect "LOG 492..."
    expect_text = "LOG 492"
    dialogue_text = page.locator('#dialogue-text').inner_text()
    print(f"Dialogue text: {dialogue_text}")

    if expect_text in dialogue_text:
        print("Success: Plot text found!")
    else:
        print("Failure: Plot text not found.")

    # Take final screenshot
    page.screenshot(path='verification/rpg_plot_dialogue.png')

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        test_rpg_plot(page)
        browser.close()
