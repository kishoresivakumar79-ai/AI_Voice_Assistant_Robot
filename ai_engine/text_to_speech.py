class TextToSpeech:
    """Converts text responses into spoken audio using pyttsx3 or system sound output."""

    def __init__(self, voice_gender="female", rate=160):
        self.rate = rate
        self.gender = voice_gender
        self.engine = None
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.rate)
            voices = self.engine.getProperty('voices')
            if voices:
                for v in voices:
                    if voice_gender in v.name.lower():
                        self.engine.setProperty('voice', v.id)
                        break
        except Exception as e:
            print(f"[TTS Info] pyttsx3 offline engine unavailable ({e}). Fallback to stdout output.")

    def speak(self, text: str):
        """Synthesize audio speech for input text."""
        print(f"[Robot Speaks 🔊]: \"{text}\"")
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"[TTS Error] {e}")
