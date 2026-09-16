"""
Question 2 — Le facteur genre
Taux de survie par genre.
"""

import plotly.express as px
import streamlit as st


def render(df):
    st.subheader("Le facteur genre : les femmes ont-elles été prioritaires ?")

    # Filtres
    col_filtre1, col_filtre2 = st.columns(2)

    with col_filtre1:
        tranche_age = st.selectbox(
            "Tranche d'âge",
            ["Toutes"] + df["tranche_age"].dropna().unique().tolist(),
            key="q2_age",
        )

    with col_filtre2:
        classe = st.selectbox(
            "Classe",
            ["Toutes"] + sorted(df["pclass"].dropna().unique().tolist()),
            key="q2_classe",
        )

    # Application des filtres
    df_filtre = df.copy()

    if tranche_age != "Toutes":
        df_filtre = df_filtre[df_filtre["tranche_age"] == tranche_age]

    if classe != "Toutes":
        df_filtre = df_filtre[df_filtre["pclass"] == classe]

    st.write(
        f"**{len(df_filtre)} passagers correspondent aux filtres sélectionnés.**"
    )

    # Taux de survie par sexe
    taux = df_filtre.groupby("sex")["survived"].mean() * 100

    taux_femmes = taux.get("female", 0)
    taux_hommes = taux.get("male", 0)

    ecart = (
        taux_femmes / taux_hommes
        if taux_hommes > 0
        else 0
    )

    # KPI
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Taux de survie des femmes",
        f"{taux_femmes:.1f} %",
    )

    col2.metric(
        "Taux de survie des hommes",
        f"{taux_hommes:.1f} %",
    )

    col3.metric(
        "Rapport femmes / hommes",
        f"x{ecart:.1f}",
    )

    # Préparation du graphique
    data = taux.reset_index()
    data.columns = ["sexe", "taux_survie"]

    data["sexe"] = data["sexe"].map(
        {
            "female": "Femmes",
            "male": "Hommes",
        }
    )

    # Graphique interactif
    fig = px.bar(
        data,
        x="sexe",
        y="taux_survie",
        color="sexe",
        color_discrete_map={
            "Femmes": "#E74C3C",
            "Hommes": "#3498DB",
        },
        title=f"Taux de survie selon le genre — {ecart:.1f} fois plus élevé chez les femmes",
        labels={
            "sexe": "Genre",
            "taux_survie": "Taux de survie (%)",
        },
        text="taux_survie",
    )

    fig.update_traces(
        texttemplate="%{text:.1f} %",
        hovertemplate="<b>%{x}</b><br>Taux de survie : %{y:.1f} %<extra></extra>",
    )

    fig.update_yaxes(
        range=[0, 100],
        ticksuffix=" %",
    )

    st.plotly_chart(fig, width="stretch")