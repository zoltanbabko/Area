import requests


def get_user_repos(access_token):
    if not access_token:
        return []

    url = "https://api.github.com/user/repos?sort=updated&per_page=100"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return []

    repos = resp.json()
    return [{"label": r["full_name"], "value": r["full_name"]} for r in repos]
