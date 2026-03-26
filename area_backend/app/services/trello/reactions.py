import requests

from app.core.registry import register_reaction

from .utils import trello_auth_params


@register_reaction(
    service="trello",
    key="create_card",
    name="Create card",
    description="Creates a Trello card in a list.",
    args={
        "api_key": {"type": "string", "description": "Trello API key."},
        "token": {"type": "string", "description": "Trello token."},
        "list_id": {"type": "string", "description": "Trello list ID (idList)."},
        "name": {"type": "string", "description": "Card title."},
        "desc": {"type": "string", "description": "Card description (optional).", "required": False},
    },
    requires_auth=True,
)
def create_card(params: dict):
    api_key = params["api_key"]
    token = params["token"]
    list_id = params["list_id"]
    name = params["name"]
    desc = params.get("desc", "")

    url = "https://api.trello.com/1/cards"
    payload = {
        "idList": list_id,
        "name": name,
        "desc": desc,
        **trello_auth_params(api_key, token),
    }
    r = requests.post(url, params=payload, timeout=10)
    r.raise_for_status()
    data = r.json()
    return {"card_id": data.get("id"), "url": data.get("url")}
