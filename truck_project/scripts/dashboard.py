from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "truck_data_clean.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(DATA_PATH)


def main() -> None:
    st.set_page_config(page_title="Truck Dashboard", layout="wide")
    st.title("Dashboard des annonces de camions")

    df = load_data()
    if df.empty:
        st.warning("Le fichier nettoye est vide ou introuvable. Lance d'abord le scraping puis le nettoyage.")
        return

    manufacturers = sorted(df["manufacturer"].dropna().unique().tolist())
    years = sorted([int(year) for year in df["year"].dropna().unique().tolist()])
    fuels = sorted(df["fuel_type"].dropna().unique().tolist())

    st.sidebar.header("Filtres")
    selected_manufacturers = st.sidebar.multiselect("Marque", manufacturers, default=manufacturers)
    selected_years = st.sidebar.multiselect("Annee", years, default=years)
    selected_fuels = st.sidebar.multiselect("Carburant", fuels, default=fuels)

    filtered_df = df[
        df["manufacturer"].isin(selected_manufacturers)
        & df["year"].isin(selected_years)
        & df["fuel_type"].isin(selected_fuels)
    ].copy()

    total_ads = int(len(filtered_df))
    avg_price = float(filtered_df["price"].dropna().mean()) if total_ads else 0.0
    avg_mileage = float(filtered_df["mileage"].dropna().mean()) if total_ads else 0.0

    metric_1, metric_2, metric_3 = st.columns(3)
    metric_1.metric("Nombre total d'annonces", f"{total_ads}")
    metric_2.metric("Prix moyen", f"{avg_price:,.0f} EUR")
    metric_3.metric("Kilometrage moyen", f"{avg_mileage:,.0f} km")

    brand_count_fig = px.histogram(
        filtered_df,
        x="manufacturer",
        title="Repartition par marque",
        color="manufacturer",
    )
    year_count_fig = px.histogram(
        filtered_df,
        x="year",
        title="Repartition par annee",
        nbins=20,
    )
    price_by_brand_fig = px.box(
        filtered_df,
        x="manufacturer",
        y="price",
        title="Prix par marque",
        points="outliers",
    )
    year_vs_price_fig = px.scatter(
        filtered_df,
        x="year",
        y="price",
        color="manufacturer",
        hover_data=["title", "mileage", "fuel_type", "location"],
        title="Annee vs prix",
    )

    col_1, col_2 = st.columns(2)
    col_1.plotly_chart(brand_count_fig, use_container_width=True)
    col_2.plotly_chart(year_count_fig, use_container_width=True)

    col_3, col_4 = st.columns(2)
    col_3.plotly_chart(price_by_brand_fig, use_container_width=True)
    col_4.plotly_chart(year_vs_price_fig, use_container_width=True)

    st.subheader("Donnees filtrees")
    st.dataframe(filtered_df, use_container_width=True)


if __name__ == "__main__":
    main()
