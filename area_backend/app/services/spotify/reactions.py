import requests

from app.core.registry import register_reaction

from .utils import spotify_headers


@register_reaction(
    service="spotify",
    key="add_track_to_playlist",
    name="Add track to playlist",
    description="Adds a track to a Spotify playlist.",
    args={
        "playlist_id": {"type": "string", "description": "Target playlist id"},
        "track_uri": {"type": "string", "description": "Spotify track URI (e.g. spotify:track:...)"},
    },
    requires_auth=True,
)
def add_track_to_playlist(access_token: str, args: dict, payload: dict) -> dict:
    playlist_id = args.get("playlist_id")
    track_uri = args.get("track_uri") or payload.get("track_uri")
    if not playlist_id or not track_uri:
        return {"ok": False, "error": "Missing playlist_id or track_uri"}

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    r = requests.post(
        url,
        headers=spotify_headers(access_token),
        json={"uris": [track_uri]},
        timeout=10,
    )
    if r.status_code >= 400:
        return {"ok": False, "error": r.text, "status": r.status_code}

    data = r.json() if r.content else {}
    return {"ok": True, "snapshot_id": data.get("snapshot_id")}
