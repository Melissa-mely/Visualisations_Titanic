"""
Question 2 — Le facteur genre
Taux de survie par genre. La devise "women and children first" s'applique-t-elle ?
Message : "Les femmes ont survécu presque 4 fois plus que les hommes : la règle a été respectée."

TODO (responsable de cette visualisation) :
- Affiner les 3 KPIs pour qu'ils soient actionables (pas juste descriptifs)
- Remplacer le graphique par la version interactive définitive (plotly/altair)
"""

import plotly.express as px
import streamlit as st


def render(df):
    st.subheader("Le facteur genre : les femmes ont-elles été prioritaires ?")

    taux = df.groupby("sex")["survived"].mean() * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Taux survie femmes", f"{taux.get('female', 0):.1f} %")
    col2.metric("Taux survie hommes", f"{taux.get('male', 0):.1f} %")
    ecart = taux.get("female", 0) / taux.get("male", 1) if taux.get("male", 0) else 0
    col3.metric("Écart femmes / hommes", f"x{ecart:.1f}")

    data = taux.reset_index()
    data.columns = ["sexe", "taux_survie"]

    fig = px.bar(
        data, x="sexe", y="taux_survie", color="sexe",
        color_discrete_map={"female": "#2ca02c", "male": "#595959"},
        title="Les femmes ont survécu presque 4 fois plus que les hommes",
        labels={"taux_survie": "Taux de survie (%)"},
    )
    st.plotly_chart(fig, width="stretch")
