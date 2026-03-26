import requests
from app.core.registry import register_reaction


def send_email(params):
    url = "https://graph.microsoft.com/v1.0/me/sendMail"
    headers = {"Authorization": f"Bearer {params['access_token']}", "Content-Type": "application/json"}

    payload = {
        "message": {
            "subject": params.get("subject", "No Subject"),
            "body": {
                "contentType": "Text",
                "content": params.get("body", "")
            },
            "toRecipients": [
                {"emailAddress": {"address": params.get("to")}}
            ]
        }
    }
    requests.post(url, headers=headers, json=payload)


register_reaction("outlook", "send_email", "Send an email", send_email, args={
    "to": {"type": "text", "label": "Recipient Email"},
    "subject": {"type": "text", "label": "Subject"},
    "body": {"type": "long_text", "label": "Message"}
})
