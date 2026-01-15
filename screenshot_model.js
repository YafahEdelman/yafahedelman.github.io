const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function screenshotModel() {
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-web-security']
    });
    const page = await browser.newPage({ viewport: { width: 600, height: 600 } });

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

    await page.waitForTimeout(1000);

    // Set up isolated model view
    await page.evaluate(() => {
        // Hide all UI elements
        document.querySelectorAll('#ui-layer, #stats-panel, #tools-panel, #instructions, #state-indicator').forEach(el => {
            if (el) el.style.display = 'none';
        });

        // Hide room elements (floor, walls, furniture)
        window.scene.children.forEach(child => {
            // Keep only the cat and lights
            if (child !== window.cat &&
                child.type !== 'DirectionalLight' &&
                child.type !== 'AmbientLight' &&
                child.type !== 'HemisphereLight') {
                child.visible = false;
            }
        });

        // Set neutral background
        window.scene.background = new THREE.Color(0xe8e8e8);

        // Reset cat to idle pose at origin
        window.cat.position.set(0, 0, 0);
        window.cat.rotation.set(0, 0, 0);

        // Reset head position
        if (window.headGroup) {
            window.headGroup.rotation.set(0, 0, 0);
            window.headGroup.position.y = 1.5;
        }

        // Reset legs to neutral
        if (window.frontLeftLeg) window.frontLeftLeg.rotation.x = 0;
        if (window.frontRightLeg) window.frontRightLeg.rotation.x = 0;
        if (window.backLeftLeg) window.backLeftLeg.rotation.x = 0;
        if (window.backRightLeg) window.backRightLeg.rotation.x = 0;

        // Reset tail
        if (window.tailGroup) {
            window.tailGroup.rotation.set(0, 0, 0.3);
        }

        // Stop animation loop updates to cat pose
        window.modelViewMode = true;
    });

    // Define camera angles
    const angles = [
        { name: 'front', x: 0, y: 3, z: 6, label: 'Front View' },
        { name: 'back', x: 0, y: 3, z: -6, label: 'Back View' },
        { name: 'left', x: -6, y: 3, z: 0, label: 'Left Side' },
        { name: 'right', x: 6, y: 3, z: 0, label: 'Right Side' },
        { name: 'top', x: 0, y: 8, z: 0.1, label: 'Top View' },
        { name: 'three-quarter', x: 4, y: 3, z: 4, label: '3/4 View' }
    ];

    const outputDir = path.join(__dirname, 'model_screenshots');
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir);
    }

    for (const angle of angles) {
        await page.evaluate((pos) => {
            window.camera.position.set(pos.x, pos.y, pos.z);
            window.camera.lookAt(0, 1, 0); // Look at cat's center
            window.renderer.render(window.scene, window.camera);
        }, angle);

        await page.waitForTimeout(200);

        const filename = path.join(outputDir, `cat_${angle.name}.png`);
        await page.screenshot({ path: filename });
        console.log(`Saved: ${angle.label} -> ${filename}`);
    }

    await browser.close();
    console.log('\nAll model screenshots saved to model_screenshots/');
}

screenshotModel().catch(console.error);
