import json
import requests

from app.core.registry import register_reaction


@register_reaction(
    service="dropbox",
    key="create_text_file",
    name="Create text file",
    description="Uploads a text file to Dropbox.",
    args={
        "path": {"type": "string", "description": "Destination path, e.g. /notes/hello.txt"},
        "content": {"type": "string", "description": "File content (text)."},
    },
    requires_auth=True,
)
def create_text_file(access_token: str, args: dict, params: dict):
    path = args.get("path")
    content = args.get("content", "")

    if not path:
        return {"error": "missing_path"}

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream",
        "Dropbox-API-Arg": json.dumps({
            "path": path,
            "mode": "add",
            "autorename": True,
            "mute": False,
            "strict_conflict": False,
        }),
    }
    r = requests.post(
        "https://content.dropboxapi.com/2/files/upload",
        headers=headers,
        data=content.encode("utf-8"),
        timeout=15,
    )
    if r.status_code >= 400:
        return {"error": "dropbox_upload_failed", "status": r.status_code, "body": r.text[:500]}

    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}
    return {
        "ok": True,
        "path_display": data.get("path_display"),
        "id": data.get("id"),
        "name": data.get("name"),
    }
