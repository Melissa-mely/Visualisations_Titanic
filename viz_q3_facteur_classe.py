"""
Question 3 — Le facteur classe sociale
Taux de survie et tarif médian par classe (pclass). Lien entre richesse et survie ?
Message : "Les passagers de 1ère classe ont survécu presque 3 fois plus que ceux de 3ème classe."
"""

import plotly.express as px
import streamlit as st


def render(df):
    st.subheader("Le facteur classe sociale : la richesse a-t-elle acheté des chances de survie ?")

    noms_classe = {1: "1ère", 2: "2ème", 3: "3ème"}
    classes_disponibles = sorted(df["pclass"].unique())
    sexes_disponibles = df["sex"].unique().tolist()

    # --- FILTRES (contrôlent le graphique) ---
    col_f1, col_f2 = st.columns(2)
    classes_sel = col_f1.multiselect("Classe(s) affichée(s)", classes_disponibles, default=classes_disponibles)
    sexes_sel = col_f2.multiselect("Sexe", sexes_disponibles, default=sexes_disponibles)

    df_filtre = df[df["pclass"].isin(classes_sel) & df["sex"].isin(sexes_sel)]

    if df_filtre.empty:
        st.warning("Aucune donnée pour ce filtre.")
        return

    # --- COMPARATEUR (indépendant du filtre, pilote les KPIs) ---
    col_c1, col_c2 = st.columns(2)
    classe_a = col_c1.selectbox("Comparer :", classes_disponibles, index=0, format_func=lambda c: f"{noms_classe[c]} classe")
    classe_b = col_c2.selectbox("à :", classes_disponibles, index=len(classes_disponibles) - 1, format_func=lambda c: f"{noms_classe[c]} classe")

    taux = df_filtre.groupby("pclass")["survived"].mean() * 100

    col1, col2, col3 = st.columns(3)
    col1.metric(f"Taux survie {noms_classe[classe_a]} classe", f"{taux.get(classe_a, 0):.1f} %")
    col2.metric(f"Taux survie {noms_classe[classe_b]} classe", f"{taux.get(classe_b, 0):.1f} %")

    if classe_a != classe_b and taux.get(classe_b, 0) > 0:
        ecart = taux.get(classe_a, 0) / taux.get(classe_b, 0)
        col3.metric(f"Écart {noms_classe[classe_a]} vs {noms_classe[classe_b]}", f"×{ecart:.1f}")
    else:
        col3.metric("Écart", "—", help="Choisissez deux classes différentes")

    # --- GRAPHIQUE BARRES ---
    data = taux.reset_index()
    data.columns = ["classe", "taux_survie"]
    data["classe"] = data["classe"].map(noms_classe)

    couleurs = {noms_classe[c]: ("#2ca02c" if c == classe_a else "#595959") for c in classes_sel}

    fig = px.bar(
        data, x="classe", y="taux_survie", color="classe",
        color_discrete_map=couleurs,
        title="Les plus riches ont été une priorité",
        labels={"taux_survie": "Taux de survie (%)"},
    )
    st.plotly_chart(fig, width="stretch")