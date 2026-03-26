import requests

from app.core.registry import register_reaction

from .utils import encode_project_id, gitlab_headers, gitlab_url


@register_reaction(
    service="gitlab",
    key="create_issue",
    name="Create issue",
    description="Creates an issue in a GitLab project.",
    args={
        "base_url": {
            "type": "string",
            "description": "GitLab base URL, e.g. https://gitlab.com",
        },
        "project_id": {"type": "string", "description": "Project numeric ID or URL-encoded path (group%2Fproject)."},
        "title": {"type": "string", "description": "Issue title."},
        "description": {"type": "string", "description": "Issue description (optional).", "optional": True},
    },
    requires_auth=True,
)
def create_issue(access_token: str, args: dict, params: dict):
    base_url = (args.get("base_url") or "https://gitlab.com").strip()
    project_id = args.get("project_id")
    title = args.get("title")
    if not project_id or not title:
        return False

    url = gitlab_url(base_url, f"api/v4/projects/{encode_project_id(project_id)}/issues")
    payload = {"title": title}
    if args.get("description"):
        payload["description"] = args["description"]

    r = requests.post(url, headers=gitlab_headers(access_token), data=payload, timeout=10)
    return r.status_code in (200, 201)
