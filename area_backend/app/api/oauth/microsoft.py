import os
import urllib.parse
import httpx
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.api.oauth.utils import process_oauth_login

router = APIRouter(prefix="/auth/microsoft", tags=["auth_microsoft"])

CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI_MICROSOFT")

SCOPES = "User.Read Mail.Read Mail.Send Files.ReadWrite.All offline_access"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/login")
def login(user_id: str = None):
    state_data = {"user_id": user_id} if user_id and user_id != "null" else {}
    import json

    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "response_mode": "query",
        "scope": SCOPES,
        "state": json.dumps(state_data)
    }
    return RedirectResponse(f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?{urllib.parse.urlencode(params)}")


@router.get("/callback")
async def callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    if not code:
        raise HTTPException(400, "Code not found")

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://login.microsoftonline.com/common/oauth2/v2.0/token",
            data={
                "client_id": CLIENT_ID,
                "scope": SCOPES,
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
                "client_secret": CLIENT_SECRET,
            }
        )
        token_data = token_resp.json()

        if "error" in token_data:
            raise HTTPException(400, f"Microsoft Error: {token_data}")

        user_resp = await client.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={
                "Authorization": f"Bearer {token_data.get('access_token')}"
            })
        user_info = user_resp.json()

    if "email" not in user_info:
        user_info["email"] = user_info.get("userPrincipalName") or user_info.get("mail")

    jwt = process_oauth_login(db, "microsoft", user_info, token_data, state)

    return RedirectResponse(f"{os.getenv('FRONTEND_URL')}/login?token={jwt}")
