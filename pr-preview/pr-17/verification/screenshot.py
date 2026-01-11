from playwright.sync_api import sync_playwright
import threading
import http.server
import socketserver
import os
import time

PORT = 8007

def start_server():
    os.chdir("/app")
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

def run():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(2)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(f"http://localhost:{PORT}/grid_map.html")
        time.sleep(5)

        # Open sidebar
        try:
            page.click("#menu-toggle")
            page.wait_for_selector("#sidebar:not(.translate-x-full)", timeout=3000)
            time.sleep(1)
        except:
            pass

        page.screenshot(path="verification/grid_map_final.png")
        browser.close()

if __name__ == "__main__":
    run()
