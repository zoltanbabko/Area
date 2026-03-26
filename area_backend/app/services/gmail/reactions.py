import requests
import base64
from email.mime.text import MIMEText
from app.core.registry import register_reaction


def send_email(params):
    to = params.get("to", "")
    subject = params.get("subject", "Notification AREA")
    body = params.get("body", "Hello from AREA")

    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    url = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"
    headers = {
        "Authorization": f"Bearer {params['access_token']}",
        "Content-Type": "application/json"
    }

    requests.post(url, headers=headers, json={"raw": raw_message})


register_reaction(
    "gmail",
    "send_email",
    "Send an email",
    send_email,
    args={
        "to": {"type": "text", "label": "Recipient Email"},
        "subject": {"type": "text", "label": "Subject"},
        "body": {"type": "long_text", "label": "Email Body"}
    }
)
