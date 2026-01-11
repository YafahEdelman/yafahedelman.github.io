import os
from playwright.sync_api import sync_playwright

def verify(page):
    page.on("console", lambda msg: print(f"PAGE CONSOLE: {msg.text}"))
    page.on("pageerror", lambda exc: print(f"PAGE ERROR: {exc}"))

    cwd = os.getcwd()
    page.goto(f"file://{cwd}/domain_eci.html")
    page.wait_for_timeout(1000)

    page.get_by_label("Frontier Breakpoint Analysis").check()
    page.wait_for_timeout(1000)

    # Inject data centered around theta=100 (diff=100)
    page.evaluate("""
        const linearPoints = [];
        const now = Date.now();
        const day = 24*60*60*1000;
        for(let i=0; i<20; i++) {
            linearPoints.push({
                x: now + i * 30 * day,
                y: 0.2 + (i/20) * 0.6 // 0.2 to 0.8
            });
        }

        window.RAW_DATA = {
            models: {},
            benchmarks: { "LinearBench": { name: "LinearBench", domain: "Test", diff: 100, disc: 1 } },
            performances: {}
        };

        for(let i=0; i<20; i++) {
            const mId = "Model" + i;
            window.RAW_DATA.models[mId] = { name: mId, date: new Date(linearPoints[i].x).toISOString() };
            window.RAW_DATA.performances[mId] = { "LinearBench": linearPoints[i].y };
        }

        state.selectedBenchmarks = new Set(["LinearBench"]);
        state.minBenchmarks = 1;
        state.mode = 'fixed';
        state.showBreakpoint = true;

        console.log("Mock data injected (Better Range). Calling updateChart...");

        renderBenchmarkList();
        updateChart().then(() => {
            console.log("UpdateChart Promise Resolved");
        });
    """)

    page.wait_for_timeout(3000)

    traces = page.evaluate("document.getElementById('chart-container').data ? document.getElementById('chart-container').data.map(d => d.name) : []")
    print(f"Traces found: {traces}")

    # Take screenshot
    page.screenshot(path="verification/verification.png")

    has_pre_break = "Pre-Break" in traces
    has_post_break = "Post-Break" in traces

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
