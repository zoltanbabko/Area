def get_weather_conditions(token=None):
    return [
        {"label": "Clear Sky ☀️", "value": "Clear"},
        {"label": "Clouds ☁️", "value": "Clouds"},
        {"label": "Rain 🌧️", "value": "Rain"},
        {"label": "Snow ❄️", "value": "Snow"},
        {"label": "Thunderstorm ⚡", "value": "Thunderstorm"},
        {"label": "Drizzle 💧", "value": "Drizzle"},
        {"label": "Mist/Fog 🌫️", "value": "Mist"}
    ]


def get_operators(token=None):
    return [
        {"label": "Greater than (>)", "value": "gt"},
        {"label": "Less than (<)", "value": "lt"},
        {"label": "Equal to (=)", "value": "eq"}
    ]
