"""
Question 4 — Le facteur âge
Taux de survie par tranche_age (colonne déjà créée dans utils.load_data). Les enfants
étaient-ils vraiment prioritaires ?
Message : "Les enfants ont bénéficié d'un net traitement prioritaire face aux autres âges."

TODO (responsable de cette visualisation) :
- Affiner les 3 KPIs pour qu'ils soient actionables (pas juste descriptifs)
- Remplacer le graphique par la version interactive définitive (plotly/altair)
"""

import plotly.express as px
import streamlit as st


def render(df):
    st.subheader("Le facteur âge : les enfants ont-ils été prioritaires ?")

    taux = df.groupby("tranche_age", observed=True)["survived"].mean() * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Taux survie enfants", f"{taux.get('Enfant (0-12)', 0):.1f} %")
    col2.metric("Taux survie adultes", f"{taux.get('Adulte (19-35)', 0):.1f} %")
    col3.metric("Nombre de tranches d'âge", df["tranche_age"].nunique())

    data = taux.reset_index()
    data.columns = ["tranche_age", "taux_survie"]

    fig = px.bar(
        data, x="tranche_age", y="taux_survie", color="tranche_age",
        title="Les enfants ont bénéficié d'un traitement prioritaire",
        labels={"taux_survie": "Taux de survie (%)"},
    )
    st.plotly_chart(fig, width="stretch")
