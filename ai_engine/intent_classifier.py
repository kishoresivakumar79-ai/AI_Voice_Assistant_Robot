class IntentClassifier:
    """Classifies natural language input into robot functional categories."""

    NAV_KEYWORDS = ["move", "forward", "backward", "left", "right", "stop", "turn", "navigate", "go", "wave", "hand", "arm", "raise"]
    VISION_KEYWORDS = ["detect", "face", "see", "camera", "track", "look", "person", "scan"]
    STATUS_KEYWORDS = ["battery", "status", "health", "state", "how are you", "power"]

    def classify(self, text: str) -> str:
        if not text:
            return "UNKNOWN"
        
        text_lower = text.lower()
        
        # Check navigation
        if any(w in text_lower for w in self.NAV_KEYWORDS):
            return "NAVIGATION"
        
        # Check vision
        if any(w in text_lower for w in self.VISION_KEYWORDS):
            return "VISION"
            
        # Check status
        if any(w in text_lower for w in self.STATUS_KEYWORDS):
            return "STATUS"
            
        # Default to conversation / chatbot
        return "CHAT"
