import os
import time
from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # Load the local file
    file_path = os.path.abspath("visual_novel.html")
    page.goto(f"file://{file_path}")

    # Start
    print("Clicking Start...")
    page.get_by_role("button", name="Start Mission").click()

    dialogue_box = page.locator(".dialogue-box")
    expect(dialogue_box).to_be_visible()

    # Click through until Gloop appears
    # Limit to avoid infinite loop
    print("Clicking through Scene 1...")
    found_gloop = False
    name_tag = page.locator("#name-tag")

    for i in range(30):
        # Check if Gloop is visible
        if name_tag.is_visible():
            text = name_tag.inner_text()
            if "Ambassador Gloop" in text:
                found_gloop = True
                print(f"Found Gloop at click {i}!")
                break

        # Click to advance
        dialogue_box.click()
        # Wait a bit for typing/transition
        page.wait_for_timeout(300)

    if not found_gloop:
        print("Warning: Gloop not found!")

    page.screenshot(path="verification/vn_gloop.png")

    # Click through until choices appear
    print("Clicking until choices...")
    choices_layer = page.locator("#choices-layer")

    found_choices = False
    for i in range(20):
        if choices_layer.is_visible():
            found_choices = True
            print(f"Found choices at click {i}!")
            break
        dialogue_box.click()
        page.wait_for_timeout(300)

    if not found_choices:
        print("Error: Choices not found!")
        # Take debug screenshot
        page.screenshot(path="verification/vn_debug_no_choices.png")
    else:
        expect(choices_layer).to_be_visible()
        page.screenshot(path="verification/vn_choices.png")

        # Select Tea
        print("Selecting Tea...")
        page.get_by_role("button", name="Offer a cup of Hot Earl Grey Tea").click()

        # Verify transition to Tea Path (Ending 1)
        # Check for text "Sophisticated" or "Ending 1"
        print("Clicking through Tea Scene...")
        found_ending = False
        dialogue_text = page.locator("#dialogue-text")

        for i in range(20):
            text = dialogue_text.inner_text()
            if "SOPHISTICATED VICTORY" in text or "The treaty is signed" in text:
                found_ending = True
                print(f"Found Ending at click {i}!")
                break
            dialogue_box.click()
            page.wait_for_timeout(300)

        if not found_ending:
             print("Warning: Ending text not found.")

        page.screenshot(path="verification/vn_ending.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
