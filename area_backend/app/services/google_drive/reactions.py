import requests
import json
from app.core.registry import register_reaction


def create_text_file(params):
    file_name = params.get("file_name") or "Untitled.txt"
    content = params.get("content") or "(Empty content)"

    metadata = {
        "name": file_name,
        "mimeType": "text/plain"
    }

    files = {
        'data': ('metadata', json.dumps(metadata), 'application/json'),
        'file': ('file', content, 'text/plain')
    }

    url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
    headers = {"Authorization": f"Bearer {params['access_token']}"}

    requests.post(url, headers=headers, files=files)


register_reaction(
    "google_drive",
    "create_text_file",
    "Create a text file",
    create_text_file,
    args={
        "file_name": {"type": "text", "label": "File Name", "default": "From {{from}}.txt"},
        "content": {"type": "long_text", "label": "File Content", "default": "{{subject}}"}
    }
)
