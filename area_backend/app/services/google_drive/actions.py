import requests
from app.core.registry import register_action


def check_new_files(params):
    url = "https://www.googleapis.com/drive/v3/files?orderBy=createdTime desc&pageSize=1"
    headers = {"Authorization": f"Bearer {params['access_token']}"}

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return None

    files = resp.json().get("files", [])
    if not files:
        return None

    latest_file = files[0]
    file_id = latest_file["id"]

    if params.get("last_file_id") == file_id:
        return None

    params["last_file_id"] = file_id

    return {
        "file_name": latest_file.get("name"),
        "file_id": file_id,
        "mime_type": latest_file.get("mimeType")
    }


register_action("google_drive", "new_file", "New file created in Drive", check_new_files)
