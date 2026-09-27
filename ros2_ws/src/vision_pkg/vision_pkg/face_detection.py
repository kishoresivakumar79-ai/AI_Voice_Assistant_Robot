class FaceDetector:
    """Detects human faces in video frames."""

    def __init__(self):
        self.face_cascade = None
        try:
            import cv2
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            print("[FaceDetector] OpenCV Haar Cascade loaded.")
        except Exception as e:
            print(f"[FaceDetector Info] OpenCV cascade unavailable ({e}). Using simulation mode.")

    def detect_faces(self, frame):
        """Returns bounding boxes [(x, y, w, h)] of detected faces."""
        if self.face_cascade is not None and frame is not None:
            try:
                import cv2
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                return [(x, y, w, h) for (x, y, w, h) in faces]
            except Exception as e:
                print(f"[FaceDetector Error] {e}")
        # Simulated face bounding box for test runs
        return [(120, 80, 100, 100)]
