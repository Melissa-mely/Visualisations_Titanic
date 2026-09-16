"""
Question 5 — L'effet famille
Taux de survie par statut_famille (colonne déjà créée dans utils.load_data). Voyager seul
était-il un désavantage ?
Message : "Voyager en petite famille offrait les meilleures chances de survie — mieux que seul
ou en grande famille."

TODO (responsable de cette visualisation) :
- Affiner les 3 KPIs pour qu'ils soient actionables (pas juste descriptifs)
- Remplacer le graphique par la version interactive définitive (plotly/altair)
"""

import plotly.express as px
import streamlit as st

ORDRE = ["Seul", "Petite famille", "Grande famille"]


def render(df):
    st.subheader("L'effet famille : voyager seul était-il un désavantage ?")

    taux = df.groupby("statut_famille")["survived"].mean().reindex(ORDRE) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Taux survie seul", f"{taux.get('Seul', 0):.1f} %")
    col2.metric("Taux survie petite famille", f"{taux.get('Petite famille', 0):.1f} %")
    col3.metric("Taux survie grande famille", f"{taux.get('Grande famille', 0):.1f} %")

    data = taux.reset_index()
    data.columns = ["statut_famille", "taux_survie"]

    fig = px.bar(
        data, x="statut_famille", y="taux_survie", color="statut_famille",
        category_orders={"statut_famille": ORDRE},
        color_discrete_map={"Seul": "#595959", "Petite famille": "#2ca02c", "Grande famille": "#595959"},
        title="Voyager en grande famille était le pire scénario possible",
        labels={"taux_survie": "Taux de survie (%)"},
    )
    st.plotly_chart(fig, width="stretch")
