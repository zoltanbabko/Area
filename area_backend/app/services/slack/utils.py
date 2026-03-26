import requests


def slack_headers(access_token: str) -> dict:
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8",
    }


def slack_get(access_token: str, url: str, params: dict | None = None) -> dict:
    r = requests.get(url, headers=slack_headers(access_token), params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    if not data.get("ok", True):
        raise requests.HTTPError(data.get("error", "slack_error"))
    return data


def slack_post(access_token: str, url: str, payload: dict) -> dict:
    r = requests.post(url, headers=slack_headers(access_token), json=payload, timeout=10)
    r.raise_for_status()
    data = r.json()
    if not data.get("ok", True):
        raise requests.HTTPError(data.get("error", "slack_error"))
    return data
