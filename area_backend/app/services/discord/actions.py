import requests
import os
from app.core.registry import register_action

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")


def check_new_message(params):
    channel_id = params.get("channel_id")
    if not channel_id or not BOT_TOKEN:
        return None

    url = f"https://discord.com/api/channels/{channel_id}/messages?limit=1"
    headers = {"Authorization": f"Bot {BOT_TOKEN}"}

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return None

    messages = resp.json()
    if not messages:
        return None

    last_msg = messages[0]
    msg_id = last_msg["id"]

    if params.get("last_message_id") == msg_id:
        return None

    params["last_message_id"] = msg_id

    if last_msg["author"].get("bot", False):
        return None

    return {
        "author": last_msg["author"]["username"],
        "content": last_msg["content"],
        "channel_id": last_msg["channel_id"]
    }


register_action(
    "discord",
    "new_message",
    "New message in channel",
    check_new_message,
    args={
        "channel_id": {
            "type": "select",
            "label": "Select Channel",
            "dynamic_source": "get_discord_channels"
        }
    }
)
