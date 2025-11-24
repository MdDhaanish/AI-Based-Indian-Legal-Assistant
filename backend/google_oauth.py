# backend/google_oauth.py
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import os
import requests
from urllib.parse import urlencode, quote_plus

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
REDIRECT_URI = os.getenv("OAUTH_REDIRECT_URL", "http://localhost:8000/google-callback")
STREAMLIT_LOGIN = os.getenv("STREAMLIT_URL", "http://localhost:8501/login")

AUTH_BASE = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

@router.get("/google-login")
def google_login():
    """
    Redirect user to Google's OAuth 2.0 consent screen.
    """
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account consent"
    }
    url = f"{AUTH_BASE}?{urlencode(params, quote_via=quote_plus)}"
    return RedirectResponse(url)

@router.get("/google-callback")
def google_callback(request: Request, code: str = None, error: str = None):
    """
    Exchange code for tokens, fetch userinfo, then redirect back to Streamlit login page
    with email and id_token in query params.
    """
    if error:
        # Redirect back to Streamlit with error
        redirect_url = f"{STREAMLIT_LOGIN}?error={quote_plus(error)}"
        return RedirectResponse(redirect_url)

    if not code:
        redirect_url = f"{STREAMLIT_LOGIN}?error=no_code"
        return RedirectResponse(redirect_url)

    # Exchange code for tokens
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_resp = requests.post(TOKEN_URL, data=data, timeout=10)
    if token_resp.status_code != 200:
        err = token_resp.text
        return RedirectResponse(f"{STREAMLIT_LOGIN}?error={quote_plus(err)}")

    tokens = token_resp.json()
    access_token = tokens.get("access_token")
    id_token = tokens.get("id_token")

    # Get user info
    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo_resp = requests.get(USERINFO_URL, headers=headers, timeout=10)
    if userinfo_resp.status_code != 200:
        return RedirectResponse(f"{STREAMLIT_LOGIN}?error=userinfo_failed")

    userinfo = userinfo_resp.json()
    email = userinfo.get("email")
    name = userinfo.get("name", "")
    picture = userinfo.get("picture", "")

    # Build redirect to Streamlit with minimal data (do NOT include secrets)
    # We pass email and a compact token (id_token) for optional verification on Streamlit side
    params = {
        "email": email,
        "name": name,
        "id_token": id_token
    }
    redirect_url = f"{STREAMLIT_LOGIN}?{urlencode(params, quote_via=quote_plus)}"
    return RedirectResponse(redirect_url)
