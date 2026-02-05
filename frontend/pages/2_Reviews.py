import streamlit as st
from services.reviews import list_reviews, create_review


from ui.background import set_background
set_background("assets/comicsfondo.png")

if "user" not in st.session_state:
    st.error("Debes iniciar sesión para acceder.")
    st.stop()


st.title("📝 Reseñas")

comic_id = st.number_input("ID del cómic", min_value=1)

if st.button("Ver reseñas"):
    reviews = list_reviews(comic_id)
    for r in reviews:
        st.write(f"⭐ {r['valoracion']} - {r['texto_resenya']}")

st.subheader("Añadir reseña")
user_id = st.number_input("Tu user_id", min_value=1)
texto = st.text_area("Texto")
valoracion = st.slider("Valoración", 1, 5)
nombre_tabla = st.selectbox("Tabla", ["manga", "marvel"])

if st.button("Enviar reseña"):
    create_review(user_id, comic_id, texto, valoracion, nombre_tabla)
    st.success("Reseña añadida")
