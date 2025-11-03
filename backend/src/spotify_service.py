import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Scopes needed for creating playlists
SPOTIFY_SCOPES = "playlist-modify-public playlist-modify-private user-library-read"


def get_spotify_auth_url():
    """Generate Spotify authorization URL"""
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPES,
        show_dialog=True
    )
    auth_url = sp_oauth.get_authorize_url()
    return auth_url


def get_spotify_client(access_token: str):
    """Get authenticated Spotify client"""
    return spotipy.Spotify(auth=access_token)


def exchange_code_for_token(code: str):
    """Exchange authorization code for access token"""
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPES
    )
    token_info = sp_oauth.get_access_token(code, as_dict=True)
    return token_info


def search_tracks_by_mood(mood: str, limit: int = 20):
    """
    Search for tracks based on mood

    Mood to genre/audio features mapping:
    - energetic: high energy, fast tempo, danceable
    - calm: low energy, slow tempo, acoustic
    - introspective: medium energy, emotional, indie/alternative
    - adventurous: diverse genres, upbeat, world music
    """
    mood_to_search = {
        "energetic": {
            "genres": ["pop", "dance", "electronic", "rock"],
            "energy_min": 0.7,
            "tempo_min": 120,
            "valence_min": 0.6
        },
        "calm": {
            "genres": ["ambient", "acoustic", "chill", "lo-fi"],
            "energy_max": 0.5,
            "tempo_max": 100,
            "valence_min": 0.3
        },
        "introspective": {
            "genres": ["indie", "alternative", "folk", "singer-songwriter"],
            "energy_min": 0.3,
            "energy_max": 0.7,
            "valence_max": 0.6
        },
        "adventurous": {
            "genres": ["world", "latin", "afrobeat", "reggae"],
            "energy_min": 0.6,
            "tempo_min": 100
        }
    }

    return mood_to_search.get(mood.lower(), mood_to_search["energetic"])


def get_recommendations(sp, mood: str, limit: int = 20):
    """Get track recommendations based on mood"""
    mood_config = search_tracks_by_mood(mood)

    # Get seed tracks from popular playlists of the genres
    seed_genres = mood_config["genres"][:5]  # Spotify allows max 5 seed genres

    # Build recommendation parameters
    recommendations_params = {
        "seed_genres": seed_genres,
        "limit": limit,
        "market": "US"
    }

    # Add audio features based on mood
    if "energy_min" in mood_config:
        recommendations_params["min_energy"] = mood_config["energy_min"]
    if "energy_max" in mood_config:
        recommendations_params["max_energy"] = mood_config["energy_max"]
    if "tempo_min" in mood_config:
        recommendations_params["min_tempo"] = mood_config["tempo_min"]
    if "tempo_max" in mood_config:
        recommendations_params["max_tempo"] = mood_config["tempo_max"]
    if "valence_min" in mood_config:
        recommendations_params["min_valence"] = mood_config["valence_min"]
    if "valence_max" in mood_config:
        recommendations_params["max_valence"] = mood_config["valence_max"]

    # Get recommendations
    recommendations = sp.recommendations(**recommendations_params)

    tracks = []
    for track in recommendations['tracks']:
        tracks.append({
            "id": track['id'],
            "name": track['name'],
            "artist": ", ".join([artist['name'] for artist in track['artists']]),
            "uri": track['uri'],
            "duration_ms": track['duration_ms'],
            "preview_url": track.get('preview_url'),
            "album_image": track['album']['images'][0]['url'] if track['album']['images'] else None
        })

    return tracks


def create_playlist(sp, user_id: str, mood: str, tracks: list):
    """Create a playlist on user's Spotify account"""
    # Get current user info
    current_user = sp.current_user()
    spotify_user_id = current_user['id']

    # Create playlist
    playlist_name = f"Tripify - Your {mood.capitalize()} Vibe"
    playlist_description = f"A personalized {mood} playlist created by Tripify based on your mood quiz"

    playlist = sp.user_playlist_create(
        user=spotify_user_id,
        name=playlist_name,
        public=True,
        description=playlist_description
    )

    # Add tracks to playlist
    track_uris = [track['uri'] for track in tracks if 'uri' in track]
    if track_uris:
        sp.playlist_add_items(playlist['id'], track_uris)

    return {
        "playlist_id": playlist['id'],
        "playlist_name": playlist_name,
        "playlist_url": playlist['external_urls']['spotify'],
        "tracks_added": len(track_uris)
    }
