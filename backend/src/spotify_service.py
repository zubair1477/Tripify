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
    "user-read-private "
    "user-top-read"
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
# VALID SPOTIFY GENRES AND MOOD PARAMETERS
# -------------------------------------------------------------
MOOD_GENRES = {
    "energetic": ["dance", "edm", "party", "power-pop"],
    "calm": ["chill", "acoustic", "ambient", "piano"],
    "introspective": ["focus", "study", "sleep", "indie-pop"],
    "adventurous": ["alternative", "indie", "world-music", "latin"],
}

# Audio features based on mood
MOOD_AUDIO_FEATURES = {
    "energetic": {
        "target_energy": 0.8,
        "min_tempo": 120,
        "target_valence": 0.7,
    },
    "calm": {
        "target_energy": 0.3,
        "max_tempo": 100,
        "target_valence": 0.5,
    },
    "introspective": {
        "target_energy": 0.4,
        "max_tempo": 110,
        "min_valence": 0.2,
        "max_valence": 0.6,
    },
    "adventurous": {
        "target_energy": 0.6,
        "min_tempo": 100,
        "target_valence": 0.6,
    },
}

# -------------------------------------------------------------
# GET RECOMMENDATIONS
# -------------------------------------------------------------
def get_recommendations(sp, mood: str, limit: int = 20):
    """
    Get personalized playlist based on mood using user's top tracks.

    NOTE: Spotify deprecated the /recommendations and restricted /audio-features endpoints
    in Nov 2024 for new apps. This function now creates playlists directly from user's
    top tracks based on the selected time range that best matches the mood.
    """

    mood = mood.lower()

    print(f"\n=== Creating '{mood}' playlist from user's favorite tracks ===")

    # Map moods to time ranges for variety
    # - Energetic: Recent tracks (user's current energy)
    # - Calm: Long-term favorites (comfort/familiarity)
    # - Introspective: Medium-term (reflective period)
    # - Adventurous: Mix of short and long-term

    mood_time_ranges = {
        "energetic": "short_term",      # Last ~4 weeks
        "calm": "long_term",             # All-time favorites
        "introspective": "medium_term",  # Last ~6 months
        "adventurous": "short_term",     # Recent discoveries
    }

    time_range = mood_time_ranges.get(mood, "medium_term")

    # Fetch more tracks than we need to ensure variety
    fetch_limit = min(limit * 2, 50)  # Spotify max is 50

    try:
        print(f"Fetching top {fetch_limit} tracks from {time_range} listening history...")
        response = sp.current_user_top_tracks(limit=fetch_limit, time_range=time_range)
        tracks_data = response.get("items", [])
        print(f"✓ Found {len(tracks_data)} tracks")
    except Exception as e:
        print(f"✗ Error fetching tracks: {e}")
        # Fallback to medium-term if primary fails
        try:
            print("Trying fallback to medium-term...")
            response = sp.current_user_top_tracks(limit=fetch_limit, time_range="medium_term")
            tracks_data = response.get("items", [])
            print(f"✓ Fallback successful! Found {len(tracks_data)} tracks")
        except Exception as fallback_error:
            print(f"✗ Fallback failed: {fallback_error}")
            return []

    if not tracks_data:
        print("✗ No tracks found in user's listening history")
        return []

    # Add some variety based on mood
    # For adventurous mood, also mix in some long-term favorites
    if mood == "adventurous" and len(tracks_data) < limit:
        try:
            print("Adding variety from long-term favorites...")
            long_term_response = sp.current_user_top_tracks(limit=20, time_range="long_term")
            long_term_tracks = long_term_response.get("items", [])

            # Add tracks that aren't already in the list
            existing_ids = {t["id"] for t in tracks_data}
            for track in long_term_tracks:
                if track["id"] not in existing_ids:
                    tracks_data.append(track)
                    existing_ids.add(track["id"])

            print(f"✓ Added variety tracks. Total: {len(tracks_data)}")
        except Exception as e:
            print(f"Note: Could not add variety tracks: {e}")

    # Shuffle for variety (deterministic based on mood)
    import random
    random.seed(hash(mood))  # Same mood = same shuffle order for consistency
    shuffled = tracks_data.copy()
    random.shuffle(shuffled)

    # Select the requested number of tracks
    selected = shuffled[:limit]

    # Format tracks
    tracks = []
    for t in selected:
        tracks.append({
            "id": t["id"],
            "name": t["name"],
            "artists": [a["name"] for a in t["artists"]],
            "duration": round(t["duration_ms"] / 60000, 2),
            "preview_url": t.get("preview_url"),
            "uri": t["uri"],
            "image": t["album"]["images"][0]["url"] if t["album"]["images"] else None
        })

    print(f"✓ Created playlist with {len(tracks)} tracks for '{mood}' mood\n")
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

