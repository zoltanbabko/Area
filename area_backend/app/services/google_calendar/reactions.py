import requests
import datetime
from app.core.registry import register_reaction

def create_quick_event(params):
    summary = params.get("summary", "New Event")
    description = params.get("description", "Created via AREA")

    start_dt = datetime.datetime.utcnow()
    end_dt = start_dt + datetime.timedelta(hours=1)

    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    headers = {
        "Authorization": f"Bearer {params['access_token']}",
        "Content-Type": "application/json"
    }

    payload = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_dt.isoformat() + "Z"},
        "end": {"dateTime": end_dt.isoformat() + "Z"}
    }

    requests.post(url, headers=headers, json=payload)


register_reaction(
    "google_calendar",
    "create_event",
    "Create a 1h event now",
    create_quick_event,
    args={
        "summary": {"type": "text", "label": "Event Title"},
        "description": {"type": "long_text", "label": "Description"}
    }
)
