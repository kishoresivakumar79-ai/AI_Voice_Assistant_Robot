class ChatbotEngine:
    """Generates conversational responses and robot feedback based on command status and user queries."""

    def __init__(self, bot_name="MARK 12"):
        self.bot_name = bot_name

    def generate_response(self, text: str, intent: str, command: dict) -> str:
        if intent == "NAVIGATION":
            action = command.get("action", "move")
            if action == "move_forward":
                return f"MARK 12 advancing forward at speed {command['params'].get('speed', 0.5)} meters per second."
            elif action == "move_backward":
                return "MARK 12 reversing backward."
            elif action == "turn_left":
                return "MARK 12 turning left 90 degrees."
            elif action == "turn_right":
                return "MARK 12 turning right 90 degrees."
            elif action == "wave_hand":
                return "MARK 12 raising right hand and waving to user."
            elif action == "stop":
                return "MARK 12 stopping all motor movement immediately."
            return "Executing navigation command."

        elif intent == "VISION":
            action = command.get("action")
            if action == "face_detection":
                return "Activating camera feed and scanning for human faces."
            elif action == "person_tracking":
                return "Engaging person tracking algorithm."
            return "Vision processing initiated."

        elif intent == "STATUS":
            return "All MARK 12 sub-systems are operating normally. Battery level is at 95 percent."

        # General conversation
        text_lower = text.lower()
        if "hello" in text_lower or "hi" in text_lower:
            return f"Hello! I am {self.bot_name}, your 3D AI Voice Assistant Robot. How can I assist you?"
        elif "who are you" in text_lower:
            return f"I am {self.bot_name}, your futuristic 3D humanoid robot assistant."
        
        return f"MARK 12 processing command: '{text}'."

