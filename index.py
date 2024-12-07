import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Spotify Developer credentials (loaded from environment variables)
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Playlist ID
PLAYLIST_ID = "24kH4QpTd1ha5AyiWR3rOs"

# Spotify API Scopes
SCOPE = "playlist-read-private user-library-modify"

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))


def fetch_all_tracks_in_order(playlist_id):
    """Fetch all tracks from the playlist in the exact order."""
    print("Fetching all tracks from the playlist...")
    offset = 0
    limit = 100
    all_tracks = []

    while True:
        results = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
        tracks = results['items']

        if not tracks:
            break

        all_tracks.extend(tracks)
        offset += limit

    print(f"Total tracks fetched: {len(all_tracks)}")
    return all_tracks


def like_tracks_in_exact_order(tracks):
    """Like tracks in the exact order they are fetched."""
    print("Liking tracks in playlist order...")
    total_liked = 0

    for idx, item in enumerate(tracks):
        track = item['track']
        track_id = track['id']
        track_name = track['name']
        artist_name = track['artists'][0]['name']

        try:
            # Like the track
            sp.current_user_saved_tracks_add([track_id])
            print(f"{idx + 1}. Liked: {track_name} by {artist_name}")
            total_liked += 1

            # Introduce a delay to ensure sequential processing
            time.sleep(0.5)  # Increase delay to avoid API rate issues
        except Exception as e:
            print(f"Error liking track {idx + 1}: {track_name} by {artist_name}. Retrying...")
            try:
                sp.current_user_saved_tracks_add([track_id])
                print(f"Retry successful for {idx + 1}: {track_name} by {artist_name}")
                total_liked += 1
            except Exception as retry_e:
                print(f"Failed to like track {idx + 1}: {track_name}. Skipping. Error: {retry_e}")

    print(f"Total liked songs: {total_liked}")


if __name__ == "__main__":
    # Step 1: Fetch all tracks in playlist order
    tracks = fetch_all_tracks_in_order(PLAYLIST_ID)

    # Step 2: Like tracks in the exact order
    like_tracks_in_exact_order(tracks)
