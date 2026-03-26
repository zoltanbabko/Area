import urllib.parse
import requests


def gitlab_headers(access_token: str) -> dict:
    return {"Authorization": f"Bearer {access_token}"}


def gitlab_url(base_url: str, path: str) -> str:
    return base_url.rstrip("/") + "/" + path.lstrip("/")


def gitlab_get(access_token: str, base_url: str, path: str, params: dict | None = None):
    r = requests.get(
        gitlab_url(base_url, path),
        headers=gitlab_headers(access_token),
        params=params,
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def gitlab_post(access_token: str, base_url: str, path: str, data: dict):
    r = requests.post(
        gitlab_url(base_url, path),
        headers=gitlab_headers(access_token),
        data=data,
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def encode_project_id(project_id: str) -> str:
    return urllib.parse.quote_plus(project_id)
