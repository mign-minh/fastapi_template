import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from fastapi import File, UploadFile, HTTPException, APIRouter
from schemas.response_schema import UploadResponse, ProcessResponse
from utils.image_utils import validate_image_file, save_uploaded_file, process_image
from utils.logger import Logger

router = APIRouter()
logger = Logger(__file__, log_file="image.log")

@router.post("/upload", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """Upload ảnh và trả về thông tin cơ bản"""
    
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
        
        logger.log_upload(file.filename, file_size)
        
        return UploadResponse(
            success=True,
            message="File uploaded successfully",
            filename=file.filename,
            file_size=file_size
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.log.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/process", response_model=ProcessResponse)
async def process_uploaded_image(file: UploadFile = File(...)):
    """Upload và xử lý ảnh"""
    
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
        
        # Process image
        result = process_image(file_path)
        
        logger.log_upload(file.filename, file_size)
        logger.log_process(file.filename, "success" if result.get("processed") else "failed")
        
        return ProcessResponse(**result, success=result.get("processed", False))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.log.error(f"Process failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Process failed: {str(e)}")
