class PersonTracker:
    """Calculates horizontal displacement (dx) and distance (depth) to track a target person."""

    def __init__(self, frame_width=640, frame_height=480):
        self.center_x = frame_width // 2
        self.center_y = frame_height // 2

    def calculate_steering(self, bbox):
        """Computes angular error and linear distance error for follower control."""
        if not bbox:
            return 0.0, 0.0 # angular_error, distance_error
        x, y, w, h = bbox
        target_x = x + (w // 2)
        error_x = (target_x - self.center_x) / float(self.center_x) # normalized [-1.0, 1.0]
        estimated_distance = 100.0 / float(w) if w > 0 else 1.0 # arbitrary depth estimate
        return error_x, estimated_distance
