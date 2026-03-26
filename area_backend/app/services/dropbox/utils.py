import json
import requests


def dropbox_headers(access_token: str) -> dict:
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }


def dropbox_post(access_token: str, url: str, payload: dict) -> dict:
    r = requests.post(url, headers=dropbox_headers(access_token), json=payload, timeout=10)
    r.raise_for_status()
    return r.json()


def dropbox_upload(access_token: str, path: str, content: bytes) -> dict:
    r = requests.post(
        "https://content.dropboxapi.com/2/files/upload",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Dropbox-API-Arg": json.dumps({"path": path, "mode": "add", "autorename": True}),
            "Content-Type": "application/octet-stream",
        },
        data=content,
        timeout=20,
    )
    r.raise_for_status()
    return r.json()
