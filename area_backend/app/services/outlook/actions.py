import requests
from app.core.registry import register_action


def check_new_email(params):
    url = "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages?$filter=isRead eq false&$top=1"
    headers = {"Authorization": f"Bearer {params['access_token']}"}

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return None

    data = resp.json()
    if not data.get("value"):
        return None

    email = data["value"][0]
    email_id = email["id"]

    if params.get("last_email_id") == email_id:
        return None

    params["last_email_id"] = email_id

    return {
        "subject": email["subject"],
        "from": email["from"]["emailAddress"]["name"],
        "body_preview": email["bodyPreview"]
    }


register_action("outlook", "new_email", "New unread email", check_new_email)
