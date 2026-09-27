# Machine Learning Models Directory

This directory stores offline pretrained models used by the AI Voice Assistant Robot:

1. **`yolov8.pt`**: Ultralytics YOLOv8 object detection model for spatial awareness & obstacle categorization.
   - Download command: `wget https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt -O yolov8.pt`
2. **`whisper-small/`**: OpenAI Whisper speech recognition model.
   - Auto-downloaded by HuggingFace / Faster-Whisper python modules.
3. **`face_model.pkl`**: Pickled face embeddings dataset trained on authorized robot user images.
