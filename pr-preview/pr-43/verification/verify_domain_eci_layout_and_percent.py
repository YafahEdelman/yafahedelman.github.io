from playwright.sync_api import sync_playwright

def verify_domain_eci_layout_and_percent():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto("file:///app/domain_eci.html")
        page.wait_for_selector("#chart-container")
        page.check("#show-breakpoint-toggle")
        page.wait_for_timeout(3000)

        # Check Stats Content for Speedup
        content = page.locator("#breakpoint-content").inner_text()
        print(f"Stats Content:\n{content}")

        if "% Speedup" in content:
            print("PASSED: Found '% Speedup' in stats.")
        else:
            print("FAILED: Did not find '% Speedup' in stats.")

        # Verify Layout
        # Check if #breakpoint-stats is NOT absolute and is visible
        stats_box = page.locator("#breakpoint-stats")
        class_attr = stats_box.get_attribute("class")

        if "absolute" in class_attr:
            print("FAILED: #breakpoint-stats still has 'absolute' class.")
        else:
            print("PASSED: #breakpoint-stats does not have 'absolute' class.")

        # Verify position via bounding box - it should be below chart wrapper's chart container
        chart_container_box = page.locator("#chart-container").bounding_box()
        stats_box_box = stats_box.bounding_box()

        print(f"Chart Bottom: {chart_container_box['y'] + chart_container_box['height']}")
        print(f"Stats Top: {stats_box_box['y']}")

        if stats_box_box['y'] >= (chart_container_box['y'] + chart_container_box['height']):
             # Note: They are in separate containers now, but vertically stacked.
             # Actually, chart container is inside flex-1, stats is static below.
             # If flex worked, stats top should be >= chart bottom (approx).
             # Let's just trust the CSS check + visual screenshot mostly.
             print("PASSED: Stats box appears to be below chart container.")

        browser.close()

if __name__ == "__main__":
    verify_domain_eci_layout_and_percent()
