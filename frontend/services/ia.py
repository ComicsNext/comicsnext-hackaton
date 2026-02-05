from .api_client import post

def get_recommendations(user_id: int):
    return post("/ia/recommendations", {"user_id": user_id})
