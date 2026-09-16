"""
Question 1 — État des lieux
Combien de passagers ont survécu ? Quel pourcentage cela représente-t-il ?
"""

import plotly.express as px
import streamlit as st


def render(df):
    st.subheader("État des lieux : combien de passagers ont survécu ?")

    # Filtres
    col_filtre1, col_filtre2, col_filtre3 = st.columns(3)

    with col_filtre1:
        sexe = st.selectbox(
            "Sexe",
            ["Tous", "female", "male"],
        )

    with col_filtre2:
        tranche_age = st.selectbox(
            "Tranche d'âge",
            ["Toutes"] + df["tranche_age"].dropna().unique().tolist(),
        )

    with col_filtre3:
        classe = st.selectbox(
            "Classe",
            ["Toutes"] + sorted(df["pclass"].dropna().unique().tolist()),
        )

    # Application des filtres
    df_filtre = df.copy()

    if sexe != "Tous":
        df_filtre = df_filtre[df_filtre["sex"] == sexe]

    if tranche_age != "Toutes":
        df_filtre = df_filtre[df_filtre["tranche_age"] == tranche_age]

    if classe != "Toutes":
        df_filtre = df_filtre[df_filtre["pclass"] == classe]

    st.write(f"**{len(df_filtre)} passagers correspondent aux filtres sélectionnés.**")

    # KPI
    total = len(df_filtre)
    survivants = int(df_filtre["survived"].sum())
    taux = survivants / total * 100 if total > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Passagers", total)
    col2.metric("Survivants", survivants)
    col3.metric("Taux de survie", f"{taux:.1f} %")

    # Graphique interactif
    counts = (
        df_filtre["survived"]
        .map({0: "Décédé", 1: "Survivant"})
        .value_counts()
        .reindex(["Décédé", "Survivant"], fill_value=0)
        .reset_index()
    )

    counts.columns = ["statut", "nombre"]

    fig = px.bar(
        counts,
        x="statut",
        y="nombre",
        color="statut",
        title=f"Survie des passagers sélectionnés — {taux:.1f} % de survie",
        labels={
            "statut": "Statut",
            "nombre": "Nombre de passagers",
        },
        text="nombre",
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Nombre : %{y}<extra></extra>"
    )

    st.plotly_chart(fig, width="stretch")