import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="Legal AI Chatbot", layout="wide")

# Require authentication if you want:
if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
    st.switch_page("login.py")

st.title("⚖️ Legal AI Assistant – Chat Interface")

# load frontend (file is one level up from pages/)
html_file = os.path.join(os.path.dirname(__file__), "..", "frontend2.html")
with open(html_file, "r", encoding="utf-8") as f:
    html_source = f.read()

# simply render the HTML — frontend calls backend directly
components.html(html_source, height=1100, scrolling=True)
