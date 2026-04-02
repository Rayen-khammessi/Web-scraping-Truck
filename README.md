# Web Scraping Workspace

A structured Python workspace for building and maintaining web scraping projects.

## Structure

- `src/`: scraping logic and shared utilities
- `scripts/`: runnable entrypoints
- `config/`: project configuration templates
- `data/raw/`: unmodified scraped data
- `data/processed/`: cleaned or transformed data
- `data/external/`: third-party input files
- `logs/`: runtime logs
- `tests/`: basic test coverage
- `notebooks/`: exploration and analysis

## Quick Start

1. Create a virtual environment:
   `python3 -m venv .venv`
2. Activate it:
   `source .venv/bin/activate`
3. Install dependencies:
   `pip install -e .`
4. Copy the environment template if needed:
   `cp .env.example .env`
5. Run the starter scraper:
   `python scripts/run_scraper.py`

## Notes

- Keep raw responses in `data/raw/`.
- Write cleaned outputs to `data/processed/`.
- Store reusable selectors, headers, or target URLs in `config/`.
- Add project-specific spiders or parsers under `src/`.
