import requests


def trello_auth_params(api_key: str, token: str) -> dict:
    return {"key": api_key, "token": token}


def trello_get(api_key: str, token: str, url: str, params: dict | None = None) -> dict:
    p = trello_auth_params(api_key, token)
    if params:
        p.update(params)
    r = requests.get(url, params=p, timeout=10)
    r.raise_for_status()
    return r.json()


def trello_post(api_key: str, token: str, url: str, data: dict) -> dict:
    p = trello_auth_params(api_key, token)
    p.update(data)
    r = requests.post(url, params=p, timeout=10)
    r.raise_for_status()
    return r.json()
