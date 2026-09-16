import streamlit as st

from utils import load_data
import viz_q1_etat_des_lieux as q1
import viz_q2_facteur_genre as q2
import viz_q3_facteur_classe as q3
import viz_q4_facteur_age as q4
import viz_q5_effet_famille as q5
import viz_q6_cas_extremes as q6

st.set_page_config(page_title="Titanic — Dashboard", page_icon="🚢", layout="wide")
st.title("🚢 Titanic — Profil des survivants")

df = load_data()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1. État des lieux",
    "2. Facteur genre",
    "3. Facteur classe",
    "4. Facteur âge",
    "5. Effet famille",
    "6. Cas extrêmes",
])

with tab1:
    q1.render(df)
with tab2:
    q2.render(df)
with tab3:
    q3.render(df)
with tab4:
    q4.render(df)
with tab5:
    q5.render(df)
with tab6:
    q6.render(df)
