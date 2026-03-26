# area_backend/app/services/google_sheets/reactions.py
import requests
import json
from app.core.registry import register_reaction

def insert_row(params):
    spreadsheet_id = params.get("spreadsheet_id")
    raw_values = params.get("values", "") 
    
    if not spreadsheet_id: 
        return

    values_list = [v.strip() for v in raw_values.split(",")]

    range_name = "A1"
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_name}:append"

    headers = {
        "Authorization": f"Bearer {params['access_token']}",
        "Content-Type": "application/json"
    }

    query_params = {
        "valueInputOption": "USER_ENTERED"
    }

    payload = {
        "range": range_name,
        "majorDimension": "ROWS",
        "values": [values_list]
    }

    requests.post(url, headers=headers, params=query_params, json=payload)


register_reaction(
    "google_sheets",
    "insert_row",
    "Insert row in Sheet",
    insert_row,
    args={
        "spreadsheet_id": {
            "type": "text",
            "label": "Spreadsheet ID (from URL)"
        },
        "values": {
            "type": "text",
            "label": "Values (comma separated)",
            "default": "{{author}}, {{subject}}, {{date}}"
        }
    }
)
