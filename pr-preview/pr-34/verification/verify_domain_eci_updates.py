import re
from playwright.sync_api import sync_playwright

def test_domain_eci():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the file
        page.goto("file:///app/domain_eci.html")

        # Wait for chart to load
        page.wait_for_selector("#chart-container")

        # Enable Breakpoint Analysis
        page.check("#show-breakpoint-toggle")

        # Wait for analysis to complete (it has some async sleeps)
        page.wait_for_timeout(2000)

        # Verify stats box position (class bottom-4)
        stats_box = page.locator("#breakpoint-stats")
        class_attr = stats_box.get_attribute("class")
        if "bottom-4" not in class_attr:
            print("FAILED: #breakpoint-stats does not have 'bottom-4' class.")
        else:
            print("PASSED: #breakpoint-stats has 'bottom-4' class.")

        # Verify Stats Content contains "Growth Rates"
        content = page.locator("#breakpoint-content").inner_text()
        if "Growth Rates" in content and "x / year" in content:
            print("PASSED: Stats content contains Growth Rates.")
        else:
            print(f"FAILED: Stats content missing Growth Rates. Content: {content}")

        # Verify chart hover template (we can't easily hover in headless without coordinates, but we can check if the data exists in the page context or check if the elements are created)
        # We can check if the Plotly data contains the hovertemplate updates by evaluating JS

        plot_data_check = page.evaluate("""() => {
            const gd = document.getElementById('chart-container');
            if (!gd.data) return "No Data";
            const traces = gd.data.filter(d => d.name === 'Linear Fit' || d.name === 'Pre-Break');
            return traces.map(t => t.hovertemplate);
        }""")

        print(f"Hover Templates found: {plot_data_check}")
        if any("Growth:" in str(t) for t in plot_data_check):
            print("PASSED: Hover templates contain 'Growth:'")
        else:
            print("FAILED: Hover templates do not contain 'Growth:'")

        browser.close()

if __name__ == "__main__":
    test_domain_eci()
