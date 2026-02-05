import requests

API_URL = "http://localhost:8000"  # FastAPI

def get(path, params=None):
    r = requests.get(f"{API_URL}{path}", params=params)
    r.raise_for_status()
    return r.json()

def post(path, data=None):
    r = requests.post(f"{API_URL}{path}", json=data)
    r.raise_for_status()
    return r.json()
