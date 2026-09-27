from .face_detection import FaceDetector
from .face_recognition import FaceRecognizer
from .person_tracking import PersonTracker

class CameraNode:
    """ROS2 Vision Node orchestrating camera input, face detection, and tracking."""

    def __init__(self):
        self.detector = FaceDetector()
        self.recognizer = FaceRecognizer()
        self.tracker = PersonTracker()
        print("[CameraNode] Initialized vision pipeline.")

    def process_frame(self, frame=None):
        faces = self.detector.detect_faces(frame)
        results = []
        for bbox in faces:
            identity = self.recognizer.recognize(frame, bbox)
            error_x, distance = self.tracker.calculate_steering(bbox)
            results.append({
                "bbox": bbox,
                "identity": identity,
                "steering_error_x": error_x,
                "estimated_distance": distance
            })
        return results

def main():
    node = CameraNode()
    res = node.process_frame()
    print(f"[CameraNode Run Result]: {res}")

if __name__ == '__main__':
    main()
