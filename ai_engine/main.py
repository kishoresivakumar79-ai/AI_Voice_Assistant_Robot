import sys
import os
import time

# Ensure ai_engine package is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wake_word import WakeWordDetector
from speech_to_text import SpeechToText
from text_to_speech import TextToSpeech
from intent_classifier import IntentClassifier
from command_parser import CommandParser
from chatbot import ChatbotEngine
from memory import RobotMemory

class AIVoiceAssistantRobot:
    """Main Orchestrator for the AI Voice Assistant Robot Engine."""

    def __init__(self):
        print("==================================================")
        print("  AI VOICE ASSISTANT ROBOT ENGINE (Starting...)   ")
        print("==================================================")
        self.wake_detector = WakeWordDetector()
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.intent_classifier = IntentClassifier()
        self.command_parser = CommandParser()
        self.chatbot = ChatbotEngine()
        self.memory = RobotMemory()
        print("[System] All AI components initialized successfully.")

    def run_cycle(self, test_input: str = None):
        """Runs one turn of the voice assistant interaction pipeline."""
        if test_input is None:
            user_text = self.stt.listen_and_transcribe()
        else:
            user_text = test_input

        print(f"\n[User Input Raw]: {user_text}")

        # Wake word check
        if not self.wake_detector.check_text(user_text):
            print("[System] Wake word not detected in input stream.")
            return

        # Intent classification
        intent = self.intent_classifier.classify(user_text)
        print(f"[Intent]: {intent}")

        # Command parsing
        parsed_cmd = self.command_parser.parse(user_text, intent)
        print(f"[Parsed Command]: {parsed_cmd}")

        # Chatbot response generation
        response = self.chatbot.generate_response(user_text, intent, parsed_cmd)

        # Store in SQLite database memory
        self.memory.store_interaction(user_text, intent, response)

        # Speak response
        self.tts.speak(response)

if __name__ == "__main__":
    assistant = AIVoiceAssistantRobot()
    
    # Run test cycle
    test_phrases = [
        "Hello Jarvis move forward by two meters",
        "Jarvis detect faces in camera feed",
        "Hello Jarvis check battery status"
    ]
    
    for phrase in test_phrases:
        assistant.run_cycle(test_input=phrase)
        time.sleep(1)
