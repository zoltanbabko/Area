import requests
from app.core.registry import register_action


def check_new_push(params):
    repo_full_name = params.get("repository")
    if not repo_full_name:
        return None

    url = f"https://api.github.com/repos/{repo_full_name}/commits"
    headers = {
        "Authorization": f"Bearer {params['access_token']}",
        "Accept": "application/vnd.github.v3+json"
    }

    resp = requests.get(url, headers=headers, params={"per_page": 1})
    if resp.status_code != 200:
        return None

    commits = resp.json()
    if not commits:
        return None

    latest_commit = commits[0]
    sha = latest_commit["sha"]

    if params.get("last_commit_sha") == sha:
        return None

    params["last_commit_sha"] = sha

    commit_info = latest_commit["commit"]
    return {
        "author": commit_info["author"]["name"],
        "message": commit_info["message"],
        "url": latest_commit["html_url"],
        "repo": repo_full_name,
        "sha_short": sha[:7]
    }


register_action(
    "github",
    "new_push",
    "New Push/Commit detected",
    check_new_push,
    args={
        "repository": {
            "type": "select",
            "label": "Select Repository",
            "dynamic_source": "get_user_repos"
        }
    }
)
