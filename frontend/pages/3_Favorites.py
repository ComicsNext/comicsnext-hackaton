import streamlit as st
from services.favorites import add_favorite, list_favorites


from ui.background import set_background
set_background("assets/comicsfondo.png")

if "user" not in st.session_state:
    st.error("Debes iniciar sesión para acceder.")
    st.stop()


st.title("⭐ Favoritos")

user_id = st.number_input("Tu user_id", min_value=1)

if st.button("Ver favoritos"):
    favs = list_favorites(user_id)
    for f in favs:
        st.write(f"Comic ID: {f['comic_id']}")

comic_id = st.number_input("Añadir comic_id", min_value=1)

if st.button("Añadir a favoritos"):
    add_favorite(user_id, comic_id)
    st.success("Añadido a favoritos")
