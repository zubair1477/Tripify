import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Required scopes
SPOTIFY_SCOPES = (
    "playlist-modify-public "
    "playlist-modify-private "
    "user-read-email "
    "user-read-private"
)


def get_spotify_auth_url():
    """Generate Spotify authorization URL"""
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPES,
        show_dialog=True
    )
    return sp_oauth.get_authorize_url()


def exchange_code_for_token(code: str):
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPES
    )
    return sp_oauth.get_access_token(code, as_dict=True)


def get_spotify_client(access_token: str):
    """Get authenticated Spotify client"""
    return spotipy.Spotify(auth=access_token)


# -------------------------------------------------------------
# VALID SPOTIFY GENRES
# -------------------------------------------------------------
MOOD_GENRES = {
    "energetic": ["dance", "edm", "party", "power-pop"],
    "calm": ["chill", "acoustic", "ambient", "piano"],
    "introspective": ["focus", "study", "sleep", "indie-pop"],
    "adventurous": ["alternative", "indie", "world-music", "latin"],
}

# -------------------------------------------------------------
# GET RECOMMENDATIONS
# -------------------------------------------------------------
def get_recommendations(sp, mood: str, limit: int = 20):
    """Get track recommendations using 1 seed artist (Spotipy-safe)."""

    MOOD_ARTISTS = {
        "energetic": "4NHQUGzhtTLFvgF5SZesLK",       # Dua Lipa
        "calm": "6Q192DXotxtaysaqNPy5yR",            # Norah Jones
        "introspective": "7oPftvlwr6VrsViSDV7fJY",   # Radiohead
        "adventurous": "3WrFJ7ztbogyGnTHbHJFl2",     # The Beatles
    }

    mood = mood.lower()

    seed_artist = MOOD_ARTISTS.get(mood, "4NHQUGzhtTLFvgF5SZesLK")

    try:
        recs = sp.recommendations(
            seed_artists=[seed_artist],   # ⭐ ONLY ONE SEED
            limit=limit,
            market="US"
        )
    except Exception as e:
        print("Spotify recommendation error:", e)
        return []

    tracks = []
    for t in recs.get("tracks", []):
        tracks.append({
            "id": t["id"],
            "name": t["name"],
            "artists": [a["name"] for a in t["artists"]],
            "duration": round(t["duration_ms"] / 60000, 2),
            "preview_url": t.get("preview_url"),
            "uri": t["uri"],
            "image": t["album"]["images"][0]["url"]
            if t["album"]["images"] else None
        })

    return tracks




# -------------------------------------------------------------
# CREATE PLAYLIST
# -------------------------------------------------------------
def create_playlist(sp, user_id: str, mood: str, tracks: list):
    """Create playlist inside user's Spotify account"""

    user = sp.current_user()
    sp_user_id = user["id"]

    playlist_name = f"Tripify – {mood.capitalize()} Mix"
    playlist_description = f"A playlist generated based on your {mood} mood from Tripify."

    playlist = sp.user_playlist_create(
        user=sp_user_id,
        name=playlist_name,
        public=True,
        description=playlist_description
    )

    track_uris = [track["uri"] for track in tracks if track.get("uri")]

    if track_uris:
        sp.playlist_add_items(playlist["id"], track_uris)

    return {
        "playlist_id": playlist["id"],
        "playlist_name": playlist_name,
        "playlist_url": playlist["external_urls"]["spotify"],
        "tracks_added": len(track_uris)
    }

