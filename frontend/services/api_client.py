import requests
import streamlit as st

BASE_URL = "http://localhost:8000"
def _headers():
    headers = {"Content-Type": "application/json"}
    token = st.session_state.get("token")
    if token:
        headers["x-token"] = token
        headers["Authorization"] = f"Bearer {token}"
    return headers

def post(path, data=None, params=None):
    r = requests.post(BASE_URL + path, params=params, json=data, headers=_headers())
    if not r.ok:
        raise RuntimeError(f"POST {path} -> {r.status_code}\n{r.text}")
    return r.json()

def get(path, params=None):
    r = requests.get(BASE_URL + path, params=params, headers=_headers())
    if not r.ok:
        raise RuntimeError(f"GET {path} -> {r.status_code}\n{r.text}")
    return r.json()