from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any

class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float
    width: float
    height: float

class Detection(BaseModel):
    id: int
    class_id: int
    class_name: str
    confidence: float
    bbox: BoundingBox

class ModelInfo(BaseModel):
    name: str
    device: str
    classes: List[str]
    num_classes: int

class InferenceParams(BaseModel):
    confidence: float
    iou_threshold: float
    image_size: int

class YOLOResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    success: bool
    detections: List[Detection]
    annotated_image_base64: Optional[str] = None
    model_info: Optional[ModelInfo] = None
    inference_params: Optional[InferenceParams] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    status: str
    message: str
    version: str
    model_loaded: bool