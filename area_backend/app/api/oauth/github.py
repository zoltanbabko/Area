import os
import urllib.parse
import httpx
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.api.oauth.utils import process_oauth_login

router = APIRouter(prefix="/auth/github", tags=["auth_github"])

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI_GITHUB")


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
        "redirect_uri": REDIRECT_URI,
        "scope": "repo user",
        "state": json.dumps(state_data)
    }
    return RedirectResponse(f"https://github.com/login/oauth/authorize?{urllib.parse.urlencode(params)}")


@router.get("/callback")
async def callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    if not code:
        raise HTTPException(400, "Code not found")

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "redirect_uri": REDIRECT_URI
            },
            headers={"Accept": "application/json"}
        )
        token_data = token_resp.json()

        user_resp = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {token_data.get('access_token')}"
            })
        user_info = user_resp.json()

    jwt = process_oauth_login(db, "github", user_info, token_data, state)

    return RedirectResponse(f"{os.getenv('FRONTEND_URL')}/login?token={jwt}")
