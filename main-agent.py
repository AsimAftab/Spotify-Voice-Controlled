from utils.speech_recognizer import SpeechRecognitionAgent
from utils.intent_parser import IntentParser
from services.spotify_agent import SpotifyControlAgent, SpotifyDirectControl


class MainAgent:
    def __init__(self):
        self.speech_agent = SpeechRecognitionAgent()
        self.intent_parser = IntentParser()
        self.spotify_agent = SpotifyControlAgent()

    def run(self):
        while True:
            user_command = self.speech_agent.listen_command()
            if not user_command:
                print("No command detected. Please try again.")
                continue

            intent_data = self.intent_parser.parse(user_command)
            if not intent_data:
                print("Intent not recognized!")
                continue

            action = intent_data['action']
            target = intent_data.get('target')

            if action == "play_music":
                # Get the token and pass it to SpotifyDirectControl
                token = self.spotify_agent.get_token()
                spotify_direct = SpotifyDirectControl(token)

                # Get devices and play music
                devices = spotify_direct.get_devices()
                if devices:
                    device_id = devices[0]['id']
                    track_uri = self.search_song_uri(target)  # Add a method to search for the song URI
                    spotify_direct.play_song(track_uri, device_id)
                else:
                    print("No active devices found. Open Spotify on your PC or phone!")
            
            elif action == "join_meeting":
                self.meet_agent.join_meeting(target)
            elif action == "search_youtube":
                self.youtube_agent.search_and_play(target)
            elif action == "exit":
                print("👋 Exiting MainAgent.")
                break
            else:
                print("Action not supported yet.")

    def search_song_uri(self, song_name):
        # Implement song search functionality here
        # For example, search for the song on Spotify and return the track URI
        result = self.spotify_agent.sp.search(song_name, limit=1, type='track')
        tracks = result.get('tracks', {}).get('items', [])
        if tracks:
            return tracks[0]['uri']
        return None


if __name__ == "__main__":
    agent = MainAgent()
    agent.run()
