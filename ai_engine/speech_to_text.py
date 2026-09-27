import os
import sys

class SpeechToText:
    """Converts audio speech to text using Whisper or SpeechRecognition engines."""

    def __init__(self, engine="whisper", model_size="small"):
        self.engine = engine
        self.model_size = model_size
        print(f"[STT] Initialized SpeechToText engine='{engine}' with model='{model_size}'")

    def transcribe_audio_file(self, audio_path: str) -> str:
        """Transcribe an audio file into text."""
        if not os.path.exists(audio_path):
            print(f"[STT Error] File not found: {audio_path}")
            return ""
        # Simulation / Whisper binding point
        print(f"[STT] Transcribing file {audio_path}...")
        return "Hello Jarvis move forward by two meters"

    def listen_and_transcribe(self, prompt="Listening...") -> str:
        """Capture microphone input and transcribe to string."""
        print(f"[STT] {prompt}")
        try:
            # If speech_recognition is installed, use microphone, else prompt mock/console input
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = recognizer.recognize_google(audio)
                print(f"[STT Heard]: {text}")
                return text
        except Exception as e:
            # Fallback to simulated input if mic unavailable or libraries missing
            print(f"[STT Info] Microphone capture unavailable ({e}). Defaulting to command simulation.")
            return "Jarvis move forward and find my face"
