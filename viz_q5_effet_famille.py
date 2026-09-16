"""
Question 5 — L'effet famille
Taux de survie par statut_famille (colonne déjà créée dans utils.load_data). Voyager seul
était-il un désavantage ?
Message : "Voyager en petite famille offrait les meilleures chances de survie — mieux que seul
ou en grande famille."
"""

import pandas as pd
import plotly.express as px
import streamlit as st

ORDRE = ["Seul", "Petite famille", "Grande famille"]
COULEURS = {"Seul": "#595959", "Petite famille": "#2ca02c", "Grande famille": "#8c8c8c"}


PORTS = {"Southampton": "Southampton", "Cherbourg": "Cherbourg", "Queenstown": "Queenstown"}


def _reset_filtres():
    for cle in ("q5_classes", "q5_sexe", "q5_age", "q5_fare", "q5_ports"):
        st.session_state.pop(cle, None)


def render(df):
    st.subheader("L'effet famille : voyager seul était-il un désavantage ?")
    st.caption("Filtrez la population pour voir si l'effet famille se confirme partout.")

    fare_max = float(df["fare"].max())

    with st.container(border=True):
        col_f1, col_f2, col_f3 = st.columns(3)
        classes = col_f1.multiselect(
            "Classe(s)", options=[1, 2, 3], default=[1, 2, 3],
            format_func=lambda c: {1: "1ère", 2: "2ème", 3: "3ème"}[c], key="q5_classes",
        )
        sexes = col_f2.multiselect(
            "Sexe", options=["female", "male"], default=["female", "male"],
            format_func=lambda s: "Femme" if s == "female" else "Homme", key="q5_sexe",
        )
        ports = col_f3.multiselect(
            "Port d'embarquement", options=list(PORTS), default=list(PORTS), key="q5_ports",
        )

        col_f4, col_f5 = st.columns(2)
        age_min, age_max = col_f4.slider(
            "Tranche d'âge", min_value=0, max_value=80, value=(0, 80), key="q5_age",
        )
        tarif_min, tarif_max = col_f5.slider(
            "Tarif payé (£)", min_value=0.0, max_value=fare_max, value=(0.0, fare_max), key="q5_fare",
        )

        st.button("Réinitialiser les filtres", on_click=_reset_filtres, key="q5_reset")

    mask_age = df["age"].isna() | df["age"].between(age_min, age_max)
    mask_fare = df["fare"].between(tarif_min, tarif_max)
    mask_port = df["embark_town"].isin(ports)
    filtre = df[
        df["pclass"].isin(classes) & df["sex"].isin(sexes) & mask_age & mask_fare & mask_port
    ]

    part = len(filtre) / len(df) * 100 if len(df) else 0
    st.caption(f"{len(filtre)} passagers sur {len(df)} correspondent à ces filtres ({part:.0f} %).")
    st.progress(min(part / 100, 1.0))

    if filtre.empty:
        st.warning("Aucun passager ne correspond à ce filtre.")
        return

    taux_global = filtre["survived"].mean() * 100
    taux = filtre.groupby("statut_famille")["survived"].mean() * 100
    effectifs = filtre["statut_famille"].value_counts()

    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Seul", f"{taux.get('Seul', 0):.1f} %",
        delta=f"{taux.get('Seul', 0) - taux_global:+.1f} pts vs moyenne",
    )
    col2.metric(
        "Petite famille", f"{taux.get('Petite famille', 0):.1f} %",
        delta=f"{taux.get('Petite famille', 0) - taux_global:+.1f} pts vs moyenne",
    )
    col3.metric(
        "Grande famille", f"{taux.get('Grande famille', 0):.1f} %",
        delta=f"{taux.get('Grande famille', 0) - taux_global:+.1f} pts vs moyenne",
    )
    st.caption(f"Moyenne de survie sur la sélection : {taux_global:.1f} %.")

    vue = st.radio(
        "Affiner l'analyse :",
        ["Vue globale", "Détail par sexe", "Détail par classe"],
        horizontal=True, key="q5_vue",
    )

    col_chart, col_pie = st.columns([2, 1])

    with col_chart:
        if vue == "Vue globale":
            data = taux.reset_index()
            data.columns = ["statut_famille", "taux_survie"]
            fig = px.bar(
                data, x="statut_famille", y="taux_survie", color="statut_famille",
                category_orders={"statut_famille": ORDRE}, color_discrete_map=COULEURS,
                title="Voyager en grande famille était le pire scénario possible",
                labels={"taux_survie": "Taux de survie (%)", "statut_famille": "Statut familial"},
            )
        elif vue == "Détail par sexe":
            data = filtre.groupby(["statut_famille", "sex"])["survived"].mean().mul(100).reset_index()
            data.columns = ["statut_famille", "sexe", "taux_survie"]
            fig = px.bar(
                data, x="statut_famille", y="taux_survie", color="sexe", barmode="group",
                category_orders={"statut_famille": ORDRE},
                title="L'effet famille reste vrai pour les deux sexes",
                labels={"taux_survie": "Taux de survie (%)", "statut_famille": "Statut familial", "sexe": "Sexe"},
            )
        else:
            data = filtre.groupby(["statut_famille", "pclass"])["survived"].mean().mul(100).reset_index()
            data.columns = ["statut_famille", "pclass", "taux_survie"]
            data["pclass"] = data["pclass"].map({1: "1ère", 2: "2ème", 3: "3ème"})
            fig = px.bar(
                data, x="statut_famille", y="taux_survie", color="pclass", barmode="group",
                category_orders={"statut_famille": ORDRE},
                title="L'effet famille varie selon la classe",
                labels={"taux_survie": "Taux de survie (%)", "statut_famille": "Statut familial", "pclass": "Classe"},
            )
        st.plotly_chart(fig, width="stretch")

    with col_pie:
        pie_data = effectifs.reindex(ORDRE).fillna(0).reset_index()
        pie_data.columns = ["statut_famille", "effectif"]
        fig_pie = px.pie(
            pie_data, names="statut_famille", values="effectif",
            title="Répartition des passagers", color="statut_famille",
            color_discrete_map=COULEURS,
        )
        fig_pie.update_layout(showlegend=False)
        st.plotly_chart(fig_pie, width="stretch")

    with st.expander("Voir le détail chiffré"):
        table = pd.DataFrame({
            "Taux de survie (%)": taux.reindex(ORDRE).fillna(0).round(1),
            "Effectif": effectifs.reindex(ORDRE).fillna(0).astype(int),
        })
        st.dataframe(table, width="stretch")
