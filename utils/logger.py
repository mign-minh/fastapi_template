import sys
import logging
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from logging.handlers import RotatingFileHandler
from config.logging_cfg import LoggingConfig

class Logger:
    def __init__(self, name="", log_level=None, log_file=None) -> None:
        if log_level is None:
            log_level = getattr(logging, LoggingConfig.LOG_LEVEL)
        self.log = logging.getLogger(name)
        self.get_logger(log_level, log_file)

    def get_logger(self, log_level, log_file):
        self.log.setLevel(log_level)
        self._init_formatter()
        if log_file is not None:
            self._add_file_hander(LoggingConfig.LOG_DIR / log_file)
        else:
            self._add_stream_hander()

    def _init_formatter(self):
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    def _add_stream_hander(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(self.formatter)
        self.log.addHandler(stream_handler)

    def _add_file_hander(self, log_file):
        file_handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=10)
        file_handler.setFormatter(self.formatter)
        self.log.addHandler(file_handler)

    def log_detection(self, filename, num_detections, confidence_scores):
        self.log.info(f"Detection completed: {filename} - Objects: {num_detections} - Max confidence: {max(confidence_scores) if confidence_scores else 0:.3f}")

    def log_model_load(self, model_name, device):
        self.log.info(f"Model loaded: {model_name} on {device}")
