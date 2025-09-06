# Spotify Sequential Playlist Liker

A Python script to like all songs in a Spotify playlist in the same order as they appear. This project uses the Spotify Web API to automate the process of liking songs while preserving the playlist's original sequence.

## Features
- Fetches all songs from a Spotify playlist (supports playlists with over 100 tracks).
- Likes songs in the exact playlist order.
- Includes retry logic for failed requests.
- Logs progress to ensure transparency and ease of debugging.

---

## Prerequisites

1. **Spotify Developer Account**:
   - Register at [Spotify for Developers](https://developer.spotify.com/dashboard/).
   - Create a new app to get your `Client ID` and `Client Secret`.

2. **Python 3.8 or Later**:
   - Ensure you have Python installed. Download it from [python.org](https://www.python.org/) if needed.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/spotify-playlist-liker.git
   cd spotify-playlist-liker
   ```

2. **Install Dependencies**:
   Use `pip` to install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   - Create a `.env` file in the project directory with the following content:
     ```plaintext
     SPOTIFY_CLIENT_ID=your_client_id
     SPOTIFY_CLIENT_SECRET=your_client_secret
     SPOTIFY_PLAYLIST_ID=your_playlist_id
     SPOTIFY_REDIRECT_URI=http://localhost:8888/callback/
     ```
   - Replace `your_client_id` and `your_client_secret` with the credentials from your Spotify Developer account.
   - Replace `your_playlist_id` with the exact playlist you wish to like the songs from. **If playlist URL is `https://open.spotify.com/playlist/24kH4QpTd1ha5AyiWR3rOs?si=9ecf8ae8812b4207` then playlist ID is `24kH4QpTd1ha5AyiWR3rOs`.**

---

4. **Run the Script**:
   Execute the Python script to like the songs in your playlist:
   ```bash
   python index.py
   ```

5. **Verify**:
   - Check your Spotify account to confirm the liked songs.
   - The script logs each track as it processes them.

---

## Notes

- **Rate Limits**: The script introduces a delay (`time.sleep(0.2)`) between requests to avoid exceeding Spotify’s rate limits. You can adjust this delay if needed.
- **Unavailable Tracks**: Tracks unavailable in your region or marked as local files in the playlist will be skipped.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
