import requests
from app.core.registry import register_action


def check_unread_emails(params):
    url = "https://gmail.googleapis.com/gmail/v1/users/me/messages?q=is:unread&maxResults=1"
    headers = {"Authorization": f"Bearer {params['access_token']}"}

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return None

    data = resp.json()
    if "messages" not in data:
        return None

    latest_msg = data["messages"][0]
    msg_id = latest_msg["id"]

    if params.get("last_email_id") == msg_id:
        return None

    params["last_email_id"] = msg_id

    detail_url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}"
    detail_resp = requests.get(detail_url, headers=headers)
    if detail_resp.status_code != 200:
        return None

    detail_json = detail_resp.json()
    headers_list = detail_json.get("payload", {}).get("headers", [])

    subject = next((h["value"] for h in headers_list if h["name"] == "Subject"), "No Subject")
    sender = next((h["value"] for h in headers_list if h["name"] == "From"), "Unknown")
    snippet = detail_json.get("snippet", "")

    return {
        "subject": subject,
        "from": sender,
        "snippet": snippet
    }


register_action("gmail", "check_unread", "New unread email received", check_unread_emails)
