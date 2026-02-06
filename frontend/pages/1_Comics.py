import streamlit as st
from services.comics import (
    list_all_comics,
    list_marvel,
    list_manga,
    filter_marvel,
    filter_manga,
    get_marvel_by_id,
    get_manga_by_id,
    manga_card,
    marvel_card
)


from ui.background import set_background
set_background("assets/comicsfondo.png")

st.set_page_config(layout="wide")

# Proteger acceso
if "token" not in st.session_state:
    st.error("Debes iniciar sesión para acceder.")
    st.stop()


st.title("📘 Catálogo de Cómics")

modo = st.selectbox(
    "Selecciona categoría",
    ["Todos", "Marvel", "Manga", "Filtrar Marvel", "Filtrar Manga", "Buscar por ID"]
)

# -------------------------
# TODOS
# -------------------------
if modo == "Todos":
    comics = list_all_comics()

    mangas = [d for d in comics if "manga_id" in d]
    marvels = [c for c in comics if "marvel_id" in c]

   
    col_manga, col_marvel = st.columns(2)

    # ---------------- MANGA (izquierda) ----------------
    with col_manga:

        st.header("🍜 Manga")

        for i, m in enumerate(mangas):
            manga_card(m)
            st.divider()

    # ---------------- MARVEL (derecha) ----------------
    with col_marvel:
        st.header("🦸 Marvel")

        for m in marvels:
            marvel_card(m)
            st.divider()

# -------------------------
# MARVEL
# -------------------------
elif modo == "Marvel":
    comics = list_marvel()

    cols = st.columns(2)

    for i , m in enumerate(comics):
        with cols[i % 2]:
            marvel_card(m)
            st.divider()

# -------------------------
# MANGA
# -------------------------
elif modo == "Manga":
    comics = list_manga()

    cols = st.columns(2)

    for i, m in enumerate(comics):
        with cols[i % 2]:
            manga_card(m)
            st.divider()
# -------------------------
# FILTRO MARVEL
# -------------------------
elif modo == "Filtrar Marvel":
    writer = st.text_input("Writer")
    penciler = st.text_input("Penciler")
    rating = st.text_input("Rating")
    imprint = st.text_input("Imprint")
    page = st.number_input("Página", min_value=1, value=1)
    size = st.number_input("Tamaño", min_value=1, max_value=50, value=10)

    if st.button("Buscar Marvel"):
        comics = filter_marvel(writer, penciler, rating, imprint, page, size)
        for c in comics:
            marvel_card(c)

# -------------------------
# FILTRO MANGA
# -------------------------
elif modo == "Filtrar Manga":
    author = st.text_input("Author")
    publisher = st.text_input("Publisher")
    demographic = st.text_input("Demographic")
    serialized = st.text_input("Serialized")
    page = st.number_input("Página", min_value=1, value=1)
    size = st.number_input("Tamaño", min_value=1, max_value=50, value=10)

    if st.button("Buscar Manga"):
        comics = filter_manga(author, publisher, demographic, serialized, page, size)
        for c in comics:
            manga_card(c)

# -------------------------
# BUSCAR POR ID
# -------------------------
elif modo == "Buscar por ID":
    tipo = st.radio("Tipo", ["Marvel", "Manga"])
    comic_id = st.number_input("ID del cómic", min_value=1)

    if st.button("Buscar"):
        if tipo == "Marvel":
            comic = get_marvel_by_id(comic_id)
            st.subheader(comic["issue_title"])
            marvel_card(comic)
        else:
            comic = get_manga_by_id(comic_id)
            st.subheader(comic["Manga_series"])
            manga_card(comic)
       