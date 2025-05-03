from bs4 import BeautifulSoup
from pathlib import Path

HTML_PATH = Path("uitspraak_rendered.html")

with open(HTML_PATH, encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Functie om metadata op basis van het label te vinden
def extract_metadata(label_text):
    label = soup.find("label", string=lambda t: t and t.strip() == label_text)
    if label:
        value_span = label.find_next_sibling("span")
        return value_span.get_text(strip=True) if value_span else "Niet gevonden"
    return "Niet gevonden"

# Extract specifieke velden
resultaten = {
    "Instantie": extract_metadata("Instantie"),
    "Datum uitspraak": extract_metadata("Datum uitspraak"),
    "Datum publicatie": extract_metadata("Datum publicatie"),
    "Zaaknummer": extract_metadata("Zaaknummer"),
    "Rechtsgebieden": extract_metadata("Rechtsgebieden"),
    "Inhoudsindicatie": extract_metadata("Inhoudsindicatie"),
}

# Print het resultaat
for veld, waarde in resultaten.items():
    print(f"{veld}: {waarde}")
