import time

class WakeWordDetector:
    """Detects wake words like 'Hello Jarvis' or 'Jarvis' from incoming audio or stream."""

    def __init__(self, wake_words=None):
        if wake_words is None:
            self.wake_words = ["hello jarvis", "jarvis", "hey jarvis", "robot"]
        else:
            self.wake_words = [w.lower() for w in wake_words]

    def check_text(self, text: str) -> bool:
        """Checks if text contains any wake word."""
        if not text:
            return False
        clean_text = text.lower().strip()
        for word in self.wake_words:
            if word in clean_text:
                return True
        return False

    def listen_passive(self, timeout=5.0) -> bool:
        """Simulate passive listening loop for wake word."""
        print("[WakeWordDetector] Listening passively for wake word ('Hello Jarvis')...")
        time.sleep(0.5)
        # Placeholder for real audio stream wake word model (e.g. Porcupine / Snowboy / OpenWakeWord)
        return True
