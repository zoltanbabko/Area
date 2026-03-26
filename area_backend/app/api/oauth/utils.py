import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.user import User, OAuth2Token
from app.security import create_access_token
from sqlalchemy import func


def process_oauth_login(db: Session, provider: str, user_info: dict, token_data: dict, state: str = None):
    email = user_info.get("email")
    if not email and "login" in user_info:
        email = f"{user_info['login']}"

    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in", 3600)
    expires_at = int(datetime.now(timezone.utc).timestamp()) + expires_in
    user = None

    if state:
        try:
            state_data = json.loads(state)
            if "user_id" in state_data:
                user = db.query(User).filter(User.id == state_data["user_id"]).first()
        except json.JSONDecodeError:
            pass

    if not user:
        user = db.query(User).filter(func.lower(User.username) == email.lower()).first()

        if not user:
            user = User(username=email)
            db.add(user)
            db.commit()
            db.refresh(user)

    oauth_token = db.query(OAuth2Token).filter(
        OAuth2Token.user_id == user.id,
        OAuth2Token.provider == provider
    ).first()

    if oauth_token:
        oauth_token.access_token = access_token
        oauth_token.expires_at = expires_at
        if refresh_token:
            oauth_token.refresh_token = refresh_token
    else:
        oauth_token = OAuth2Token(
            user_id=user.id,
            provider=provider,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at
        )
        db.add(oauth_token)

    db.commit()

    return create_access_token({"user_id": user.id})
