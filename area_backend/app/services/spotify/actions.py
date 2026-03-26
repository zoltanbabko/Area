from app.core.registry import register_action

from .utils import spotify_get


@register_action(
    service="spotify",
    key="new_saved_track",
    name="New saved track",
    description="Triggers when the user saves a new track (Liked Songs).",
    args={},
    requires_auth=True,
    polling=True,
)
def new_saved_track(access_token: str, args: dict, state: dict) -> dict | None:
    """Poll Spotify for the latest saved track.

    State keys:
      - last_track_id: str
    """
    data = spotify_get(
        access_token,
        "https://api.spotify.com/v1/me/tracks",
        params={"limit": 1},
    )
    items = data.get("items", [])
    if not items:
        return None

    track = (items[0] or {}).get("track") or {}
    track_id = track.get("id")
    if not track_id:
        return None

    last = state.get("last_track_id")
    if last is None:
        state["last_track_id"] = track_id
        return None

    if track_id == last:
        return None

    state["last_track_id"] = track_id
    return {
        "track_id": track_id,
        "track_name": track.get("name"),
        "track_uri": track.get("uri"),
        "artist": ((track.get("artists") or [{}])[0] or {}).get("name"),
        "album": (track.get("album") or {}).get("name"),
        "saved_at": (items[0] or {}).get("added_at"),
        "external_url": (track.get("external_urls") or {}).get("spotify"),
    }
