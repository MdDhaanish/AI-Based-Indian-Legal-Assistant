import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="Login | Legal AI Assistant",
    page_icon="⚖️",
    layout="centered"
)

st.title("Welcome to Legal AI Assistant ⚖️")


# ------------------------------------------------------------
# GOOGLE LOGIN BUTTON
# ------------------------------------------------------------
st.markdown("""
<div style="text-align:center; margin-bottom:18px;">
  <a href="http://localhost:8000/google-login" target="_blank">
    <div style="
      display:inline-flex; align-items:center; gap:10px;
      padding:10px 18px; background:white; border-radius:8px; border:1px solid #ddd;
      box-shadow:0 2px 6px rgba(0,0,0,0.08); text-decoration:none; color:#222;
    ">
      <img src="https://developers.google.com/identity/images/g-logo.png" width="20"/>
      <span style="font-weight:600;">Continue with Google</span>
    </div>
  </a>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.write("### Or login using username/password:")


# ------------------------------------------------------------
# GOOGLE REDIRECT AFTER LOGIN
# ------------------------------------------------------------
query = st.query_params

email = query.get("email")
name = query.get("name")
id_token = query.get("id_token")
oauth_error = query.get("error")

# Show OAuth error if any
if oauth_error:
    st.error(f"Google OAuth Error: {oauth_error}")

# If we have email from Google -> auto-login user
if email:
    user_email = email[0] if isinstance(email, list) else email
    user_name = name[0] if isinstance(name, list) else (user_email.split("@")[0])

    st.session_state["authentication_status"] = True
    st.session_state["name"] = user_name
    st.session_state["username"] = user_email

    st.success(f"Logged in with Google: {user_email}")
    st.switch_page("pages/chat_ui.py")
  
# ------------------------------------------------------------
# USERNAME/PASSWORD LOGIN
# ------------------------------------------------------------
with open("credentials/auth_config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

authenticator.login(location="main")

auth_status = st.session_state.get("authentication_status")
user = st.session_state.get("name")

if auth_status is False:
    st.error("❌ Incorrect username or password")

elif auth_status is None:
    st.info("👤 Enter your login details")

elif auth_status:
    st.success(f"Welcome, {user} 👋")
    st.switch_page("pages/chat_ui.py")
# ------------------------------------------------------------



