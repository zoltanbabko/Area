import requests
from app.core.registry import register_reaction


def create_issue(params):
    repo = params.get("repository")
    title = params.get("title", "Issue créée via AREA")
    body = params.get("body", "Description automatique.")

    if not repo:
        return

    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"Bearer {params['access_token']}",
        "Accept": "application/vnd.github.v3+json"
    }

    payload = {"title": title, "body": body}
    requests.post(url, headers=headers, json=payload)


register_reaction(
    "github",
    "create_issue",
    "Create a new Issue",
    create_issue,
    args={
        "repository": {
            "type": "select",
            "label": "Repository",
            "dynamic_source": "get_user_repos"
        },
        "title": {"type": "text", "label": "Issue Title"},
        "body": {"type": "long_text", "label": "Issue Description"}
    }
)
