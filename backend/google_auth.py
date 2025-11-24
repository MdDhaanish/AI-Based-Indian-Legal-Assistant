from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/google-login")
def google_login():
    return RedirectResponse("http://localhost:5500/index.html")
