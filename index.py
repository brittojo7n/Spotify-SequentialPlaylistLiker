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

# Playlist ID (replace with your playlist ID)
PLAYLIST_ID = "<playlist_id>"

# Spotify API Scopes
SCOPE = "playlist-read-private user-library-read user-library-modify"

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))


def fetch_all_tracks_in_order(playlist_id):
    """Fetch all tracks from the playlist in exact order."""
    print("Fetching all tracks from the playlist...")
    offset = 0
    limit = 100
    ordered_tracks = []

    while True:
        results = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
        tracks = results['items']

        if not tracks:
            break

        for idx, item in enumerate(tracks):
            track_name = item['track']['name']
            artist_name = item['track']['artists'][0]['name']
            track_id = item['track']['id']
            ordered_tracks.append((offset + idx, track_id, track_name, artist_name))

        offset += limit

    print(f"Total tracks fetched: {len(ordered_tracks)}")
    return ordered_tracks


def is_track_liked(track_id):
    """Check if a track is already liked."""
    try:
        return sp.current_user_saved_tracks_contains([track_id])[0]
    except Exception as e:
        print(f"Error checking if track is liked: {e}")
        return False


def like_track_with_confirmation(track_id, delay):
    """
    Attempt to like a track and confirm the operation by re-checking its liked status.
    Introduces a delay if the API response is slow.
    """
    retries = 2  # Reduced retries for faster processing

    for attempt in range(retries):
        try:
            sp.current_user_saved_tracks_add([track_id])
            time.sleep(delay)  # Wait for the API to process the request

            # Confirm if the track is now liked
            if is_track_liked(track_id):
                return True

            print(f"Attempt {attempt + 1}/{retries}: API response delay detected. Retrying...")
        except Exception as e:
            print(f"Error liking track: {e}")

    return False


def like_tracks_with_shorter_delays(tracks, delay):
    """Process tracks strictly in order, verifying API responses for each track."""
    print(f"Liking tracks with a delay of {delay} seconds between requests...")
    total_liked = 0

    for idx, (playlist_index, track_id, track_name, artist_name) in enumerate(tracks):
        print(f"Processing track {playlist_index + 1}: {track_name} by {artist_name}...")

        if is_track_liked(track_id):
            print(f"{playlist_index + 1}. Already liked: {track_name} by {artist_name}")
            continue

        # Attempt to like the track with confirmation
        if like_track_with_confirmation(track_id, delay):
            print(f"{playlist_index + 1}. Liked: {track_name} by {artist_name}")
            total_liked += 1
        else:
            print(f"{playlist_index + 1}. Failed to confirm liking: {track_name} by {artist_name}")

        # Introduce a consistent delay between processing tracks
        time.sleep(delay)

    print(f"Total liked songs: {total_liked}")


if __name__ == "__main__":
    try:
        # Step 1: Fetch all tracks in playlist order
        tracks = fetch_all_tracks_in_order(PLAYLIST_ID)

        # Step 2: Process tracks with API response validation and shorter delays
        INITIAL_DELAY = 1.0  # Reduced to 1 second for faster processing
        like_tracks_with_shorter_delays(tracks, INITIAL_DELAY)

    except spotipy.SpotifyException as e:
        print(f"Spotify API Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
