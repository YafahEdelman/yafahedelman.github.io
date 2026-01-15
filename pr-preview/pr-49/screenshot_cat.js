const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function screenshotCat(outputName = 'cat_screenshot.png', options = {}) {
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-web-security']
    });
    const page = await browser.newPage({ viewport: { width: 1000, height: 800 } });

    // Capture console logs for debugging
    page.on('console', msg => {
        if (msg.type() === 'error') console.log('Page error:', msg.text());
    });

    // Read Three.js locally
    const threejsPath = path.join(__dirname, 'three.min.js');
    const threejsCode = fs.readFileSync(threejsPath, 'utf8');

    // Inject Three.js before page loads
    await page.addInitScript(threejsCode);

    // Load the local HTML file
    const filePath = path.join(__dirname, 'kitten_game.html');
    await page.goto(`file://${filePath}`, { waitUntil: 'networkidle', timeout: 60000 });

    // Wait for Three.js scene to be ready
    await page.waitForFunction(() => {
        return typeof THREE !== 'undefined' && document.querySelector('canvas');
    }, { timeout: 30000 }).catch(() => console.log('Waited for THREE.js'));

    // Additional wait for rendering
    await page.waitForTimeout(2000);

    // Try to adjust camera via window object
    await page.evaluate((opts) => {
        if (window.cameraDistance !== undefined) {
            window.cameraDistance = opts.zoom || 8;
        }
        if (window.cameraHeight !== undefined) {
            window.cameraHeight = opts.height || 4;
        }
        if (window.cameraAngle !== undefined) {
            window.cameraAngle = opts.angle || 0.5;
        }
    }, options).catch(e => console.log('Camera adjustment skipped'));

    await page.waitForTimeout(500);

    // Take screenshot
    await page.screenshot({ path: outputName, fullPage: false });
    console.log(`Screenshot saved to: ${outputName}`);

    await browser.close();
}

const outputName = process.argv[2] || 'cat_screenshot.png';
const zoom = parseFloat(process.argv[3]) || 8;
const angle = parseFloat(process.argv[4]) || 0.5;
const height = parseFloat(process.argv[5]) || 4;

screenshotCat(outputName, { zoom, angle, height });
