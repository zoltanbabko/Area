import requests
from app.core.registry import register_reaction


def create_text_file(params):
    name = params.get("name", "log.txt")
    content = params.get("content", "Hello AREA")

    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{name}:/content"
    headers = {
        "Authorization": f"Bearer {params['access_token']}",
        "Content-Type": "text/plain"
    }

    requests.put(url, headers=headers, data=content)


register_reaction("onedrive", "create_file", "Create a text file", create_text_file, args={
    "name": {"type": "text", "label": "File Name (ex: log.txt)"},
    "content": {"type": "long_text", "label": "File Content"}
})
