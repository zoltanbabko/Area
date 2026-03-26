import requests


def spotify_headers(access_token: str) -> dict:
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }


def spotify_get(access_token: str, url: str, params: dict | None = None) -> dict:
    r = requests.get(
        url,
        headers=spotify_headers(access_token),
        params=params,
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def spotify_post(access_token: str, url: str, json: dict | None = None) -> dict:
    r = requests.post(
        url,
        headers=spotify_headers(access_token),
        json=json,
        timeout=10,
    )
    r.raise_for_status()
    return r.json() if r.content else {}
