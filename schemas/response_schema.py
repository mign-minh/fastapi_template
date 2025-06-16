from pydantic import BaseModel
from typing import Optional

class UploadResponse(BaseModel):
    success: bool
    message: str
    filename: Optional[str] = None
    file_size: Optional[int] = None
    
class ProcessResponse(BaseModel):
    success: bool
    message: str
    filename: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    mode: Optional[str] = None
    format: Optional[str] = None
    processed: Optional[bool] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    message: str
    version: str