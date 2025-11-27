# backend/auth_router.py
import os
import yaml
import bcrypt
import jwt
import pathlib
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi.responses import JSONResponse
from fastapi import Cookie
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import APIRouter


BASE_DIR = pathlib.Path(__file__).resolve().parents[1]   # Goes to Assistant/
AUTH_YAML_PATH = BASE_DIR / "credentials" / "auth_config.yaml"


# JWT secret (set this in your .env or change below)
JWT_SECRET = os.getenv("AUTH_JWT_SECRET", "change_this_secret_in_env")
JWT_ALGORITHM = "HS256"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
async def me(request: Request):
    cfg = load_auth_config()
    cookie_name = cfg.get("cookie", {}).get("name", "legalassistant")
    token = request.cookies.get(cookie_name)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {"user": {"username": payload.get("sub"), "email": payload.get("email"), "name": payload.get("name")}}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")


router = APIRouter(prefix="/auth")

@router.post("/google")
async def google_login(data: dict):
    token = data.get("id_token")
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        email = idinfo["email"]
        name = idinfo.get("name", email.split("@")[0])

        # return a JWT to frontend
        jwt_token = create_access_token({"email": email})

        return {
            "success": True,
            "token": jwt_token,
            "email": email,
            "name": name
        }


    except Exception as e:
        return {"success": False, "error": str(e)}

def load_auth_config():
    if not os.path.exists(AUTH_YAML_PATH):
        raise FileNotFoundError(f"Auth file not found at {AUTH_YAML_PATH}")
    with open(AUTH_YAML_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg

def find_user_by_email(email: str, cfg: dict):
    # YAML structure: credentials -> usernames -> <username> -> { email, name, password }
    users = cfg.get("credentials", {}).get("usernames", {}) or {}
    for username, info in users.items():
        if info.get("email") == email:
            # return tuple (username, info)
            return username, info
    return None, None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # hashed_password is bcrypt string like "$2b$12$..."
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

@router.post("/signup")
async def signup(payload: dict):
    email = payload.get("email")
    password = payload.get("password")
    name = payload.get("name")

    if not email or not password or not name:
        raise HTTPException(status_code=400, detail="All fields required")

    cfg = load_auth_config()
    users = cfg.get("credentials", {}).get("usernames", {})

    # Check if user already exists
    for _, info in users.items():
        if info.get("email") == email:
            raise HTTPException(status_code=400, detail="User already exists")

    # Create new username
    username = email.split("@")[0]

    # Hash password
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # Add user
    users[username] = {
        "email": email,
        "name": name,
        "password": hashed
    }

    cfg["credentials"]["usernames"] = users

    # Save back to YAML
    with open(AUTH_YAML_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f)

    return {"success": True, "message": "User registered successfully"}

@router.post("/login")
async def login(payload: dict, response: Response):
    """
    POST /auth/login
    body: { "email": "...", "password": "..." }
    Sets HTTPOnly cookie with JWT on success.
    Returns JSON { token, user } as well.
    """
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required.")

    cfg = load_auth_config()
    username, info = find_user_by_email(email, cfg)
    if not info:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    hashed = info.get("password")
    if not verify_password(password, hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    # build JWT
    expiry_days = cfg.get("cookie", {}).get("expiry_days", 1)
    expiry = datetime.utcnow() + timedelta(days=expiry_days)
    token_payload = {
        "sub": username,
        "email": email,
        "name": info.get("name"),
        "exp": expiry
    }
    token = jwt.encode(token_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    # set cookie parameters from YAML
    cookie_name = cfg.get("cookie", {}).get("name", "legalassistant")
    cookie_key = cfg.get("cookie", {}).get("key", None)
    # set HTTPOnly cookie (secure flag off for localhost; set secure=True in prod with https)
    response.set_cookie(
        key=cookie_name,
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        expires=int(expiry.timestamp()),
    )

    return JSONResponse({"token": token, "user": {"username": username, "email": email, "name": info.get("name")}})

@router.post("/logout")
async def logout(response: Response):
    cfg = load_auth_config()
    cookie_name = cfg.get("cookie", {}).get("name", "legalassistant")
    # remove cookie by setting expired
    response.delete_cookie(cookie_name)
    return {"detail": "Logged out"}
