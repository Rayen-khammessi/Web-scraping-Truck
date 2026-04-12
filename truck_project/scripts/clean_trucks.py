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
