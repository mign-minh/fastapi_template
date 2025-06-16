import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

class AppConfig:
    APP_NAME = "Computer Vision API"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Template API cho việc triển khai mô hình Computer Vision"
    
class ImageConfig:
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR = Path(__file__).parent.parent / "uploads"

class ServerConfig:
    HOST = "0.0.0.0"
    PORT = 8000
    RELOAD = True
    WORKERS = 4