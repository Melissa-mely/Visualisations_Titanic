"""
Question 4 — Le facteur âge
Taux de survie par tranche_age (colonne déjà créée dans utils.load_data). Les enfants
étaient-ils vraiment prioritaires ?
Message : "Les enfants ont bénéficié d'un net traitement prioritaire face aux autres âges."
"""

import re
import plotly.express as px
import streamlit as st


def _ordre_naturel(tranches):
    """Trie les tranches d'âge par leur borne inférieure numérique,
    plutôt que de dépendre de libellés codés en dur (évite les
    décalages si la colonne tranche_age change de nom/format)."""
    def borne_inf(label):
        match = re.search(r"\d+", str(label))
        return int(match.group()) if match else 9999
    return sorted(tranches, key=borne_inf)


def _label_enfant(tranches):
    """Détecte automatiquement le libellé correspondant aux enfants
    (contient 'enfant', insensible à la casse)."""
    for t in tranches:
        if "enfant" in str(t).lower():
            return t
    return None


def render(df):
    st.subheader("Le facteur âge : les enfants ont-ils été prioritaires ?")

    # --- FILTRES ---
    classes_disponibles = sorted(df["pclass"].unique())
    sexes_disponibles = df["sex"].unique().tolist()

    col_f1, col_f2 = st.columns(2)
    classes_sel = col_f1.multiselect(
        "Classe", classes_disponibles, default=classes_disponibles, key="q4_classe"
    )
    sexes_sel = col_f2.multiselect(
        "Sexe", sexes_disponibles, default=sexes_disponibles, key="q4_sexe"
    )

    df_filtre = df[df["pclass"].isin(classes_sel) & df["sex"].isin(sexes_sel)]

    if df_filtre.empty:
        st.warning("Aucune donnée pour ce filtre.")
        return

    # --- CALCUL DU TAUX PAR TRANCHE ---
    taux = df_filtre.groupby("tranche_age", observed=True)["survived"].mean() * 100
    taux.index = taux.index.astype(str)  # sécurise la comparaison si colonne catégorielle

    if taux.empty:
        st.warning("Pas de données de survie par tranche d'âge pour ce filtre.")
        return

    tranches_presentes = _ordre_naturel(taux.index.tolist())
    label_enfant = _label_enfant(tranches_presentes)

    # --- KPIs ---
    taux_enfants = taux.get(label_enfant, 0) if label_enfant else 0
    taux_autres = taux.drop(label_enfant, errors="ignore") if label_enfant else taux
    tranche_min = taux_autres.idxmin() if not taux_autres.empty else None
    taux_min = taux_autres.min() if not taux_autres.empty else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Taux survie enfants", f"{taux_enfants:.1f} %" if label_enfant else "N/A")
    col2.metric(f"Taux le plus bas ({tranche_min or '—'})", f"{taux_min:.1f} %")
    if taux_min > 0 and label_enfant:
        col3.metric("Écart enfants vs tranche la moins favorisée", f"×{(taux_enfants / taux_min):.1f}")
    else:
        col3.metric("Écart", "—")

    # --- GRAPHIQUE ---
    data = taux.reindex(tranches_presentes).reset_index()
    data.columns = ["tranche_age", "taux_survie"]

    couleurs = {t: ("#2ca02c" if t == label_enfant else "#595959") for t in tranches_presentes}

    fig = px.bar(
        data, x="tranche_age", y="taux_survie", color="tranche_age",
        color_discrete_map=couleurs,
        category_orders={"tranche_age": tranches_presentes},
        title="Les enfants ont bénéficié d'un traitement prioritaire",
        labels={"taux_survie": "Taux de survie (%)", "tranche_age": "Tranche d'âge"},
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, width="stretch")