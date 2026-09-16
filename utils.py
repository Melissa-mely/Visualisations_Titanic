import pandas as pd
import streamlit as st


@st.cache_data
def load_data() -> pd.DataFrame:
    """Charge titanic.csv et ajoute les colonnes dérivées utilisées par plusieurs visualisations."""
    df = pd.read_csv("titanic.csv")

    bins = [0, 12, 18, 35, 60, 100]
    labels = ["Enfant (0-12)", "Ado (13-18)", "Adulte (19-35)", "Senior (36-60)", "Senior+ (60+)"]
    df["tranche_age"] = pd.cut(df["age"], bins=bins, labels=labels)

    df["famille_size"] = df["sibsp"] + df["parch"] + 1

    def statut(n):
        if n == 1:
            return "Seul"
        elif n <= 4:
            return "Petite famille"
        else:
            return "Grande famille"

    df["statut_famille"] = df["famille_size"].apply(statut)

    return df
