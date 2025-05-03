import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

BASE_URL = "https://uitspraken.rechtspraak.nl/"

async def fetch_html(ecli: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(BASE_URL, timeout=60000)
        await page.click("#mainSearch")
        await page.wait_for_selector("input[type='text']", timeout=10000)
        await page.fill("input[type='text']", ecli)
        await page.keyboard.press("Enter")
        await page.wait_for_selector("a[href*='document']", timeout=15000)
        await page.click("a[href*='document']")
        await page.wait_for_selector("h1", timeout=15000)

        content = await page.content()
        await browser.close()
        return content

def parse_html(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    def find_value(label: str) -> str:
        el = soup.find("label", string=label)
        if el:
            value_span = el.find_next("span", class_="rnl-details-value")
            return value_span.get_text(strip=True) if value_span else ""
        return ""

    return {
        "instantie": find_value("Instantie"),
        "datum_uitspraak": find_value("Datum uitspraak"),
        "datum_publicatie": find_value("Datum publicatie"),
        "zaaknummer": find_value("Zaaknummer"),
        "rechtsgebieden": find_value("Rechtsgebieden"),
        "inhoudsindicatie": find_value("Inhoudsindicatie")
    }

def scrape_and_parse(ecli: str) -> dict:
    html = asyncio.run(fetch_html(ecli))
    return parse_html(html)
