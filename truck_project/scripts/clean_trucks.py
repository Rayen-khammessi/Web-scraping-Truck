from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_PATH = BASE_DIR / "data" / "truck_data_raw.csv"
CLEAN_PATH = BASE_DIR / "data" / "truck_data_clean.csv"


def to_number(value: object) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None

    text = str(value).strip()
    if not text:
        return None

    text = text.replace("\xa0", " ")
    text = re.sub(r"[^\d,.\-]", "", text)
    text = text.replace(".", "")
    text = text.replace(",", "")

    if not text or text == "-":
        return None

    try:
        return float(text)
    except ValueError:
        return None


def to_year(value: object) -> int | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None

    match = re.search(r"(19|20)\d{2}", str(value))
    if match:
        return int(match.group())
    return None


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()
    df.columns = [column.strip().lower() for column in df.columns]

    for column in df.columns:
        if df[column].dtype == object:
            df[column] = df[column].fillna("").astype(str).str.strip()

    df = df.drop_duplicates(subset=["ad_url"])
    df["price"] = df["price"].apply(to_number)
    df["mileage"] = df["mileage"].apply(to_number)
    df["year"] = df["year"].apply(to_year)

    if "power" in df.columns:
        df["power"] = df["power"].str.extract(r"(\d[\d,\.]*)", expand=False)
        df["power"] = df["power"].apply(to_number)

    string_columns = [
        "title",
        "manufacturer",
        "model",
        "fuel_type",
        "gearbox",
        "axle_configuration",
        "location",
        "ad_url",
    ]
    for column in string_columns:
        if column in df.columns:
            df[column] = df[column].replace("", "Unknown")

    return df


def main() -> None:
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Fichier introuvable: {RAW_PATH}")

    df = pd.read_csv(RAW_PATH)
    clean_df = clean_dataframe(df)
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(CLEAN_PATH, index=False)
    print(f"{len(clean_df)} lignes nettoyees sauvegardees dans {CLEAN_PATH}")


if __name__ == "__main__":
    main()
