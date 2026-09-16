"""
Question 1 — État des lieux
Combien de passagers ont survécu ? Quel pourcentage cela représente-t-il ?
Message : "Seulement 38 % des passagers ont survécu au naufrage."

TODO (responsable de cette visualisation) :
- Affiner les 3 KPIs pour qu'ils soient actionables (pas juste descriptifs)
- Remplacer le graphique par la version interactive définitive (plotly/altair)
"""

import plotly.express as px
import streamlit as st


def render(df):
    st.subheader("État des lieux : combien de passagers ont survécu ?")

    total = len(df)
    survivants = int(df["survived"].sum())
    taux = survivants / total * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Passagers total", total)
    col2.metric("Survivants", survivants)
    col3.metric("Taux de survie", f"{taux:.1f} %")

    counts = df["survived"].map({0: "Décédé", 1: "Survivant"}).value_counts().reset_index()
    counts.columns = ["statut", "nombre"]

    fig = px.bar(
        counts, x="statut", y="nombre", color="statut",
        color_discrete_map={"Décédé": "#595959", "Survivant": "#2ca02c"},
        title="Seulement 38 % des passagers ont survécu au naufrage",
    )
    st.plotly_chart(fig, width="stretch")
