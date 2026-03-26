from fastapi import APIRouter, Request
from app.core.registry import ACTIONS, REACTIONS
import time

router = APIRouter()


@router.get("/about.json")
def about(request: Request):
    services = {}

    for a in ACTIONS.values():
        services.setdefault(a["service"], {"actions": [], "reactions": []})
        services[a["service"]]["actions"].append({
            "name": a["name"],
            "description": a["description"]
        })

    for r in REACTIONS.values():
        services.setdefault(r["service"], {"actions": [], "reactions": []})
        services[r["service"]]["reactions"].append({
            "name": r["name"],
            "description": r["description"]
        })

    return {
        "client": {"host": request.client.host},
        "server": {
            "current_time": int(time.time()),
            "services": [
                {"name": k, **v} for k, v in services.items()
            ]
        }
    }
