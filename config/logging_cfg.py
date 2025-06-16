import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class LoggingConfig:
    ROOT_DIR = Path(__file__).parent.parent
    LOG_DIR = Path(os.getenv("LOG_DIR", "./logs"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LoggingConfig.LOG_DIR.mkdir(parents=True, exist_ok=True)