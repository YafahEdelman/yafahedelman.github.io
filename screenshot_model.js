const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function screenshotModel() {
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-web-security']
    });
    const page = await browser.newPage({ viewport: { width: 500, height: 500 } });

    page.on('console', msg => {
        if (msg.type() === 'error' && !msg.text().includes('ERR_TUNNEL')) {
            console.log('Page error:', msg.text());
        }
    });

    // Inject Three.js before page loads
    const threejsPath = path.join(__dirname, 'three.min.js');
    const threejsCode = fs.readFileSync(threejsPath, 'utf8');
    await page.addInitScript(threejsCode);

    // Load the game
    const filePath = path.join(__dirname, 'kitten_game.html');
    await page.goto(`file://${filePath}`, { waitUntil: 'networkidle', timeout: 60000 });

    // Wait for scene to be ready
    await page.waitForFunction(() => {
        return typeof THREE !== 'undefined' &&
               document.querySelector('canvas') &&
               window.scene &&
               window.cat;
    }, { timeout: 30000 });

    await page.waitForTimeout(500);

    // Initial setup - hide everything except cat
    await page.evaluate(() => {
        // Hide all UI
        document.querySelectorAll('#ui-layer, #stats-panel, #tools-panel, #instructions, #state-indicator').forEach(el => {
            if (el) el.style.display = 'none';
        });

        // Set neutral background
        window.scene.background = new THREE.Color(0xdddddd);

        // Hide all scene objects except cat and lights
        window.scene.children.forEach(child => {
            if (child !== window.cat &&
                child.type !== 'DirectionalLight' &&
                child.type !== 'AmbientLight' &&
                child.type !== 'HemisphereLight' &&
                child.type !== 'PointLight') {
                child.visible = false;
            }
        });

        // Traverse entire scene and hide sprites/particles
        window.scene.traverse(obj => {
            if (obj.type === 'Sprite' || obj.type === 'Points') {
                obj.visible = false;
            }
        });
    });

    // Define views: rotate cat to show different angles, camera stays fixed at +Z
    const views = [
        { name: 'front', catRotY: 0, label: 'Front View' },             // Cat faces +Z (toward camera)
        { name: 'back', catRotY: Math.PI, label: 'Back View' },         // Cat faces -Z (away)
        { name: 'left', catRotY: -Math.PI / 2, label: 'Left Side' },    // Cat's left visible
        { name: 'right', catRotY: Math.PI / 2, label: 'Right Side' },   // Cat's right visible
        { name: 'three-quarter', catRotY: -Math.PI / 4, label: '3/4 View' }
    ];

    const outputDir = path.join(__dirname, 'model_screenshots');
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir);
    }

    for (const view of views) {
        await page.evaluate((v) => {
            // Reset cat position and set rotation for this view
            window.cat.position.set(0, 0, 0);
            window.cat.rotation.set(0, v.catRotY, 0);

            // Reset head
            if (window.headGroup) {
                window.headGroup.rotation.set(0, 0, 0);
                window.headGroup.position.set(0, 1.75, 0.9);
            }

            // Reset tail
            if (window.tailGroup) {
                window.tailGroup.rotation.set(-0.4, 0, 0.3);
            }

            // Position camera for tight framing - close up
            window.camera.position.set(0, 1.0, 1.5);
            window.camera.lookAt(0, 0.8, 0);

            // Force render
            window.renderer.render(window.scene, window.camera);
        }, view);

        await page.waitForTimeout(100);

        const filename = path.join(outputDir, `cat_${view.name}.png`);
        await page.screenshot({ path: filename });
        console.log(`Saved: ${view.label} -> ${filename}`);
    }

    // Top view - special camera position
    await page.evaluate(() => {
        window.cat.position.set(0, 0, 0);
        window.cat.rotation.set(0, 0, 0);
        window.camera.position.set(0, 2, 0.01);
        window.camera.lookAt(0, 0, 0);
        window.renderer.render(window.scene, window.camera);
    });
    await page.waitForTimeout(100);
    await page.screenshot({ path: path.join(outputDir, 'cat_top.png') });
    console.log('Saved: Top View -> model_screenshots/cat_top.png');

    await browser.close();
    console.log('\nAll model screenshots saved to model_screenshots/');
}

screenshotModel().catch(console.error);
