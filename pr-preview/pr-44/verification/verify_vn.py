import os
from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # Load the local file
    file_path = os.path.abspath("visual_novel.html")
    page.goto(f"file://{file_path}")

    # Wait for the start button
    start_button = page.get_by_role("button", name="Start Mission")
    expect(start_button).to_be_visible()

    # Take screenshot of Title Screen
    page.screenshot(path="verification/vn_title.png")

    # Click Start
    start_button.click()

    # Wait for dialogue box to appear
    dialogue_box = page.locator(".dialogue-box")
    expect(dialogue_box).to_be_visible()

    # Wait for text to appear (Tea-Bot speaking)
    dialogue_text = page.locator("#dialogue-text")
    # Wait a bit for typing effect
    page.wait_for_timeout(2000)

    # Take screenshot of Scene 1
    page.screenshot(path="verification/vn_scene1.png")

    # Click through dialogue until choice appears
    # We know there are 5 frames in scene 1 before choices
    for _ in range(5):
        dialogue_box.click()
        page.wait_for_timeout(1000) # wait for typing/transition

    # Check for choices
    choice_btn = page.get_by_role("button", name="Offer a cup of Hot Earl Grey Tea")
    expect(choice_btn).to_be_visible()

    # Take screenshot of Choices
    page.screenshot(path="verification/vn_choices.png")

    # Click Tea Choice
    choice_btn.click()

    # Wait for new scene
    page.wait_for_timeout(1000)
    page.screenshot(path="verification/vn_tea_scene.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
