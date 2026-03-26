import requests
import datetime
from app.core.registry import register_action

def check_upcoming_event(params):
    now = datetime.datetime.utcnow()
    time_min = now.isoformat() + 'Z'
    
    url = f"https://www.googleapis.com/calendar/v3/calendars/primary/events"
    headers = {"Authorization": f"Bearer {params['access_token']}"}
    
    query_params = {
        "timeMin": time_min,
        "maxResults": 1,
        "orderBy": "startTime",
        "singleEvents": True
    }

    resp = requests.get(url, headers=headers, params=query_params)
    if resp.status_code != 200:
        return None

    items = resp.json().get("items", [])
    if not items:
        return None

    event = items[0]
    event_id = event["id"]

    if params.get("last_event_id") == event_id:
        return None

    start_str = event["start"].get("dateTime") or event["start"].get("date")
    if not start_str: return None

    params["last_event_id"] = event_id

    return {
        "summary": event.get("summary", "No Title"),
        "start": start_str,
        "link": event.get("htmlLink")
    }


register_action(
    "google_calendar",
    "upcoming_event",
    "Next event starting soon",
    check_upcoming_event
)
