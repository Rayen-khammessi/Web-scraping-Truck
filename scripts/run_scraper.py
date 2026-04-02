from src.scraper import ExampleScraper


if __name__ == "__main__":
    scraper = ExampleScraper()
    html = scraper.fetch()
    title = scraper.parse_title(html)
    saved_to = scraper.save_raw_html(html)

    print(f"Title: {title}")
    print(f"Saved raw HTML to: {saved_to}")
