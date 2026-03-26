ACTIONS = {}
REACTIONS = {}


def register_action(service, name, description, handler, args=None):
    args_conf = args or {}

    ACTIONS[f"{service}.{name}"] = {
        "service": service,
        "name": name,
        "description": description,
        "handler": handler,
        "args": args_conf
    }


def register_reaction(service, name, description, handler, args=None):
    args_conf = args or {}

    REACTIONS[f"{service}.{name}"] = {
        "service": service,
        "name": name,
        "description": description,
        "handler": handler,
        "args": args_conf
    }
