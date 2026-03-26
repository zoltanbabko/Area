from app.core.registry import register_action

from .utils import slack_get


@register_action(
    service="slack",
    key="new_message_in_channel",
    name="New message in channel",
    description="Triggers when a new message appears in a Slack channel.",
    args={
        "channel_id": {
            "type": "string",
            "description": "Slack channel ID (e.g. C012AB3CD).",
        }
    },
    requires_auth=True,
    polling=True,
)
def new_message_in_channel(access_token: str, params: dict):
    """Polls Slack channel history and triggers on a new latest message."""
    channel_id = params.get("channel_id")
    if not channel_id:
        return None

    data = slack_get(
        access_token,
        "https://slack.com/api/conversations.history",
        params={"channel": channel_id, "limit": 1},
    )
    msgs = data.get("messages", []) or []
    if not msgs:
        return None

    msg = msgs[0]
    ts = msg.get("ts")
    if not ts:
        return None

    last_ts = params.get("_last_ts")
    if last_ts == ts:
        return None

    params["_last_ts"] = ts
    return {
        "channel_id": channel_id,
        "user": msg.get("user"),
        "text": msg.get("text"),
        "ts": ts,
    }
