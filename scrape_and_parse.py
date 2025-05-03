# citation-scraper-backend/scrape_and_parse.py

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
import sys

async def fetch_html(ecli):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await (await browser.new_context()).new_page()

        await page.goto("https://uitspraken.rechtspraak.nl", timeout=60000)
        await page.fill("input[type='text']", ecli)
        await page.keyboard.press("Enter")
        await page.wait_for_selector("a[href^='/details?id=']", timeout=15000)
        await page.click("a[href^='/details?id=']")
        await page.click("a[href*='document']")
        await page.wait_for_selector("h1", timeout=15000)

        html = await page.content()
        await browser.close()
        return html

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    def get_value(label):
        el = soup.find("label", string=label)
        if el:
            value_span = el.find_next_sibling("span")
            return value_span.get_text(strip=True) if value_span else ""
        return ""

    return {
        "instantie": get_value("Instantie"),
        "datum_uitspraak": get_value("Datum uitspraak"),
        "datum_publicatie": get_value("Datum publicatie"),
        "zaaknummer": get_value("Zaaknummer"),
        "rechtsgebieden": get_value("Rechtsgebieden"),
        "inhoudsindicatie": get_value("Inhoudsindicatie"),
    }

if __name__ == "__main__":
    ecli = sys.argv[1]
    html = asyncio.run(fetch_html(ecli))
    data = parse_html(html)
    print(json.dumps(data))
