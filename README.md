# Dashboard Titanic — Streamlit

## Lancer le dashboard

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Répartition du travail

Un onglet Streamlit = une visualisation du notebook. Chaque fichier `viz_qX_*.py`
contient une fonction `render(df)` à compléter (titre + 3 KPIs + graphique interactif).
`df` est déjà enrichi des colonnes `tranche_age`, `famille_size` et `statut_famille`
(voir `utils.py`).

| Fichier | Visualisation | Responsable |
|---|---|---|
| `viz_q1_etat_des_lieux.py` | Q1 — État des lieux | |
| `viz_q2_facteur_genre.py` | Q2 — Facteur genre | |
| `viz_q3_facteur_classe.py` | Q3 — Facteur classe sociale | |
| `viz_q4_facteur_age.py` | Q4 — Facteur âge | |
| `viz_q5_effet_famille.py` | Q5 — Effet famille | |
| `viz_q6_cas_extremes.py` | Q6 — Cas extrêmes | |

## Workflow git

1. `git clone` le repo.
2. Créer une branche par personne : `git checkout -b viz-<prenom>`.
3. Ne modifier **que** les fichiers `viz_qX_*.py` dont vous êtes responsable
   (ne touchez pas à `app.py` ni au fichier des autres, pour éviter les conflits).
4. Push la branche puis ouvrir une Pull Request vers `main`.
5. Une fois toutes les PR mergées, `app.py` assemble automatiquement les 6 onglets.
