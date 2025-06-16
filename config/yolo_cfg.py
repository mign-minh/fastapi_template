import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import torch

sys.path.append(str(Path(__file__).parent))

# Load environment variables
load_dotenv()

class YOLOConfig:
    # Model settings
    MODEL_NAME = os.getenv("YOLO_MODEL_NAME", "yolov8n.pt")
    MODEL_PATH = Path(os.getenv("YOLO_MODEL_PATH", "./models/weights/yolov8n.pt"))
    CONFIDENCE = float(os.getenv("YOLO_CONFIDENCE", "0.25"))
    IOU_THRESHOLD = float(os.getenv("YOLO_IOU_THRESHOLD", "0.45"))
    MAX_DETECTIONS = int(os.getenv("YOLO_MAX_DETECTIONS", "1000"))
    IMAGE_SIZE = int(os.getenv("YOLO_IMAGE_SIZE", "640"))
    DEVICE = os.getenv("YOLO_DEVICE", "cuda" if torch.cuda.is_available() else "cpu")
    
    # Ensure model directory exists
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
