from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import requests

class SpotifyControlAgent:
    def __init__(self):
        self.auth_manager = SpotifyOAuth(
            client_id="e99e9d6443ff4a74b271d40e64743387",
            client_secret="ff682d7c63e04884819d1e6b79dcae05",
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="user-modify-playback-state,user-read-playback-state,user-read-currently-playing"
        )
        self.sp = Spotify(auth_manager=self.auth_manager)

    def get_token(self):
        token_info = self.auth_manager.get_cached_token()
        if not token_info:
            token_info = self.auth_manager.get_access_token(as_dict=True)
        return token_info['access_token']

    def search_song(self, song_name):
        result = self.sp.search(song_name, limit=1, type='track')
        if result['tracks']['items']:
            return result['tracks']['items'][0]['uri']
        return None

class SpotifyDirectControl:
    def __init__(self, bearer_token):
        self.token = bearer_token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get_devices(self):
        url = "https://api.spotify.com/v1/me/player/devices"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            devices = response.json()
            for device in devices['devices']:
                print(f"Device: {device['name']} — ID: {device['id']} — Type: {device['type']}")
            return devices['devices']
        else:
            print(f"Error fetching devices: {response.status_code} — {response.text}")
            return []

    def play_song(self, uri, device_id=None):
        url = "https://api.spotify.com/v1/me/player/play"
        if device_id:
            url += f"?device_id={device_id}"

        data = {
            "uris": [uri]
        }

        response = requests.put(url, headers=self.headers, json=data)
        if response.status_code == 204:
            print("Playback started successfully.")
        else:
            print(f"Failed to start playback: {response.status_code} — {response.text}")
