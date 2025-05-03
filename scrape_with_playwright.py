import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ECLI = "ECLI:NL:RBDHA:2018:8801"
BASE_URL = f"https://uitspraken.rechtspraak.nl/#!/details?id={ECLI}"
OUTPUT_DIR = Path(".")
HTML_PATH = OUTPUT_DIR / "uitspraak_rendered.html"
IMG_PATH = OUTPUT_DIR / "uitspraak_screenshot.png"

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print(f"🌐 Stap 1: Open directe uitspraakpagina voor {ECLI}...")
        await page.goto(BASE_URL, timeout=60000)
        await page.wait_for_timeout(5000)  # Wacht even zodat alles kan laden

        print("📸 Pagina geladen, neem screenshot en HTML...")
        await page.screenshot(path=str(IMG_PATH), full_page=True)
        HTML_PATH.write_text(await page.content(), encoding="utf-8")

        print(f"✅ Screenshot opgeslagen als {IMG_PATH.name}")
        print(f"✅ HTML opgeslagen als {HTML_PATH.name}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
