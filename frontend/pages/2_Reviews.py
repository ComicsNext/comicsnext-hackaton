from ui.background import set_background
set_background("assets/comicsfondo.png")



import streamlit as st
from services.reviews import (
    add_resenya,
    list_resenyas,
    list_all_resenyas,
    delete_resenya
)

if "token" not in st.session_state:
    st.error("Debes iniciar sesión para acceder.")
    st.stop()


st.title("📝 Reseñas")

modo = st.selectbox(
    "Selecciona acción",
    ["Ver reseñas de un cómic", "Añadir reseña", "Ver todas las reseñas", "Borrar reseña"]
)

# -------------------------
# VER RESEÑAS DE UN CÓMIC
# -------------------------
if modo == "Ver reseñas de un cómic":
    item_id = st.number_input("ID del cómic", min_value=1)
    nombre_tabla = st.selectbox("Tabla", ["marvel", "manga"])

    if st.button("Ver reseñas"):
        resenyas = list_resenyas(item_id, nombre_tabla)
        if not resenyas:
            st.info("No hay reseñas.")
        else:
            for r in resenyas:
                card = st.container(border=2)
                card.subheader(f"⭐ {r['valoracion']}")
                card.write(r["texto_resenya"])
                card.caption(f"ID reseña: {r['resenya_id']}")

# -------------------------
# AÑADIR RESEÑA
# -------------------------
elif modo == "Añadir reseña":
    item_id = st.number_input("ID del cómic", min_value=1)
    nombre_tabla = st.selectbox("Tabla", ["marvel", "manga"])
    texto = st.text_area("Texto de la reseña")
    valoracion = st.slider("Valoración", 1, 5)

    if st.button("Enviar reseña"):
        add_resenya(item_id, nombre_tabla, texto, valoracion)
        st.success("Reseña añadida correctamente.")

# -------------------------
# VER TODAS LAS RESEÑAS
# -------------------------
elif modo == "Ver todas las reseñas":
    resenyas = list_all_resenyas()
    for r in resenyas:
        st.subheader(f"⭐ {r['valoracion']}")
        st.write(r["texto_resenya"])
        st.caption(f"ID reseña: {r['resenya_id']} - Tabla: {r['nombre_tabla']} - Item: {r['item_id']}")

# -------------------------
# BORRAR RESEÑA
# -------------------------
elif modo == "Borrar reseña":
    resenya_id = st.number_input("ID de la reseña", min_value=1)

    if st.button("Borrar"):
        delete_resenya(resenya_id)
        st.success("Reseña eliminada.")
