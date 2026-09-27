import re

class CommandParser:
    """Parses text input into executable structured commands for ROS2 navigation and vision nodes."""

    def parse(self, text: str, intent: str) -> dict:
        text_lower = text.lower()
        command = {
            "raw_text": text,
            "intent": intent,
            "action": "none",
            "params": {}
        }

        if intent == "NAVIGATION":
            if "wave" in text_lower or "hand" in text_lower or "arm" in text_lower:
                command["action"] = "wave_hand"
            elif "forward" in text_lower or "ahead" in text_lower:
                command["action"] = "move_forward"
                command["params"]["speed"] = self._extract_number(text_lower, default=0.5)
            elif "backward" in text_lower or "back" in text_lower:
                command["action"] = "move_backward"
                command["params"]["speed"] = self._extract_number(text_lower, default=0.5)
            elif "left" in text_lower:
                command["action"] = "turn_left"
                command["params"]["angle"] = 90
            elif "right" in text_lower:
                command["action"] = "turn_right"
                command["params"]["angle"] = 90
            elif "stop" in text_lower or "halt" in text_lower:
                command["action"] = "stop"

        elif intent == "VISION":
            if "face" in text_lower:
                command["action"] = "face_detection"
            elif "track" in text_lower or "follow" in text_lower:
                command["action"] = "person_tracking"

        elif intent == "STATUS":
            command["action"] = "get_status"

        return command

    def _extract_number(self, text: str, default=0.5) -> float:
        cleaned_text = re.sub(r'mark\s*12|mark\s*xii', '', text, flags=re.IGNORECASE)
        matches = re.findall(r"[-+]?\d*\.\d+|\d+", cleaned_text)
        if matches:
            return float(matches[0])
        return default
