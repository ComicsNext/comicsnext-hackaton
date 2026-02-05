import streamlit as st
from services.comics import list_comics, get_comic

from ui.background import set_background
set_background("assets/comicsfondo.png")


if "user" not in st.session_state:
    st.error("Debes iniciar sesión para acceder.")
    st.stop()



st.title("📘 Lista de Cómics")

genre = st.text_input("Género")
author = st.text_input("Autor")
publisher = st.text_input("Editorial")
year = st.number_input("Año", min_value=1900, max_value=2100, step=1)

if st.button("Buscar"):
    comics = list_comics(genre, author, publisher, year)
    for c in comics:
        st.subheader(c["title"])
        st.write(c["description"])
        st.write(f"ID: {c['id']}")
