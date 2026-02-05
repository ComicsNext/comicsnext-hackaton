import requests
import streamlit as st

API_URL = "http://localhost:8000"

def _auth_headers():
    if "token" in st.session_state:
        return {"Authorization": f"Bearer {st.session_state['token']}"}
    return {}

def get(path, params=None):
    r = requests.get(
        f"{API_URL}{path}",
        params=params,
        headers=_auth_headers()
    )
    r.raise_for_status()
    return r.json()

def post(path, data=None):
    r = requests.post(
        f"{API_URL}{path}",
        json=data,
        headers=_auth_headers()
    )
    r.raise_for_status()
    return r.json()
