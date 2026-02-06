from .api_client import get
import streamlit as st

# Catálogo completo
def list_all_comics():
    return get("/comics")

# Marvel
def list_marvel():
    return get("/comics/marvel")

def filter_marvel(writer=None, penciler=None, rating=None, imprint=None, page=1, size=10):
    params = {
        "writer": writer,
        "penciler": penciler,
        "rating": rating,
        "imprint": imprint,
        "page": page,
        "size": size
    }
    return get("/comics/filter/marvel", params=params)

def get_marvel_by_id(marvel_id: int):
    return get(f"/comics/marvel/{marvel_id}")

# Manga
def list_manga():
    return get("/comics/manga")

def filter_manga(author=None, publisher=None, demographic=None, serialized=None, page=1, size=10):
    params = {
        "author": author,
        "publisher": publisher,
        "demographic": demographic,
        "serialized": serialized,
        "page": page,
        "size": size
    }
    return get("/comics/filter/manga", params=params)

def get_manga_by_id(manga_id: int):
    return get(f"/comics/manga/{manga_id}")


# Estilo Tajetas

st.markdown("""
<style>
.card:hover {
    transform: scale(1.03);
    transition: 0.2s;
    box-shadow: 0 12px 28px rgba(0,0,0,0.6);
}
</style>
""", unsafe_allow_html=True)


def manga_card(m):
    st.markdown(f"""
    <div class="card" style="
        background-color: rgba(20,20,20,0.85);
        padding: 18px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 6px 18px rgba(0,0,0,0.4);
        margin-bottom: 18px;
        backdrop-filter: blur(6px);
    ">
        <h3 style="margin-bottom:10px;">📖 {m['Manga_series']}</h3>
        <p><b>Autor:</b> {m['Author_s']}</p>
        <p><b>Demographic:</b> {m['Demographic']}</p>
        <p><b>Publisher:</b> {m['Publisher']}</p>
        <p><b>Volúmenes:</b> {m['No_of_collected_volumes']}</p>
        <p><b>Ventas:</b> {m['Approximate_sales_in_million_s']}M</p>
        <p><b>Serializado:</b> {m['Serialized']}</p>
    </div>
    """, unsafe_allow_html=True)


    
def marvel_card(m):
    st.markdown(f"""
    <div class="card" style="
        background-color: rgba(20,20,20,0.85);
        padding: 18px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 6px 18px rgba(0,0,0,0.4);
        margin-bottom: 18px;
        backdrop-filter: blur(6px);
    ">
        <h3 style="margin-bottom:10px;">🦸 {m['issue_title']}</h3>


        <p><b>Serie:</b> {m['comic_name']}</p>
        <p><b>Writer:</b> {m['writer']}</p>
        <p><b>Penciler:</b> {m['penciler']}</p>
        <p><b>Rating:</b> ⭐ {m['Rating']}</p>
        <p><b>Fecha:</b> {m['publish_date']}</p>
        <p><b>Formato:</b> {m['Format']}</p>
        <p><b>Precio:</b> 💲{m['Price']}</p>


        <hr style="opacity:0.2">


        <p style="font-size: 0.9rem; opacity:0.85;">
            {m['issue_description']}
        </p>
    </div>
    """, unsafe_allow_html=True)