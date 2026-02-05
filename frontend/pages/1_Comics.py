import streamlit as st
from services.comics import (
    list_all_comics,
    list_marvel,
    list_manga,
    filter_marvel,
    filter_manga,
    get_marvel_by_id,
    get_manga_by_id
)


from ui.background import set_background
set_background("assets/comicsfondo.png")

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

    # separar
    mangas = [c for c in comics if "manga_id" in c]
    marvels = [c for c in comics if "marvel_id" in c]

    # ---------------- MANGA ----------------
    st.header("🍜 Manga")

    cols = st.columns(2)

    for i, m in enumerate(mangas):
        with cols[i % 2]:
            st.markdown(f"""
            ### 📖 {m['Manga_series']}
            **Autor:** {m['Author_s']}  
            **Demographic:** {m['Demographic']}  
            **Publisher:** {m['Publisher']}  
            **Volúmenes:** {m['No_of_collected_volumes']}  
            **Ventas:** {m['Approximate_sales_in_million_s']}M  
            **Serializado:** {m['Serialized']}
            """)
            st.divider()

     # ---------------- MARVEL ----------------
        st.header("🦸 Marvel")

        cols = st.columns(2)

        for i, m in enumerate(marvels):
            
            with cols[i % 2]:
                st.divider()
                st.markdown(f"""
                ### 🦸 {m['issue_title']}
                **Serie:** {m['comic_name']}  
                **Writer:** {m['writer']}  
                **Penciler:** {m['penciler']}  
                **Rating:** {m['Rating']}  
                **Fecha:** {m['publish_date']}  
                **Formato:** {m['Format']}  
                **Precio:** {m['Price']}
                {m['issue_description']}
                """)
        

# -------------------------
# MARVEL
# -------------------------
elif modo == "Marvel":
    comics = list_marvel()
    for c in comics:
        st.subheader(c["title"])
        st.write(c)

# -------------------------
# MANGA
# -------------------------
elif modo == "Manga":
    comics = list_manga()
    for c in comics:
        st.subheader(c["title"])
        st.write(c)

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
            st.subheader(c["title"])
            st.write(c)

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
            st.subheader(c["title"])
            st.write(c)

# -------------------------
# BUSCAR POR ID
# -------------------------
elif modo == "Buscar por ID":
    tipo = st.radio("Tipo", ["Marvel", "Manga"])
    comic_id = st.number_input("ID del cómic", min_value=1)

    if st.button("Buscar"):
        if tipo == "Marvel":
            comic = get_marvel_by_id(comic_id)
        else:
            comic = get_manga_by_id(comic_id)

        st.subheader(comic["title"])
        st.write(comic)
