from app.core.registry import register_action

from .utils import trello_get


@register_action(
    service="trello",
    key="card_created_in_list",
    name="Card created in list",
    description="Triggers when a new Trello card is created in a given list (polling).",
    args={
        "api_key": {
            "type": "string",
            "description": "Trello API key (developer API key).",
        },
        "token": {
            "type": "string",
            "description": "Trello API token for the user.",
        },
        "list_id": {
            "type": "string",
            "description": "Trello list ID (the list to monitor).",
        },
    },
    requires_auth=True,
    polling=True,
)
def card_created_in_list(params: dict):
    """Return the new card payload when a new card is detected.

    Stores the latest card id in params['__last_card_id'].
    """
    api_key = params.get("api_key")
    token = params.get("token")
    list_id = params.get("list_id")
    if not api_key or not token or not list_id:
        return None

    cards = trello_get(
        api_key,
        token,
        f"https://api.trello.com/1/lists/{list_id}/cards",
        params={"fields": "id,name,desc,dateLastActivity,shortUrl", "limit": 1},
    )
    if not cards:
        return None

    latest = cards[0]
    last_id = params.get("__last_card_id")
    if last_id is None:
        params["__last_card_id"] = latest.get("id")
        return None

    if latest.get("id") != last_id:
        params["__last_card_id"] = latest.get("id")
        return {
            "id": latest.get("id"),
            "name": latest.get("name"),
            "desc": latest.get("desc"),
            "url": latest.get("shortUrl"),
            "list_id": list_id,
        }

    return None
