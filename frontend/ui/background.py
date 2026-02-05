import streamlit as st
import base64
import os

def set_background(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

   
    st.markdown(
        f"""
        <style>
        /* Fondo principal con imagen + overlay */
        .stApp {{
            background:
                linear-gradient(
                    rgba(0,0,0,0.75),
                    rgba(0,0,0,0.75)
                ),
                url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #f5f5f5;
        }}

        /* Capas internas TRANSPARENTES */
        .stAppViewContainer,
        .main,
        .block-container {{
            background: transparent !important;
        }}

        /* Texto general */
        h1, h2, h3, h4, h5, h6, p, label {{
            color: #f5f5f5 !important;
        }}

        /* Header superior sin fondo blanco */
        header[data-testid="stHeader"] {{
            background: transparent;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: rgba(20,20,20,0.95);
        }}

        section[data-testid="stSidebar"] * {{
            color: #f5f5f5 !important;
        }}

        section[data-testid="stSidebar"] button {{
            background-color: #2e2e2e;
            color: #ffffff;
            border-radius: 8px;
            border: none;
            padding: 0.5em;
        }}

        section[data-testid="stSidebar"] button:hover {{
            background-color: #444444;
        }}

        /* Botones del contenido principal */
        div.stButton > button {{
            background-color: #2e2e2e;
            color: #ffffff;
            border-radius: 10px;
            border: 1px solid #444;
            padding: 0.6em 1.2em;
            font-weight: 600;
        }}

        div.stButton > button:hover {{
            background-color: #444444;
            border-color: #666;
        }}

        /* Reducir margen superior */
        .block-container {{
            padding-top: 1rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

