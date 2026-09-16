"""
Question 6 — Les cas extrêmes
Comparaison de profils opposés pour isoler l'effet du sexe, de la classe, et des deux
combinés.
Message : "L'écart de survie entre femmes de 1ère classe et hommes de 3ème classe est
vertigineux : sexe et classe se cumulent."
"""

import pandas as pd
import plotly.express as px
import streamlit as st

PROFILS = {
    "Cas extrêmes (sexe + classe cumulés)": (
        ("Femmes 1ère classe", "female", 1),
        ("Hommes 3ème classe", "male", 3),
    ),
    "Effet du sexe seul (à classe égale : 3ème)": (
        ("Femmes 3ème classe", "female", 3),
        ("Hommes 3ème classe", "male", 3),
    ),
    "Effet de la classe seule (à sexe égal : hommes)": (
        ("Hommes 1ère classe", "male", 1),
        ("Hommes 3ème classe", "male", 3),
    ),
}

SEXE_LABELS = {"female": "Femmes", "male": "Hommes"}
CLASSE_LABELS = {1: "1ère classe", 2: "2ème classe", 3: "3ème classe"}


def _label(sex, pclass):
    return f"{SEXE_LABELS[sex]} {CLASSE_LABELS[pclass]}"


def _profil_stats(subset):
    return {
        "taux": subset["survived"].mean() * 100 if len(subset) else 0,
        "age_median": subset["age"].median(),
        "tarif_median": subset["fare"].median(),
        "n": len(subset),
    }


def render(df):
    st.subheader("Les cas extrêmes : sexe et classe se cumulent-ils ?")
    st.caption("Choisissez les deux profils à comparer pour isoler l'effet du sexe, de la classe, ou des deux.")

    mode = st.radio(
        "Mode de comparaison :", ["Profils prédéfinis", "Profils personnalisés"],
        horizontal=True, key="q6_mode",
    )

    if mode == "Profils prédéfinis":
        choix = st.selectbox("Comparer :", list(PROFILS.keys()), key="q6_choix")
        (label_a, sex_a, class_a), (label_b, sex_b, class_b) = PROFILS[choix]
        titre_bar = "Sexe et classe se cumulent : un écart de survie vertigineux" if "extrêmes" in choix else choix
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Profil A**")
            sex_a = st.selectbox(
                "Sexe", ["female", "male"], format_func=lambda s: SEXE_LABELS[s], key="q6_sex_a",
            )
            class_a = st.selectbox(
                "Classe", [1, 2, 3], format_func=lambda c: CLASSE_LABELS[c], key="q6_class_a",
            )
        with col_b:
            st.markdown("**Profil B**")
            sex_b = st.selectbox(
                "Sexe", ["female", "male"], index=1, format_func=lambda s: SEXE_LABELS[s], key="q6_sex_b",
            )
            class_b = st.selectbox(
                "Classe", [1, 2, 3], index=2, format_func=lambda c: CLASSE_LABELS[c], key="q6_class_b",
            )
        label_a, label_b = _label(sex_a, class_a), _label(sex_b, class_b)
        titre_bar = f"{label_a} vs {label_b}"
        if (sex_a, class_a) == (sex_b, class_b):
            st.info("Les deux profils sont identiques — choisissez deux combinaisons différentes.")

    subset_a = df[(df["sex"] == sex_a) & (df["pclass"] == class_a)]
    subset_b = df[(df["sex"] == sex_b) & (df["pclass"] == class_b)]
    stats_a = _profil_stats(subset_a)
    stats_b = _profil_stats(subset_b)

    col1, col2, col3 = st.columns(3)
    col1.metric(f"Taux survie — {label_a}", f"{stats_a['taux']:.1f} %")
    col2.metric(f"Taux survie — {label_b}", f"{stats_b['taux']:.1f} %")
    ratio = stats_a["taux"] / stats_b["taux"] if stats_b["taux"] else 0
    col3.metric("Écart de survie", f"{stats_a['taux'] - stats_b['taux']:+.1f} pts", delta=f"x{ratio:.1f}")

    col_chart, col_box = st.columns(2)

    with col_chart:
        data = {"profil": [label_a, label_b], "taux_survie": [stats_a["taux"], stats_b["taux"]]}
        fig = px.bar(
            data, x="profil", y="taux_survie", color="profil",
            color_discrete_map={label_a: "#2ca02c", label_b: "#595959"},
            title=titre_bar,
            labels={"taux_survie": "Taux de survie (%)"},
        )
        st.plotly_chart(fig, width="stretch")

    with col_box:
        combined = pd.concat([
            subset_a.assign(profil=label_a),
            subset_b.assign(profil=label_b),
        ])
        fig_box = px.box(
            combined, x="profil", y="age", color="profil",
            color_discrete_map={label_a: "#2ca02c", label_b: "#595959"},
            title="Répartition des âges par profil", points="all",
        )
        fig_box.update_layout(showlegend=False)
        st.plotly_chart(fig_box, width="stretch")

    with st.expander("Voir le détail chiffré"):
        def _format(stats):
            return [
                str(stats["n"]),
                f"{stats['age_median']:.0f} ans",
                f"{stats['tarif_median']:.0f} £",
                f"{stats['taux']:.1f} %",
            ]

        table = pd.DataFrame(
            {label_a: _format(stats_a), label_b: _format(stats_b)},
            index=["Nombre de passagers", "Âge médian", "Tarif médian", "Taux de survie"],
        )
        st.dataframe(table, width="stretch")
