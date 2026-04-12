from __future__ import annotations
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# Chemin vers les données
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "truck_data_clean.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    """Charge les données nettoyées"""
    if not DATA_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(DATA_PATH)


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Applique les filtres sélectionnés dans la sidebar"""
    manufacturers = sorted(df["manufacturer"].dropna().unique())
    years = sorted(df["year"].dropna().unique())
    fuels = sorted(df["fuel_type"].dropna().unique())

    st.sidebar.header("Filtres")

    selected_manufacturers = st.sidebar.multiselect(
        "Marque", manufacturers, default=manufacturers
    )
    selected_years = st.sidebar.multiselect(
        "Année", years, default=years
    )
    selected_fuels = st.sidebar.multiselect(
        "Carburant", fuels, default=fuels
    )

    return df[
        df["manufacturer"].isin(selected_manufacturers)
        & df["year"].isin(selected_years)
        & df["fuel_type"].isin(selected_fuels)
    ].copy()


def display_metrics(df: pd.DataFrame) -> None:
    """Affiche les KPI principaux"""
    total_ads = len(df)
    avg_price = df["price"].mean() if total_ads else 0
    avg_mileage = df["mileage"].mean() if total_ads else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Nombre d'annonces", total_ads)
    col2.metric("Prix moyen", f"{avg_price:,.0f} €")
    col3.metric("Kilométrage moyen", f"{avg_mileage:,.0f} km")


def display_charts(df: pd.DataFrame) -> None:
    """Affiche les visualisations"""
    col1, col2 = st.columns(2)

    col1.plotly_chart(
        px.histogram(df, x="manufacturer", title="Répartition par marque"),
        use_container_width=True,
    )

    col2.plotly_chart(
        px.histogram(df, x="year", title="Répartition par année"),
        use_container_width=True,
    )

    col3, col4 = st.columns(2)

    col3.plotly_chart(
        px.box(df, x="manufacturer", y="price", title="Prix par marque"),
        use_container_width=True,
    )

    col4.plotly_chart(
        px.scatter(
            df,
            x="year",
            y="price",
            color="manufacturer",
            title="Année vs Prix",
        ),
        use_container_width=True,
    )


def main() -> None:
    st.set_page_config(page_title="Truck Dashboard", layout="wide")
    st.title("Dashboard des annonces de camions")

    df = load_data()

    if df.empty:
        st.warning("Données introuvables. Lancez le pipeline de scraping/nettoyage.")
        return

    filtered_df = apply_filters(df)

    display_metrics(filtered_df)
    display_charts(filtered_df)

    st.subheader("Données filtrées")
    st.dataframe(filtered_df, use_container_width=True)


if __name__ == "__main__":
    main()
