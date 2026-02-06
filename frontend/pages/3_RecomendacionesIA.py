import streamlit as st
from services.ia import get_recommendations
from ui.background import set_background

def load_css(path: str):
    with open(path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

set_background("assets/comicsfondo.png")
load_css("assets/ia.css")

if "token" not in st.session_state:
    st.error("Debes iniciar sesión para acceder.")
    st.stop()

# ---------- Header tipo "hero" ----------
st.markdown(
    """
    <div class="cn-header">
      <div class="cn-kicker">Copiloto de lectura</div>
      <div class="cn-title">🤖 Recomendaciones IA</div>
      <div class="cn-subtitle">
        Describe tu estilo (géneros, tono, autores, vibes) y te propongo mangas del catálogo.
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- Card principal ----------
st.markdown('<div class="cn-card cn-ai-card">', unsafe_allow_html=True)

user_profile = st.text_area(
    "🧠 ¿Qué tipo de mangas te gustan?",
    placeholder="Ej: Me gustan mangas oscuros tipo Berserk, acción, demonios, sin comedia...",
    height=140,
)

c1, c2 = st.columns([1, 1])
with c1:
    top_k = st.slider("🎯 Cantidad de recomendaciones", 1, 10, 5)
with c2:
    st.markdown('<div class="cn-hint">Tip: menciona 2–3 referencias (“tipo X”), lo que NO quieres y el tono.</div>', unsafe_allow_html=True)

btn = st.button("✨ Obtener recomendaciones", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)  # cierre card

# ---------- Resultados ----------
if btn:
    if not user_profile.strip():
        st.warning("Escribe qué te gusta para recomendarte algo.")
        st.stop()

    with st.spinner("Generando recomendaciones..."):
        data = get_recommendations(user_profile, top_k)

    recs = data.get("recommendations", [])

    st.markdown('<div class="cn-results">', unsafe_allow_html=True)

    if not recs:
        st.info("No he encontrado recomendaciones con ese perfil. Prueba a ser más específico/a.")
    else:
        for r in recs:
            title = r.get("title", "Sin título")
            reason = r.get("reason", "")

            st.markdown(
                f"""
                <div class="cn-rec">
                  <div class="cn-rec-title">{title}</div>
                  <div class="cn-rec-reason">{reason}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)