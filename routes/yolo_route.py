import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from fastapi import File, UploadFile, HTTPException, APIRouter
from schemas.yolo_schema import YOLOResponse
from utils.image_utils import validate_image_file, save_uploaded_file
from models.yolo_predictor import YOLOPredictor
from utils.logger import Logger

router = APIRouter()
logger = Logger(__file__, log_file="yolo.log")

# Initialize predictor (singleton)
predictor = YOLOPredictor()

@router.post("/detect", response_model=YOLOResponse)
async def detect_objects(file: UploadFile = File(...)):
    """
    Upload ảnh và detect objects bằng YOLOv8
    Trả về kết quả detection và ảnh đã annotate dưới dạng base64
    """
    
    try:
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Validate file
        is_valid, message = validate_image_file(file.filename, file_size)
        if not is_valid:
            logger.log.error(f"Invalid file: {file.filename} - {message}")
            raise HTTPException(status_code=400, detail=message)
        
        # Save file
        file_path = save_uploaded_file(content, file.filename)
        
        logger.log.info(f"Processing image: {file.filename}")
        
        # Run prediction
        result = await predictor.predict(file_path)
        
        return YOLOResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.log.error(f"Detection failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

@router.get("/model-info")
async def get_model_info():
    """Get YOLOv8 model information"""
    try:
        model_info = predictor.yolo_model.get_model_info()
        return {
            "success": True,
            "model_info": model_info
        }
    except Exception as e:
        logger.log.error(f"Failed to get model info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))