from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CarbonCompliance Agent Download",
    description="Standalone application for downloading CarbonCompliance agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    logger.warning(f"Could not mount static files: {e}")

@app.get("/")
async def serve_download_page():
    """Serve the agent download page"""
    try:
        download_path = "static/download.html"
        if os.path.exists(download_path):
            return FileResponse(download_path)
        else:
            raise HTTPException(status_code=404, detail="Download page not found")
    except Exception as e:
        logger.error(f"Error serving download page: {e}")
        raise HTTPException(status_code=500, detail="Error serving download page")

@app.get("/api/download/{os_type}")
async def get_download_info(os_type: str):
    """Get download information for agent binaries"""
    download_info = {
        "macos": {
            "binary_name": "carboncompliance-agent-macos",
            "download_url": "https://carboncomplianceagent.carbonteq.build/downloads/carboncompliance-agent-macos",
            "single_command": "curl -s https://carboncomplianceagent.carbonteq.build/downloads/carboncompliance-agent-macos -o carboncompliance-agent-macos && chmod +x carboncompliance-agent-macos && ./carboncompliance-agent-macos --api-url=https://carboncompliance.carbonteq.build",
            "instructions": "chmod +x carboncompliance-agent-macos && ./carboncompliance-agent-macos --api-url=https://carboncompliance.carbonteq.build"
        },
        "linux": {
            "binary_name": "carboncompliance-agent-linux", 
            "download_url": "https://carboncomplianceagent.carbonteq.build/downloads/carboncompliance-agent-linux",
            "single_command": "curl -s https://carboncomplianceagent.carbonteq.build/downloads/carboncompliance-agent-linux -o carboncompliance-agent-linux && chmod +x carboncompliance-agent-linux && ./carboncompliance-agent-linux --api-url=https://carboncompliance.carbonteq.build",
            "instructions": "chmod +x carboncompliance-agent-linux && ./carboncompliance-agent-linux --api-url=https://carboncompliance.carbonteq.build"
        },
        "windows": {
            "binary_name": "carboncompliance-agent-windows.exe",
            "download_url": "https://carboncomplianceagent.carbonteq.build/downloads/carboncompliance-agent-windows.exe", 
            "single_command": "powershell -Command \"Invoke-WebRequest -Uri 'https://carboncomplianceagent.carbonteq.build/downloads/carboncompliance-agent-windows.exe' -OutFile 'carboncompliance-agent-windows.exe'; .\\carboncompliance-agent-windows.exe --api-url=https://carboncompliance.carbonteq.build\"",
            "instructions": ".\\carboncompliance-agent-windows.exe --api-url=https://carboncompliance.carbonteq.build"
        }
    }
    
    if os_type not in download_info:
        raise HTTPException(status_code=400, detail="Unsupported OS type")
    
    return download_info[os_type]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "agent-download"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 