from app.core.registry import register_action

from .utils import encode_project_id, gitlab_get


@register_action(
    service="gitlab",
    key="new_issue_in_project",
    name="New issue in project",
    description="Triggers when a new issue is created in a GitLab project (polling).",
    args={
        "base_url": {
            "type": "string",
            "description": "GitLab base URL (e.g. https://gitlab.com)"
        },
        "project_id": {
            "type": "string",
            "description": "Numeric project id or path like group/name"
        },
    },
    requires_auth=True,
    polling=True,
)
def new_issue_in_project(access_token: str, args: dict, params: dict):
    base_url = args.get("base_url", "https://gitlab.com")
    project_id = args.get("project_id")
    if not project_id:
        return None

    try:
        issues = gitlab_get(
            access_token,
            base_url,
            f"api/v4/projects/{encode_project_id(project_id)}/issues",
            params={"per_page": 1, "order_by": "created_at", "sort": "desc"},
        )
    except Exception:
        return None

    if not issues:
        return None

    latest = issues[0]
    latest_id = str(latest.get("id"))
    prev = params.get("last_issue_id")

    params["last_issue_id"] = latest_id
    if prev and prev != latest_id:
        return {
            "id": latest.get("id"),
            "iid": latest.get("iid"),
            "title": latest.get("title"),
            "web_url": latest.get("web_url"),
        }
    return None
