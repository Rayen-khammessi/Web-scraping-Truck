from src.scraper import ExampleScraper


def test_parse_title_extracts_page_title() -> None:
    scraper = ExampleScraper()
    html = "<html><head><title>Example Domain</title></head><body></body></html>"

    assert scraper.parse_title(html) == "Example Domain"
