from __future__ import annotations

import argparse
import csv
import re
import time
from pathlib import Path
from typing import Iterable
from urllib.parse import urlencode, urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.truckscout24.com"
SEARCH_PATH = "/main/search/index"
DEFAULT_PARAMS = {
    "mainCategoryIds": "246",
    "subCategoryIds": "",
    "manufacturers": "",
    "models[0]": "",
    "priceTo": "",
    "usePriceGross": "0",
    "manufacturedFrom": "",
    "countries": "",
    "properties[axle configuration][value]": "",
}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; TruckProjectBot/1.0; +https://www.truckscout24.com)",
    "Accept-Language": "en-US,en;q=0.9",
}
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "truck_data_raw.csv"
COLUMNS = [
    "title",
    "price",
    "manufacturer",
    "model",
    "year",
    "mileage",
    "power",
    "fuel_type",
    "gearbox",
    "axle_configuration",
    "location",
    "ad_url",
]


def build_search_url(page: int = 1) -> str:
    params = DEFAULT_PARAMS.copy()
    if page > 1:
        params["page"] = str(page)
    return f"{BASE_URL}{SEARCH_PATH}?{urlencode(params)}"


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def extract_year(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"(19|20)\d{2}", value)
    if match:
        return int(match.group())
    return None


def split_manufacturer_and_model(title: str, manufacturer: str = "") -> tuple[str, str]:
    title = clean_text(title)
    manufacturer = clean_text(manufacturer)

    if manufacturer:
        manufacturer_index = title.lower().find(manufacturer.lower())
        if manufacturer_index >= 0:
            model = title[manufacturer_index + len(manufacturer) :].strip(" -")
            return manufacturer, model or title

    parts = title.split(maxsplit=1)
    if not manufacturer and parts:
        manufacturer = parts[0]
    model = parts[1] if len(parts) > 1 else ""
    return manufacturer, model


def extract_price(card: BeautifulSoup) -> str:
    price_block = card.select_one('div[data-grid="price"]')
    if price_block is None:
        return ""

    text = clean_text(price_block.get_text(" ", strip=True))
    match = re.search(r"€\s?[\d,.]+", text)
    if match:
        return clean_text(match.group())
    return text


def parse_detail_pairs(card: BeautifulSoup) -> dict[str, str]:
    footer = card.select_one("section.grid-footer .description-preview")
    if footer is None:
        return {}

    text = clean_text(footer.get_text(" ", strip=True))
    patterns = {
        "mileage": r"mileage:\s*(.*?)(?=\s+[A-Za-z][A-Za-z /-]+:|$)",
        "power": r"power:\s*(.*?)(?=\s+[A-Za-z][A-Za-z /-]+:|$)",
        "fuel_type": r"fuel type:\s*(.*?)(?=\s+[A-Za-z][A-Za-z /-]+:|$)",
        "gearbox": r"gearing type:\s*(.*?)(?=\s+[A-Za-z][A-Za-z /-]+:|$)",
        "axle_configuration": r"axle configuration:\s*(.*?)(?=\s+[A-Za-z][A-Za-z /-]+:|$)",
        "year": r"(?:Year of construction|first registration):\s*(.*?)(?=\s+[A-Za-z][A-Za-z /-]+:|$)",
    }

    values: dict[str, str] = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            values[key] = clean_text(match.group(1).strip(" ,"))
    return values


def extract_listing(card: BeautifulSoup) -> dict[str, str | int | None]:
    title_link = card.select_one('a[data-grid="title"]')
    location_block = card.select_one('div[data-grid="location"] .country-name')
    manufacturer_tag = title_link.select_one(".me-1") if title_link else None
    category_tag = title_link.select_one(".text-gray-100") if title_link else None

    title = clean_text(title_link.get_text(" ", strip=True) if title_link else "")
    category = clean_text(category_tag.get_text(" ", strip=True) if category_tag else "")
    if category and title.lower().startswith(category.lower()):
        title = clean_text(title[len(category) :])
    manufacturer, model = split_manufacturer_and_model(
        title=title,
        manufacturer=manufacturer_tag.get_text(strip=True) if manufacturer_tag else "",
    )
    details = parse_detail_pairs(card)
    detail_year = details.get("year", "")

    return {
        "title": title,
        "price": extract_price(card),
        "manufacturer": manufacturer,
        "model": model,
        "year": extract_year(detail_year),
        "mileage": details.get("mileage", ""),
        "power": details.get("power", ""),
        "fuel_type": details.get("fuel_type", ""),
        "gearbox": details.get("gearbox", ""),
        "axle_configuration": details.get("axle_configuration", ""),
        "location": clean_text(location_block.get_text(" ", strip=True) if location_block else ""),
        "ad_url": urljoin(BASE_URL, title_link.get("href", "")) if title_link else "",
    }


def fetch_page(page: int, session: requests.Session) -> list[dict[str, str | int | None]]:
    response = session.get(build_search_url(page), timeout=30)
    if response.status_code == 404:
        return []
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select("section[data-listing-id]")
    return [extract_listing(card) for card in cards]


def scrape_trucks(max_pages: int = 3, pause_seconds: float = 1.0) -> list[dict[str, str | int | None]]:
    session = requests.Session()
    session.headers.update(HEADERS)

    rows: list[dict[str, str | int | None]] = []
    for page in range(1, max_pages + 1):
        try:
            page_rows = fetch_page(page, session)
        except requests.RequestException as error:
            print(f"Arret a la page {page}: {error}")
            break
        if not page_rows:
            print(f"Arret a la page {page}: aucune annonce trouvee.")
            break
        rows.extend(page_rows)
        print(f"Page {page}: {len(page_rows)} annonces recuperees")
        time.sleep(pause_seconds)
    return rows


def save_to_csv(rows: Iterable[dict[str, str | int | None]], output_path: Path = OUTPUT_PATH) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape truck ads from TruckScout24.")
    parser.add_argument("--pages", type=int, default=3, help="Number of result pages to scrape.")
    parser.add_argument("--pause", type=float, default=1.0, help="Pause between pages in seconds.")
    args = parser.parse_args()

    rows = scrape_trucks(max_pages=args.pages, pause_seconds=args.pause)
    output_path = save_to_csv(rows)
    print(f"{len(rows)} annonces sauvegardees dans {output_path}")


if __name__ == "__main__":
    main()
