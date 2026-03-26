import requests

from app.core.registry import register_reaction

from .utils import slack_headers


@register_reaction(
    service="slack",
    key="post_message",
    name="Post message",
    description="Posts a message to a Slack channel.",
    args={
        "channel_id": {"type": "string", "description": "Target Slack channel ID (e.g. C0123...)."},
        "text": {"type": "string", "description": "Message text."},
    },
    requires_auth=True,
)
def post_message(access_token: str, channel_id: str, text: str, **kwargs):
    url = "https://slack.com/api/chat.postMessage"
    r = requests.post(
        url,
        headers=slack_headers(access_token),
        json={"channel": channel_id, "text": text},
        timeout=10,
    )
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"Slack API error: {data}")
    return {
        "channel": channel_id,
        "ts": data.get("ts"),
        "message": data.get("message"),
    }
