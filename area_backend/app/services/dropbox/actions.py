from app.core.registry import register_action

from .utils import dropbox_post


@register_action(
    service="dropbox",
    key="file_added",
    name="File added",
    description="Triggers when a file is added/changed in a Dropbox folder (polling via cursor).",
    args={
        "path": {
            "type": "string",
            "description": "Dropbox folder path to watch (e.g. '/Apps/myarea'). Use '' for root.",
            "required": False,
            "default": "",
        },
    },
    requires_auth=True,
    polling=True,
)
def file_added(access_token: str, args: dict, state: dict) -> dict | None:
    watched_path = args.get("path", "") or ""
    cursor = state.get("cursor")
    last_triggered_id = state.get("last_entry_id")

    if not cursor:
        res = dropbox_post(
            access_token,
            "https://api.dropboxapi.com/2/files/list_folder",
            {"path": watched_path, "recursive": False, "include_deleted": False},
        )
        state["cursor"] = res.get("cursor")
        return None

    res = dropbox_post(
        access_token,
        "https://api.dropboxapi.com/2/files/list_folder/continue",
        {"cursor": cursor},
    )
    state["cursor"] = res.get("cursor")

    entries = res.get("entries") or []
    if not entries:
        return None
    entry = entries[0]
    entry_id = entry.get("id") or entry.get("path_lower")
    if not entry_id or entry_id == last_triggered_id:
        return None

    state["last_entry_id"] = entry_id
    return {
        "name": entry.get("name"),
        "path": entry.get("path_display") or entry.get("path_lower"),
        "id": entry_id,
        "tag": entry.get(".tag"),
    }
