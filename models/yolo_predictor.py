import sys
import io
import base64
import cv2
import numpy as np
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from PIL import Image
from utils.logger import Logger
from config.yolo_cfg import YOLOConfig
from .yolo_model import YOLOModel

LOGGER = Logger(__file__, log_file="predictor.log")

class YOLOPredictor:
    def __init__(self):
        self.yolo_model = YOLOModel()
        self.confidence = YOLOConfig.CONFIDENCE
        self.iou_threshold = YOLOConfig.IOU_THRESHOLD
        self.max_detections = YOLOConfig.MAX_DETECTIONS
        self.image_size = YOLOConfig.IMAGE_SIZE

    async def predict(self, image_file) -> dict:
        """Predict objects in image and return annotated image as base64"""
        try:
            # Load image
            image = Image.open(image_file)
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            
            # Convert PIL to opencv format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Run inference
            results = self.yolo_model.model(
                cv_image,
                conf=self.confidence,
                iou=self.iou_threshold,
                max_det=self.max_detections,
                imgsz=self.image_size
            )
            
            # Process results
            detections = self._process_results(results[0])
            
            # Draw annotations on image
            annotated_image = self._draw_annotations(cv_image, results[0])
            
            # Convert annotated image to base64
            base64_image = self._image_to_base64(annotated_image)
            
            LOGGER.log_detection(
                "uploaded_image", 
                len(detections), 
                [det['confidence'] for det in detections]
            )
            
            return {
                "success": True,
                "detections": detections,
                "annotated_image_base64": base64_image,
                "model_info": self.yolo_model.get_model_info(),
                "inference_params": {
                    "confidence": self.confidence,
                    "iou_threshold": self.iou_threshold,
                    "image_size": self.image_size
                }
            }
            
        except Exception as e:
            LOGGER.log.error(f"Prediction failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "detections": [],
                "annotated_image_base64": None
            }

    def _process_results(self, result) -> list:
        """Process YOLO results into structured format"""
        detections = []
        
        if result.boxes is not None:
            boxes = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy().astype(int)
            
            for i, (box, conf, cls_id) in enumerate(zip(boxes, confidences, class_ids)):
                x1, y1, x2, y2 = box
                
                detection = {
                    "id": i,
                    "class_id": int(cls_id),
                    "class_name": self.yolo_model.model.names[cls_id],
                    "confidence": float(conf),
                    "bbox": {
                        "x1": float(x1),
                        "y1": float(y1),
                        "x2": float(x2),
                        "y2": float(y2),
                        "width": float(x2 - x1),
                        "height": float(y2 - y1)
                    }
                }
                detections.append(detection)
        
        return detections

    def _draw_annotations(self, image, result):
        """Draw bounding boxes and labels on image"""
        annotated_img = image.copy()
        
        if result.boxes is not None:
            boxes = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy().astype(int)
            
            for box, conf, cls_id in zip(boxes, confidences, class_ids):
                x1, y1, x2, y2 = map(int, box)
                
                # Draw bounding box
                cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw label
                label = f"{self.yolo_model.model.names[cls_id]}: {conf:.2f}"
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                
                # Draw label background
                cv2.rectangle(annotated_img, (x1, y1 - label_size[1] - 10), 
                            (x1 + label_size[0], y1), (0, 255, 0), -1)
                
                # Draw label text
                cv2.putText(annotated_img, label, (x1, y1 - 5), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        return annotated_img

    def _image_to_base64(self, cv_image) -> str:
        """Convert OpenCV image to base64 string"""
        # Encode image to jpeg
        _, buffer = cv2.imencode('.jpg', cv_image)
        
        # Convert to base64
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return image_base64