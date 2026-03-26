import requests
import os
from app.core.registry import register_reaction

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")


def post_message(params):
    channel_id = params.get("channel_id")
    content = params.get("message")

    if not channel_id or not content or not BOT_TOKEN:
        return

    url = f"https://discord.com/api/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    requests.post(url, headers=headers, json={"content": content})

def post_embed(params):
    channel_id = params.get("channel_id")
    title = params.get("title", "Notification")
    description = params.get("description", "")
    color_hex = params.get("color", "#00ff00") # Vert par défaut
    
    # Conversion hex -> int pour Discord
    try:
        color_int = int(color_hex.replace("#", ""), 16)
    except:
        color_int = 65280

    if not channel_id or not os.getenv("DISCORD_BOT_TOKEN"):
        return

    url = f"https://discord.com/api/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {os.getenv('DISCORD_BOT_TOKEN')}",
        "Content-Type": "application/json"
    }

    payload = {
        "embeds": [{
            "title": title,
            "description": description,
            "color": color_int
        }]
    }

    requests.post(url, headers=headers, json=payload)


register_reaction(
    "discord",
    "post_message",
    "Post a message to channel",
    post_message,
    args={
        "channel_id": {
            "type": "select",
            "label": "Select Channel",
            "dynamic_source": "get_discord_channels"
        },
        "message": {
            "type": "long_text",
            "label": "Message Content",
        }
    }
)

register_reaction(
    "discord",
    "post_embed",
    "Post a Rich Embed message",
    post_embed,
    args={
        "channel_id": {
            "type": "select",
            "label": "Channel",
            "dynamic_source": "get_discord_channels"
        },
        "title": {"type": "text", "label": "Embed Title"},
        "description": {"type": "long_text", "label": "Embed Content"},
        "color": {"type": "text", "label": "Color Hex (ex: #ff0000)", "default": "#7289da"}
    }
)
