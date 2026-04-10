# Web Scraping TRUCK

Projet data simple, lisible et bien organise pour recuperer des annonces de camions depuis TruckScout24, les nettoyer, puis les visualiser dans un dashboard interactif.

## Demarrage rapide

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r truck_project/requirements.txt
python3 truck_project/scripts/scrape_trucks.py --pages 10 --pause 0
python3 truck_project/scripts/clean_trucks.py
streamlit run truck_project/scripts/dashboard.py
```

Le scraper s'arrete automatiquement quand il n'y a plus de pages disponibles.
