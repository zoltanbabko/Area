import requests
import os
from app.core.registry import register_action

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def _get_weather_data(city):
    if not API_KEY:
        return None
    try:
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
        resp = requests.get(url)
        if resp.status_code != 200:
            return None
        return resp.json()
    except Exception:
        return None


def check_temperature(params):
    city = params.get("city")
    operator = params.get("operator", "gt")
    target_temp = float(params.get("temperature", 20))

    data = _get_weather_data(city)
    if not data:
        return None

    current_temp = data["main"]["temp"]

    triggered = False
    if operator == "gt" and current_temp > target_temp:
        triggered = True
    elif operator == "lt" and current_temp < target_temp:
        triggered = True
    elif operator == "eq" and abs(current_temp - target_temp) < 0.5:
        triggered = True

    if not triggered:
        return None

    return {
        "temp": current_temp,
        "city": data["name"],
        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"]
    }


def check_condition(params):
    city = params.get("city")
    target_condition = params.get("condition", "Rain")

    data = _get_weather_data(city)
    if not data:
        return None

    current_condition = data["weather"][0]["main"]
    if current_condition.lower() != target_condition.lower():
        return None

    return {
        "city": data["name"],
        "condition": current_condition,
        "temp": data["main"]["temp"]
    }


register_action(
    "openweather",
    "check_temp",
    "Monitor Temperature",
    check_temperature,
    args={
        "city": {"type": "text", "label": "City Name (ex: Paris)"},
        "operator": {
            "type": "select",
            "label": "Operator",
            "dynamic_source": "get_operators"
        },
        "temperature": {"type": "number", "label": "Target Temperature (°C)", "default": 20}
    }
)


register_action(
    "openweather",
    "check_condition",
    "Monitor Weather Condition",
    check_condition,
    args={
        "city": {"type": "text", "label": "City Name (ex: Tokyo)"},
        "condition": {
            "type": "select",
            "label": "Condition",
            "dynamic_source": "get_weather_conditions"
        }
    }
)
