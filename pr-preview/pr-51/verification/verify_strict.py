from playwright.sync_api import sync_playwright
import os

def verify(page):
    cwd = os.getcwd()
    page.goto(f"file://{cwd}/verification/repro_strict.html")
    page.wait_for_timeout(2000)

    traces = page.evaluate("document.getElementById('chart-container').data ? document.getElementById('chart-container').data.map(d => d.name) : []")
    print(f"Traces found: {traces}")

    has_pre_break = "Pre-Break" in traces
    has_post_break = "Post-Break" in traces

    page.screenshot(path="verification/verification_strict.png")

    return has_pre_break and has_post_break

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        found = verify(page)
        browser.close()

        if found:
            print("Breakpoint lines FOUND.")
        else:
            print("Breakpoint lines NOT FOUND.")
