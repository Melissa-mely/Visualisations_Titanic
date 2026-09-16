"""
Question 3 — Le facteur classe sociale
Taux de survie et tarif médian par classe (pclass). Lien entre richesse et survie ?
Message : "Les passagers de 1ère classe ont survécu presque 3 fois plus que ceux de 3ème classe."

TODO (responsable de cette visualisation) :
- Affiner les 3 KPIs pour qu'ils soient actionables (pas juste descriptifs)
- Remplacer le graphique par la version interactive définitive (plotly/altair)
"""

import plotly.express as px
import streamlit as st


def render(df):
    st.subheader("Le facteur classe sociale : la richesse a-t-elle acheté des chances de survie ?")

    taux = df.groupby("pclass")["survived"].mean() * 100
    tarif_median = df.groupby("pclass")["fare"].median()

    col1, col2, col3 = st.columns(3)
    col1.metric("Taux survie 1ère classe", f"{taux.get(1, 0):.1f} %")
    col2.metric("Taux survie 3ème classe", f"{taux.get(3, 0):.1f} %")
    col3.metric("Tarif médian 1ère classe", f"{tarif_median.get(1, 0):.0f} £")

    data = taux.reset_index()
    data.columns = ["classe", "taux_survie"]
    data["classe"] = data["classe"].map({1: "1ère", 2: "2ème", 3: "3ème"})

    fig = px.bar(
        data, x="classe", y="taux_survie", color="classe",
        color_discrete_map={"1ère": "#2ca02c", "2ème": "#595959", "3ème": "#595959"},
        title="Les plus riches ont été une priorité",
        labels={"taux_survie": "Taux de survie (%)"},
    )
    st.plotly_chart(fig, width="stretch")
