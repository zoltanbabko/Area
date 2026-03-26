from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.registry import ACTIONS, REACTIONS
from app.api.dependencies import get_current_user
from app.models.user import OAuth2Token
from app.core.hook_engine import get_fresh_token
import app.services.discord.utils as discord_utils
import app.services.openweather.utils as weather_utils
import app.services.github.utils as github_utils

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/services")
def services(user=Depends(get_current_user), db: Session = Depends(get_db)):
    services_data = {}

    AUTH_MAP = {
        "gmail": "google",
        "google_drive": "google",
        "google_calendar": "google",
        "google_sheets": "google",
        "discord": "discord",
        "github": "github",
        "outlook": "microsoft",
        "onedrive": "microsoft",
    }

    user_tokens = db.query(OAuth2Token).filter(OAuth2Token.user_id == user.id).all()
    connected_providers = [t.provider for t in user_tokens]

    def add_item(target_dict, item_type, item_def):
        s_name = item_def["service"]

        if s_name not in target_dict:
            provider = AUTH_MAP.get(s_name)
            target_dict[s_name] = {
                "actions": [],
                "reactions": [],
                "connected": False,
                "auth_provider": provider
            }
            if not provider or provider in connected_providers:
                target_dict[s_name]["connected"] = True

        target_dict[s_name][item_type].append({
            "name": item_def["name"],
            "description": item_def["description"],
            "args": item_def["args"]
        })

    for a in ACTIONS.values():
        add_item(services_data, "actions", a)

    for r in REACTIONS.values():
        add_item(services_data, "reactions", r)

    return services_data


@router.get("/services/{service_name}/{item_type}/{item_name}/options/{field_name}")
def get_field_options(service_name: str, item_type: str, item_name: str, field_name: str, user=Depends(get_current_user)):
    registry = ACTIONS if item_type == "actions" else REACTIONS
    key = f"{service_name}.{item_name}"
    item_def = registry.get(key)

    if not item_def:
        return []

    field_def = item_def["args"].get(field_name)
    if not field_def or field_def.get("type") != "select":
        return []

    source_func_name = field_def.get("dynamic_source")
    if not source_func_name:
        return []

    token = get_fresh_token(user.id, service_name)

    if service_name == "discord" and source_func_name == "get_discord_channels":
        return discord_utils.get_discord_channels(token)

    if service_name == "openweather":
        if source_func_name == "get_operators":
            return weather_utils.get_operators()
        if source_func_name == "get_weather_conditions":
            return weather_utils.get_weather_conditions()

    if service_name == "github" and source_func_name == "get_user_repos":
        return github_utils.get_user_repos(token)

    return []
