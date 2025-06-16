from fastapi import APIRouter
from .yolo_route import router as yolo_router
from .health_route import router as health_router

router = APIRouter()
router.include_router(health_router)
router.include_router(yolo_router, prefix="/api/v1/yolo", tags=["YOLOv8 Detection"])