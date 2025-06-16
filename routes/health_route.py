from fastapi import APIRouter
from schemas.yolo_schema import HealthResponse
from config.app_cfg import AppConfig
from models.yolo_predictor import YOLOPredictor

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Check if model is loaded
        model_loaded = hasattr(YOLOPredictor, 'yolo_model') and YOLOPredictor().yolo_model.model is not None
        
        return HealthResponse(
            status="healthy",
            message="YOLOv8 API is running",
            version=AppConfig.APP_VERSION,
            model_loaded=model_loaded
        )
    except:
        return HealthResponse(
            status="unhealthy", 
            message="Model not loaded",
            version=AppConfig.APP_VERSION,
            model_loaded=False
        )

@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {AppConfig.APP_NAME}",
        "version": AppConfig.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
        "model_info": "/api/v1/yolo/model-info"
    }