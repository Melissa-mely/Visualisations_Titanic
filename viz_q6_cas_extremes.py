"""
Question 6 — Les cas extrêmes
Comparaison de deux profils opposés : femmes de 1ère classe vs hommes de 3ème classe.
Message : "L'écart de survie entre femmes de 1ère classe et hommes de 3ème classe est
vertigineux : sexe et classe se cumulent."

TODO (responsable de cette visualisation) :
- Affiner les 3 KPIs pour qu'ils soient actionables (pas juste descriptifs)
- Remplacer le graphique par la version interactive définitive (plotly/altair)
"""

import plotly.express as px
import streamlit as st


def render(df):
    st.subheader("Les cas extrêmes : sexe et classe se cumulent-ils ?")

    profil_a = df[(df["sex"] == "female") & (df["pclass"] == 1)]
    profil_b = df[(df["sex"] == "male") & (df["pclass"] == 3)]

    taux_a = profil_a["survived"].mean() * 100
    taux_b = profil_b["survived"].mean() * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Taux survie femmes 1ère classe", f"{taux_a:.1f} %")
    col2.metric("Taux survie hommes 3ème classe", f"{taux_b:.1f} %")
    ecart = taux_a - taux_b
    col3.metric("Écart de survie", f"{ecart:.1f} pts")

    data = {
        "profil": ["Femmes 1ère classe", "Hommes 3ème classe"],
        "taux_survie": [taux_a, taux_b],
    }

    fig = px.bar(
        data, x="profil", y="taux_survie", color="profil",
        color_discrete_map={"Femmes 1ère classe": "#2ca02c", "Hommes 3ème classe": "#595959"},
        title="Sexe et classe se cumulent : un écart de survie vertigineux",
        labels={"taux_survie": "Taux de survie (%)"},
    )
    st.plotly_chart(fig, width="stretch")
