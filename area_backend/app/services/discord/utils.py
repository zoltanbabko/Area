import requests
import os

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")


def get_discord_channels(user_access_token):
    if not user_access_token or not BOT_TOKEN:
        return []

    headers_bot = {"Authorization": f"Bot {BOT_TOKEN}"}
    headers_user = {"Authorization": f"Bearer {user_access_token}"}

    bot_guilds_resp = requests.get("https://discord.com/api/users/@me/guilds", headers=headers_bot)
    if bot_guilds_resp.status_code != 200:
        print(f"Error fetching bot guilds: {bot_guilds_resp.text}")
        return []

    bot_guilds_map = {g["id"]: g for g in bot_guilds_resp.json()}

    user_guilds_resp = requests.get("https://discord.com/api/users/@me/guilds", headers=headers_user)
    if user_guilds_resp.status_code != 200:
        return []

    user_guilds = user_guilds_resp.json()

    options = []

    for u_guild in user_guilds:
        if u_guild["id"] not in bot_guilds_map:
            continue

        url_channels = f"https://discord.com/api/guilds/{u_guild['id']}/channels"
        c_resp = requests.get(url_channels, headers=headers_bot)

        if c_resp.status_code == 200:
            channels = c_resp.json()
            channels.sort(key=lambda x: x.get('position', 0))
            for c in channels:
                if c["type"] == 0:
                    options.append({
                        "label": f"[{u_guild['name']}] #{c['name']}",
                        "value": c["id"]
                    })
    return options
