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
