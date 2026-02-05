import streamlit as st
from services.ia import get_recommendations


from ui.background import set_background
set_background("assets/comicsfondo.png")

if "token" not in st.session_state:
    st.error("Debes iniciar sesión para acceder.")
    st.stop()

st.title("🤖 Recomendaciones IA")

user_id = st.number_input("Tu user_id", min_value=1)

if st.button("Obtener recomendaciones"):
    recs = get_recommendations(user_id)
    for r in recs:
        st.subheader(r["title"])
        st.write(r["description"])
