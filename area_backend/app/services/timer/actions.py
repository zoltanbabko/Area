import time
from app.core.registry import register_action


def _check_interval(params, interval_seconds):
    now = time.time()
    last_run = params.get("last_run", 0)

    if last_run == 0:
        params["last_run"] = now
        return {
            "timestamp": now,
            "message": "First run triggered immediately"
        }

    if now - last_run >= interval_seconds:
        params["last_run"] = now
        return {
            "timestamp": now,
            "message": f"Triggered after {interval_seconds} seconds"
        }

    return None


def every_minute(params):
    return _check_interval(params, 60)


def every_hour(params):
    return _check_interval(params, 3600)


def every_day(params):
    return _check_interval(params, 86400)


def every_month(params):
    return _check_interval(params, 2592000)


def custom_interval(params):
    interval = int(params.get("interval", 60))
    if interval < 10:
        interval = 10
    return _check_interval(params, interval)


register_action(
    service="timer",
    name="every_minute",
    description="Triggered every minute",
    handler=every_minute,
    args={}
)


register_action(
    service="timer",
    name="every_hour",
    description="Triggered every hour",
    handler=every_hour,
    args={}
)


register_action(
    service="timer",
    name="every_day",
    description="Triggered every day",
    handler=every_day,
    args={}
)


register_action(
    service="timer",
    name="every_month",
    description="Triggered every month (30 days)",
    handler=every_month,
    args={}
)


register_action(
    service="timer",
    name="custom_interval",
    description="Triggered every X seconds (custom)",
    handler=custom_interval,
    args={
        "interval": {
            "type": "number",
            "label": "Interval (seconds)",
            "default": 60
        }
    }
)
