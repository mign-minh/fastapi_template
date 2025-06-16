import uvicorn
from config.app_cfg import ServerConfig

if __name__ == "__main__":
    uvicorn.run(
        "app:app", 
        host=ServerConfig.HOST, 
        port=ServerConfig.PORT, 
        reload=ServerConfig.RELOAD,
        workers=ServerConfig.WORKERS
    )