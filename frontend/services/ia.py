from .api_client import post

def get_recommendations(user_profile: str, top_k: int = 5):
    payload = {
        "user_profile": user_profile,
        "top_k": top_k,
        "history": []
    }

    return post("/ai/recommend", payload)
