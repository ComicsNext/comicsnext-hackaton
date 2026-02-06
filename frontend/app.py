import streamlit as st
from services.auth import login_user, register_user
from ui.background import set_background


def load_css(path: str):
    with open(path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ----------------------------
# 0) Page config SIEMPRE lo primero
# ----------------------------
st.set_page_config(page_title="COMICSNEXT", layout="wide")


# ----------------------------
# 1) Background + CSS externo
# ----------------------------
set_background("assets/comicsfondo.png")
load_css("assets/styles.css")


# ----------------------------
# 2) Header
# ----------------------------
st.markdown(
    """
    <div class="cn-header">
        <h1 class="cn-title">
            <span class="cn-comics">COMICS</span><span class="cn-next">NEXT</span>
        </h1>        
        <div class="cn-subtitle">
            Tu copiloto para descubrir cómics, reseñas y recomendaciones con IA
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ----------------------------
# 3) Layout centrado con card
# ----------------------------
left, center, right = st.columns([1, 1.25, 1])

with center:

    tab_login, tab_registro = st.tabs(["🔑 Iniciar sesión", "✨ Registrarse"])

    # -------- LOGIN --------
    with tab_login:
        st.subheader("Bienvenido de vuelta")
        st.caption("Accede a tu cuenta para ver cómics, reseñas y recomendaciones.")

        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Email", key="login_email", placeholder="tuemail@ejemplo.com")
            password = st.text_input("Contraseña", type="password", key="login_password", placeholder="••••••••")
            submitted = st.form_submit_button("Entrar")

        if submitted:
            try:
                token = login_user(email, password)
                st.session_state["token"] = token["access_token"]
                st.session_state["user_email"] = email
                st.session_state["logged"] = True
                st.success("✅ Sesión iniciada correctamente.")
                st.rerun()
            except Exception:
                st.error("❌ Credenciales incorrectas")

    # -------- REGISTRO --------
    with tab_registro:
        st.subheader("Crear cuenta")
        st.caption("Tarda menos de 1 minuto.")

        with st.form("register_form", clear_on_submit=False):
            nombre = st.text_input("Nombre completo", key="reg_nombre", placeholder="Nombre y apellidos")
            email_reg = st.text_input("Email", key="reg_email", placeholder="tuemail@ejemplo.com")

            col1, col2 = st.columns(2)
            with col1:
                genero = st.selectbox("Género", ["Hombre", "Mujer", "Otro"], key="reg_genero")
            with col2:
                fecha_naci = st.date_input("Fecha de nacimiento", key="reg_fecha")

            password_reg = st.text_input(
                "Contraseña",
                type="password",
                key="reg_password",
                placeholder="Mínimo 8 caracteres"
            )

            submitted_reg = st.form_submit_button("Registrarme")

        if submitted_reg:
            try:
                register_user(
                    nombre=nombre,
                    email=email_reg,
                    genero=genero,
                    fecha_naci=str(fecha_naci),
                    password=password_reg
                )
                st.success("✅ Usuario registrado. Ya puedes iniciar sesión.")
            except Exception:
                st.error("❌ No se pudo registrar el usuario.")

    st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------
# 4) Si ya está logueado, muestra accesito rápido
# ----------------------------
if st.session_state.get("logged"):
    st.success(f"Conectado como: {st.session_state.get('user_email')}")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("➡️ Ir a la app"):
            try:
                st.switch_page("pages/1_Comics.py")
            except Exception:
                st.info("Ve a la pestaña Pages (izquierda) para entrar a Comics / Reviews / Recomendaciones.")