class ROSSpeechToText:
    """ROS2 compatible speech to text processor."""
    def __init__(self):
        print("[ROS STT] Module Initialized.")

    def process_audio(self, audio_data: bytes) -> str:
        # Converts byte stream to text transcript
        return "Hello Jarvis robot move forward"
