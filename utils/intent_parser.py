class IntentParser:
    def parse(self, command):
        command = command.lower()

        if "play music" in command:
            # Remove "play music" part and strip any leading/trailing spaces
            song = command.replace("play music", "").strip()
            if "on spotify" in song:
                song = song.replace("on spotify", "").strip()
            return {"action": "play_music", "target": song}

        if "join" in command and "meeting" in command:
            return {"action": "join_meeting", "target": None}

        if "search" in command and "youtube" in command:
            query = command.replace("search", "").replace("on youtube", "").strip().title()
            return {"action": "search_youtube", "target": query}

        if "exit" in command or "stop" in command:
            return {"action": "exit"}

        return None
