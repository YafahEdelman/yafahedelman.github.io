from playwright.sync_api import sync_playwright

def verify_domain_eci_additive():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto("file:///app/domain_eci.html")
        page.wait_for_selector("#chart-container")
        page.check("#show-breakpoint-toggle")
        page.wait_for_timeout(3000)

        # Check Stats Content
        content = page.locator("#breakpoint-content").inner_text()
        print(f"Stats Content:\n{content}")

        if "ECI points / year" in content:
            print("PASSED: Found 'ECI points / year' in stats.")
        else:
            print("FAILED: Did not find 'ECI points / year' in stats.")

        # Check Hover Template
        plot_data_check = page.evaluate("""() => {
            const gd = document.getElementById('chart-container');
            if (!gd.data) return "No Data";
            const traces = gd.data.filter(d => d.name === 'Linear Fit' || d.name === 'Pre-Break');
            // Return first 5 x points of Linear Fit to verify density
            return {
                templates: traces.map(t => t.hovertemplate),
                linearPoints: traces.find(d => d.name === 'Linear Fit').x.length
            };
        }""")

        print(f"Plot Data Check: {plot_data_check}")

        if any("ECI points / year" in str(t) for t in plot_data_check['templates']):
             print("PASSED: Hover templates correct.")
        else:
             print("FAILED: Hover templates incorrect.")

        if plot_data_check['linearPoints'] > 2:
            print(f"PASSED: Linear fit has {plot_data_check['linearPoints']} points (dense).")
        else:
            print(f"FAILED: Linear fit has {plot_data_check['linearPoints']} points (sparse).")

        browser.close()

if __name__ == "__main__":
    verify_domain_eci_additive()
