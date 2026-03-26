# How to Contribute to AREA

Welcome to the AREA project! We are thrilled that you want to contribute. This document aims to guide you through the process of extending the platform, specifically how to add new Services, Actions, and REActions.

Our architecture is designed to be modular: the Frontend and Mobile clients dynamically generate forms based on the Backend configuration. This means 90% of your contributions will happen in the Backend.

---

## 📂 Project Structure

Before starting, familiarize yourself with the service structure in the backend:

```
area_backend/
├── app/
│   ├── api/             # API Routes & OAuth endpoints
│   ├── core/            # Core logic (registry, scheduler, hooks)
│   ├── models/          # Database models
│   ├── services/        # <--- YOUR PLAYGROUND
│   │   ├── google/
│   │   ├── discord/
│   │   └── [new_service]/
│   │       ├── __init__.py
│   │       ├── actions.py
│   │       ├── reactions.py
│   │       └── utils.py
│   └── main.py          # Entry point where services are loaded
```

---

## 🚀 Adding a New Service

To add a new service (e.g., Reddit), follow these steps:

### 1. Create the Directory

Create a new folder in area_backend/app/services/reddit/.

Inside, create empty files: __init__.py, actions.py, reactions.py, utils.py (if needed).

### 2. Implement an Action (Trigger)

Open actions.py. You must use the @register_action decorator to register your function.

```python
# area_backend/app/services/reddit/actions.py

import requests
from app.core.registry import register_action

def check_new_post(params):
    
    # logic...
    
    return {
        "title": "New Post Title",
        "author": "User123",
        "url": "https://reddit.com/..."
    }

# Registration
register_action(
    service="reddit",
    name="new_post",
    description="Triggers when a new post is created in a subreddit",
    handler=check_new_post,
    args={
        "subreddit": {
            "type": "text",
            "label": "Subreddit Name (without r/)",
            "default": "python"
        }
    }
)
```

Argument Types `args`: The frontend generates forms automatically based on these types:
- `text`: Simple input.
- `long_text`: Textarea.
- `number`: Numeric input.
- `select`: Dropdown (requires dynamic_source).

### 3. Implement a REAction (Consequence)

Open reactions.py. Use the @register_reaction decorator.

```Python
# area_backend/app/services/reddit/reactions.py

from app.core.registry import register_reaction

def post_comment(params):
    access_token = params.get("access_token")
    post_id = params.get("post_id")
    content = params.get("content") # Can contain variables like {{ title }}
    
    # Logic to post comment via API...

register_reaction(
    service="reddit",
    name="post_comment",
    description="Post a comment on a thread",
    handler=post_comment,
    args={
        "post_id": {"type": "text", "label": "Target Post ID"},
        "content": {"type": "long_text", "label": "Comment Body"}
    }
)
```

### 4. Register the Service in main.py

This is the most critical step. If you don't import your new files in main.py, they won't be loaded into the registry.

Open area_backend/app/main.py and add:

```Python
# existing imports...
import app.services.reddit.actions
import app.services.reddit.reactions

# add to the liste to remove error coding style
# ...
```

To make your service fully functional, you must register it in the core engine and API logic.

### 5. Allow Execution without Token (If applicable)

If your service does not require OAuth2 (like timer or openweather), you must whitelist it in the Hook Engine to prevent the "Missing OAuth token" error.

Open `area_backend/app/core/hook_engine.py` and update the check in execute_area:

```python
# Look for this line:
elif action_def["service"] not in ["timer", "openweather", "YOUR_NEW_SERVICE"] and not token:
    print(f"[WARNING] Area {area.id}: Missing OAuth token for service '{action_def['service']}'")
    db.close()
    return
```

### 6. Register in Services API (services.py)

Open `area_backend/app/api/services.py` to configure how the Frontend interacts with your service.

#### A. Auth Provider Mapping

If your service uses OAuth2, add it to the AUTH_MAP in the services function. This tells the frontend which OAuth provider to call when clicking "Connect".

```python
# In function services():
AUTH_MAP = {
    "gmail": "google",
    # existing...
    "reddit": "reddit",  # <--- ADD YOUR NEW SERVICE
}
```

#### B. Dynamic Options (Select Fields)

If your actions/reactions use a "type": "select" argument with a dynamic_source, you must handle the call in get_field_options.

Import your utils at the top: import app.services.reddit.utils as reddit_utils

Add the logic in get_field_options:

```python
# In function get_field_options():

    # existing checks...

    if service_name == "reddit" and source_func_name == "get_subreddits":
        # Pass token only if required by your util function
        return reddit_utils.get_subreddits(token) 

    return []
```

## 🔐 Adding OAuth2 Authentication (Optional)

If your service requires OAuth2 (like Google or Discord):

Create a file area_backend/app/api/oauth/reddit.py.

Implement login (redirect to provider) and callback (exchange code for token) endpoints.

Use process_oauth_login from app.api.oauth.utils to save tokens.

Register the router in area_backend/app/main.py:

```Python
from app.api.oauth import reddit

api.include_router(reddit.router)
```

Frontend: The services page detects auth_provider automatically if the naming convention matches.

## 📝 Checklist

- Files created (actions.py, reactions.py, utils.py).
- Service imported in main.py.
- Token check updated in hook_engine.py (if public service).
- AUTH_MAP updated in api/services.py (if OAuth service).
- Field Options updated in api/services.py (if using dynamic selects).
- Don't forget to add your app secret and link your secret to docker-compose

## 🧪 Testing Your Changes

Restart the Backend:

```Bash
docker-compose restart server
```

Verify Registration: Go to http://localhost:8080/about.json. Your new service, actions, and reactions should appear in the JSON response.

Test the UI: Go to the Web Client (http://localhost:8081). The "Create AREA" page should automatically display your new service in the dropdowns without any frontend code changes!

## 📝 Coding Standards

Python: Follow PEP8 guidelines.

Error Handling: Never let an Action/Reaction crash the server. Use try/except blocks inside your handler functions.

Variables: When returning data from an Action, use clean keys (e.g., author instead of data_user_name) as these are displayed to the user for interpolation.

Happy Coding! 🚀