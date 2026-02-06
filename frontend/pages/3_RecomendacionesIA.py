import streamlit as st
from services.ia import get_recommendations
from ui.background import set_background

set_background("assets/comicsfondo.png")

if "token" not in st.session_state:
    st.error("Debes iniciar sesión para acceder.")
    st.stop()

st.title("🤖 Recomendaciones IA")

# 👇 TEXTO QUE USA LA IA
user_profile = st.text_area(
    "Describe qué mangas te gustan",
    placeholder="Ej: Me gustan mangas oscuros tipo Berserk, acción, demonios..."
)

top_k = st.slider("Cantidad de recomendaciones", 1, 10, 5)

if st.button("Obtener recomendaciones"):
    if not user_profile.strip():
        st.warning("Escribe qué te gusta para recomendarte algo")
        st.stop()

    with st.spinner("Generando recomendaciones..."):
        data = get_recommendations(user_profile, top_k)

    recs = data["recommendations"]

    for r in recs:
        st.subheader(r["title"])
        st.write(r["reason"])
