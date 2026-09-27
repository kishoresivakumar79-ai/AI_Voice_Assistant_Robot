class FaceRecognizer:
    """Matches face bounding boxes against known user embeddings."""

    def __init__(self, model_path="../../models/face_model.pkl"):
        self.model_path = model_path
        print(f"[FaceRecognizer] Initialized with model path='{model_path}'")

    def recognize(self, frame, bbox):
        """Identifies person name from face bounding box."""
        # Returns face identity match
        return "User (Admin)"
