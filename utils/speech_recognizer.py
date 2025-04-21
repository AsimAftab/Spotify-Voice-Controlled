import speech_recognition as sr

class SpeechRecognitionAgent:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen_command(self):
        with sr.Microphone() as source:
            print("🎤 Listening for your command...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text
        except Exception as e:
            print(f"❌ Could not recognize speech: {e}")
            return None
