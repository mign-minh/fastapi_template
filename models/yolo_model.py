import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from ultralytics import YOLO
from config.yolo_cfg import YOLOConfig
from utils.logger import Logger

LOGGER = Logger(__file__, log_file="model.log")

class YOLOModel:
    def __init__(self):
        self.model = None
        self.model_name = YOLOConfig.MODEL_NAME
        self.model_path = YOLOConfig.MODEL_PATH
        self.device = YOLOConfig.DEVICE
        self.load_model()

    def load_model(self):
        """Load YOLOv8 model"""
        try:
            # Check if custom model exists, otherwise use pretrained
            if self.model_path.exists():
                LOGGER.log.info(f"Loading model from: {self.model_path}")
                self.model = YOLO(str(self.model_path))
            else:
                LOGGER.log.info(f"Loading pretrained model: {self.model_name}")
                self.model = YOLO(self.model_name)
                
                # Save model to specified path for future use
                self.model_path.parent.mkdir(parents=True, exist_ok=True)
                self.model.save(str(self.model_path))
            
            # Move to specified device
            self.model.to(self.device)
            
            LOGGER.log_model_load(self.model_name, self.device)
            LOGGER.log.info(f"Model classes: {list(self.model.names.values())}")
            
        except Exception as e:
            LOGGER.log.error(f"Failed to load model: {str(e)}")
            raise e

    def get_model_info(self):
        """Get model information"""
        if self.model is None:
            return None
            
        return {
            "name": self.model_name,
            "device": str(self.device),
            "classes": list(self.model.names.values()),
            "num_classes": len(self.model.names)
        }
