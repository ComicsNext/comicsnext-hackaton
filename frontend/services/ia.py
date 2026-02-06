from .api_client import post
import streamlit as st

def get_recommendations(user_profile: str, top_k: int = 5):
    payload = {
        "user_profile": user_profile,
        "top_k": top_k,
        "history": []
    }

    return post("/ai/recommend", payload)


# Taejeta 

st.markdown("""
<style>
.card:hover {
    transform: scale(1.03);
    transition: 0.2s;
    box-shadow: 0 12px 28px rgba(0,0,0,0.6);
}
</style>
""", unsafe_allow_html=True)

def ia_card(m):
    title = m["title"]
    reason = m["reason"]

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
        <h3 style="margin-bottom:10px;">🤖 {title}</h3>
        <p>{reason}</p>
    </div>
    """, unsafe_allow_html=True)