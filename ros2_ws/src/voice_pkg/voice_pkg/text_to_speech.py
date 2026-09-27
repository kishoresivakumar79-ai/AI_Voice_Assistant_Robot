class ROSTextToSpeech:
    """ROS2 compatible text to speech synthesizer."""
    def __init__(self):
        print("[ROS TTS] Module Initialized.")

    def synthesize(self, text: str):
        print(f"[ROS TTS Output]: {text}")
