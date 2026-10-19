// Screenshot a local HTML file to PNG with headless Chrome (full page). Usage: node shoot.mjs <file-url> <out.png>
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const puppeteer = require('C:/Users/Pushkar/AppData/Local/npm-cache/_npx/0f94ee7615faf582/node_modules/puppeteer-core');
const [url, out] = process.argv.slice(2);
const browser = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true,
  args: ['--allow-file-access-from-files'] });
const page = await browser.newPage();
await page.setViewport({ width: 1354, height: 800 });
await page.goto(url, { waitUntil: 'load' });
await page.screenshot({ path: out, fullPage: true });
await browser.close();
