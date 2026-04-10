# Truck Project

Projet data simple et bien structure pour recuperer des annonces de camions depuis TruckScout24, nettoyer les donnees, puis les visualiser dans un dashboard interactif.

## Structure

```text
truck_project/
├── data/
│   ├── truck_data_raw.csv
│   └── truck_data_clean.csv
├── scripts/
│   ├── scrape_trucks.py
│   ├── clean_trucks.py
│   └── dashboard.py
├── requirements.txt
└── README.md
```

## Donnees recuperees

Le scraper essaie d'extraire les champs suivants quand ils sont disponibles dans les cartes d'annonces du site :

- `title`
- `price`
- `manufacturer`
- `model`
- `year`
- `mileage`
- `power`
- `fuel_type`
- `gearbox`
- `axle_configuration`
- `location`
- `ad_url`

## Installation

1. Creer un environnement virtuel :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Installer les dependances :

```bash
pip install -r truck_project/requirements.txt
```

## Execution

1. Lancer le scraping :

```bash
python3 truck_project/scripts/scrape_trucks.py --pages 10 --pause 0
```

Le fichier brut est enregistre dans `truck_project/data/truck_data_raw.csv`.

2. Lancer le nettoyage :

```bash
python3 truck_project/scripts/clean_trucks.py
```

Le fichier nettoye est enregistre dans `truck_project/data/truck_data_clean.csv`.

3. Lancer le dashboard :

```bash
streamlit run truck_project/scripts/dashboard.py
```

## Nettoyage applique

- suppression des doublons sur `ad_url`
- noms de colonnes en minuscules
- conversion du prix en numerique
- conversion du kilometrage en numerique
- conversion de l'annee en entier
- nettoyage des caracteres inutiles
- gestion simple des valeurs manquantes avec `Unknown`

## Dashboard

Le dashboard affiche :

- le nombre total d'annonces
- le prix moyen
- le kilometrage moyen
- la repartition par marque
- la repartition par annee
- un filtre par marque
- un filtre par annee
- un filtre par type de carburant
- un graphique du prix par marque
- un graphique annee vs prix

## Remarques

- Le site TruckScout24 renvoie deja les cartes d'annonces dans le HTML, donc `requests + BeautifulSoup` suffisent pour cette premiere version.
- Certains champs peuvent manquer selon les annonces. Le scraper les laisse vides puis le script de nettoyage les harmonise.
- Si la structure HTML du site evolue, il faudra ajuster les selecteurs CSS dans `scrape_trucks.py`.
- Le scraper s'arrete automatiquement a la derniere page disponible si tu demandes plus de pages que le site n'en propose.
