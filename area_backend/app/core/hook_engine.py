from app.core.registry import ACTIONS, REACTIONS
from app.database import SessionLocal
from app.models.area import Area
from app.models.user import OAuth2Token
import json


def get_fresh_token(user_id, service):
    db = SessionLocal()

    PROVIDER_MAP = {
        "gmail": "google",
        "google_drive": "google",
        "google_calendar": "google",
        "google_sheets": "google",
        "google": "google",
        "discord": "discord",
        "github": "github",
        "outlook": "microsoft",
        "onedrive": "microsoft",
    }

    provider_name = PROVIDER_MAP.get(service, service)

    token_entry = db.query(OAuth2Token).filter_by(user_id=user_id, provider=provider_name).first()
    db.close()

    if token_entry:
        return token_entry.access_token
    return None


def _interpolate_params(reaction_params, action_result):
    if not isinstance(action_result, dict):
        return reaction_params

    try:
        str_params = json.dumps(reaction_params)
        for key, value in action_result.items():
            str_params = str_params.replace(f"{{{{ {key} }}}}", str(value))
            str_params = str_params.replace(f"{{{{{key}}}}}", str(value))
        return json.loads(str_params)
    except Exception as e:
        print(f"[ERROR] Variable interpolation failed: {e}")
        return reaction_params


def _execute_action_step(area, action_def, action_params):
    token = get_fresh_token(area.user_id, action_def["service"])

    if token:
        action_params["access_token"] = token
    elif action_def["service"] not in ["timer", "openweather"]:
        print(f"[WARNING] Area {area.id}: Missing OAuth token for service '{action_def['service']}'")
        return None

    try:
        return action_def["handler"](action_params)
    except Exception as e:
        print(f"[ERROR] Area {area.id} - Action '{area.action}' failed: {e}")
        return None


def _execute_reaction_step(area, reaction_def, reaction_params):
    token = get_fresh_token(area.user_id, reaction_def["service"])
    if token:
        reaction_params["access_token"] = token

    try:
        reaction_def["handler"](reaction_params)
        print(f"[SUCCESS] Area {area.id} reaction executed: {area.reaction}")
    except Exception as e:
        print(f"[ERROR] Area {area.id} - Reaction '{area.reaction}' failed: {e}")


def execute_area(area_id: int):
    db = SessionLocal()
    area = db.query(Area).filter(Area.id == area_id).first()

    if not area:
        db.close()
        return

    action_def = ACTIONS.get(area.action)
    reaction_def = REACTIONS.get(area.reaction)

    if not action_def or not reaction_def:
        print(f"[ERROR] Area {area.id}: Action or Reaction not found in registry.")
        db.close()
        return

    action_params = area.action_params.copy()
    action_result = _execute_action_step(area, action_def, action_params)

    if not action_result:
        db.close()
        return

    print(f"[SUCCESS] Area {area.id} triggered: {area.action}")

    action_params.pop("access_token", None)
    area.action_params = action_params
    db.commit()

    reaction_params = area.reaction_params.copy()
    reaction_params = _interpolate_params(reaction_params, action_result)

    _execute_reaction_step(area, reaction_def, reaction_params)

    db.close()
