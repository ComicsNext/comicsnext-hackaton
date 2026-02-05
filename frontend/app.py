import streamlit as st
from services.auth import login_user, register_user


from ui.background import set_background
set_background("assets/comicsfondo.png")

st.markdown(
    """
    <style>
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.95); 
        z-index: -1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="ComicsNext", layout="wide")

st.markdown(
    """
    <h1 style="
        font-size: 90px;
        text-align: center;
        font-weight: 900;
        background: linear-gradient(90deg, #ff0000, #ff9900, #ffee00, #00ccff, #0066ff);
        -webkit-background-clip: text;
        color: transparent;
        font-family: 'Comic Sans MS', sans-serif;
        margin-bottom: 40px;
        text-shadow:
            1px 1px 0px #000000,
            -1px 1px 0px #000000,
            1px -1px 0px #000000,
            -1px -1px 0px #000000;
    ">
        ComicsNext
    </h1>
    """,
    unsafe_allow_html=True
)

tab_login, tab_registro = st.tabs(["Iniciar sesión", "Registrarse"])

with tab_login:
    st.subheader("Iniciar sesión")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Contraseña", type="password", key="login_password")

    if st.button("Entrar", key="login_button"):
        try:
            token = login_user(email, password)
            st.session_state["token"] = token["access_token"]
            st.session_state["user_email"] = email
            st.session_state["logged"] = True
            st.success("Sesión iniciada correctamente.")
        except:
            st.error("Credenciales incorrectas")

with tab_registro:
    st.subheader("Crear cuenta")

    nombre = st.text_input("Nombre completo", key="reg_nombre")
    email_reg = st.text_input("Email", key="reg_email")
    genero = st.selectbox("Género", ["Hombre", "Mujer", "Otro"], key="reg_genero")
    fecha_naci = st.date_input("Fecha de nacimiento", key="reg_fecha")
    password_reg = st.text_input("Contraseña", type="password", key="reg_password")

    if st.button("Registrarme", key="reg_button"):
        try:
            register_user(
                nombre=nombre,
                email=email_reg,
                genero=genero,
                fecha_naci=str(fecha_naci),
                password=password_reg
            )
            st.success("Usuario registrado correctamente. Ya puedes iniciar sesión.")
        except:
            st.error("No se pudo registrar el usuario.")
