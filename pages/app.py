import streamlit as st
import json
import os
import requests
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# ------------------- STREAMLIT PAGE CONFIG -------------------
st.set_page_config(
    page_title="Legal AI Assistant ⚖️",
    page_icon="⚖️",
    layout="wide",
)

# ------------------- CUSTOM CSS -------------------
st.markdown("""
<style>
body {
    background-color: #f8f9fa;
    font-family: serif;
}
div.stTextInput > label {
    font-size: 18px;
    font-weight: 600;
}
.chat-box {
    background: white;
    padding: 16px;
    border-radius: 10px;
    margin-bottom: 10px;
    border: 1px solid #e1e1e1;
}
.response-box {
    background: #e7f1ff;
    color: #000;
    padding: 16px;
    border-radius: 10px;
    border-left: 4px solid #0d6efd;
    font-size: 16px;
}
.simple-box {
    background: #fff4d6;
    color: #000;
    padding: 16px;
    border-radius: 10px;
    border-left: 4px solid #f4b400;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)



# ------------------- API ROUTE -------------------
API_URL = "http://127.0.0.1:8000/chatbot"

with open('credentials/auth_config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    cookie_key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days'],
)

name = st.session_state.get("name")
auth_status = st.session_state.get("authentication_status")

if not auth_status:
    st.error("Please login first.")
    st.stop()

authenticator.logout("Logout", "sidebar")
st.sidebar.write(f"👤 {name}")

st.title("⚖️ Legal AI Assistant")
st.caption("Ask questions related to Indian Law (IPC / CrPC / Constitution) and get simplified, accurate legal answers.")

# ------------------- USER INPUT -------------------
query = st.text_area(
    "Enter your legal question below:",
    placeholder="e.g., What is the punishment for theft under IPC?",
    height=120
)

# ------------------- ASK BUTTON -------------------
if st.button("Ask AI"):
    if not query.strip():
        st.warning("⚠️ Please enter a legal question.")
    else:
        with st.spinner("🔍 Analyzing legal query and fetching relevant sections..."):
            try:
                res = requests.post(API_URL, json={"query": query})
                data = res.json()

                # ✅ Legal Answer
                st.subheader("📘 Legal Answer")
                st.markdown(f"<div class='response-box'>{data.get('answer', '⚠️ No answer returned')}</div>", unsafe_allow_html=True)

                # ✅ Simplified Explanation
                st.subheader("📝 Simplified Explanation")
                st.markdown(f"<div class='simple-box'>{data.get('simplified', '⚠️ No simplified output')}</div>", unsafe_allow_html=True)

                # ✅ Legal Sections Used
                st.subheader("📜 Legal Sections Referenced")
                sections = data.get("sections_used", [])
                if sections:
                    for section in sections:
                        with st.expander(f"{section['act']} — {section['section']}"):
                            st.write(section["text"])
                else:
                    st.info("⚠️ No legal sections returned by backend")

            except Exception as e:
                st.error(f"Backend error: {e}")

