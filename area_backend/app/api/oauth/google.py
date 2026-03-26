import os
import urllib.parse
import json
import httpx
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.api.oauth.utils import process_oauth_login

router = APIRouter(prefix="/auth/google", tags=["auth_google"])

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI_GOOGLE")
SCOPES = "openid email profile " \
         "https://www.googleapis.com/auth/gmail.readonly " \
         "https://www.googleapis.com/auth/gmail.send " \
         "https://www.googleapis.com/auth/drive.file " \
         "https://www.googleapis.com/auth/calendar.events " \
         "https://www.googleapis.com/auth/spreadsheets"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/login")
def login(user_id: str = None):
    state_data = {"user_id": user_id} if user_id and user_id != "null" else {}
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
        "state": json.dumps(state_data)
    }
    return RedirectResponse(f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}")


@router.get("/callback")
async def callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    if not code:
        raise HTTPException(400, "Code not found")

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            })
        token_data = token_resp.json()

        user_resp = await client.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={
                "Authorization": f"Bearer {token_data.get('access_token')}"
            })
        user_info = user_resp.json()

    jwt = process_oauth_login(db, "google", user_info, token_data, state)

    return RedirectResponse(f"{os.getenv('FRONTEND_URL')}/login?token={jwt}")
