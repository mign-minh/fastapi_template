import os
from pathlib import Path
from PIL import Image
from config.app_cfg import ImageConfig

def validate_image_file(filename: str, file_size: int) -> tuple[bool, str]:
    """Validate uploaded image file"""
    
    # Check file extension
    file_ext = Path(filename).suffix.lower()
    if file_ext not in ImageConfig.ALLOWED_EXTENSIONS:
        return False, f"File extension {file_ext} not allowed. Allowed: {ImageConfig.ALLOWED_EXTENSIONS}"
    
    # Check file size
    if file_size > ImageConfig.MAX_FILE_SIZE:
        return False, f"File size {file_size} exceeds maximum {ImageConfig.MAX_FILE_SIZE} bytes"
    
    return True, "Valid"

def save_uploaded_file(file_content: bytes, filename: str) -> str:
    """Save uploaded file to upload directory"""
    
    # Create upload directory if not exists
    ImageConfig.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_path = ImageConfig.UPLOAD_DIR / filename
    counter = 1
    while file_path.exists():
        name, ext = os.path.splitext(filename)
        file_path = ImageConfig.UPLOAD_DIR / f"{name}_{counter}{ext}"
        counter += 1
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    return str(file_path)