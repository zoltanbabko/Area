import os
import urllib.parse
import json
import httpx
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.api.oauth.utils import process_oauth_login

router = APIRouter(prefix="/auth/discord", tags=["auth_discord"])

CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8080/auth/discord/callback"
SCOPES = "identify email guilds"


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
        "state": json.dumps(state_data)
    }
    return RedirectResponse(f"https://discord.com/api/oauth2/authorize?{urllib.parse.urlencode(params)}")


@router.get("/callback")
async def callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    if not code:
        raise HTTPException(400, "Code not found")

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://discord.com/api/oauth2/token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        token_data = token_resp.json()
        user_resp = await client.get(
            "https://discord.com/api/users/@me",
            headers={
                "Authorization": f"Bearer {token_data.get('access_token')}"
            })
        user_info = user_resp.json()

    jwt = process_oauth_login(db, "discord", user_info, token_data, state)

    return RedirectResponse(f"http://localhost:8081/login?token={jwt}")
