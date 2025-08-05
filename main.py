from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import logging
import os
import platform
import subprocess
from typing import Dict, Any
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
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

# Create downloads directory if it doesn't exist
DOWNLOADS_DIR = "downloads"
if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)
    logger.info(f"Created downloads directory: {DOWNLOADS_DIR}")

@app.get("/")
async def serve_download_page():
    """Serve the agent download page"""
    try:
        download_path = "static/download.html"
        if os.path.exists(download_path):
            return FileResponse(download_path)
        else:
            logger.error(f"Download page not found at {download_path}")
            raise HTTPException(status_code=404, detail="Download page not found")
    except Exception as e:
        logger.error(f"Error serving download page: {e}")
        raise HTTPException(status_code=500, detail="Error serving download page")

@app.get("/downloads/{filename}")
async def download_agent_binary(filename: str):
    """Download agent binary files"""
    try:
        # Validate filename for security
        allowed_files = [
            "carboncompliance-agent-macos",
            "carboncompliance-agent-linux", 
            "carboncompliance-agent-windows.exe"
        ]
        
        if filename not in allowed_files:
            logger.warning(f"Invalid download request: {filename}")
            raise HTTPException(status_code=400, detail="Invalid file requested")
        
        file_path = os.path.join(DOWNLOADS_DIR, filename)
        
        # If file doesn't exist, create a placeholder binary
        if not os.path.exists(file_path):
            await create_placeholder_binary(filename, file_path)
        
        if os.path.exists(file_path):
            logger.info(f"Serving download: {filename}")
            return FileResponse(
                path=file_path,
                filename=filename,
                media_type='application/octet-stream'
            )
        else:
            logger.error(f"File not found: {file_path}")
            raise HTTPException(status_code=404, detail="File not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving download {filename}: {e}")
        raise HTTPException(status_code=500, detail="Error serving download")

async def create_placeholder_binary(filename: str, file_path: str):
    """Create a placeholder binary file for testing"""
    try:
        if filename == "carboncompliance-agent-macos" or filename == "carboncompliance-agent-linux":
            # Create a simple shell script as placeholder
            content = f"""#!/bin/bash
echo "CarbonCompliance Agent - {filename}"
echo "This is a placeholder binary for testing purposes"
echo "In production, this would be the actual agent binary"
echo "API URL: https://carboncompliance.carbonteq.build"
echo "Device ID: $(hostname)"
echo "Starting agent..."
sleep 2
echo "Agent started successfully"
"""
            with open(file_path, 'w') as f:
                f.write(content)
            os.chmod(file_path, 0o755)  # Make executable
            
        elif filename == "carboncompliance-agent-windows.exe":
            # Create a simple batch file as placeholder
            content = f"""@echo off
echo CarbonCompliance Agent - {filename}
echo This is a placeholder binary for testing purposes
echo In production, this would be the actual agent binary
echo API URL: https://carboncompliance.carbonteq.build
echo Device ID: %COMPUTERNAME%
echo Starting agent...
timeout /t 2 /nobreak >nul
echo Agent started successfully
pause
"""
            with open(file_path, 'w') as f:
                f.write(content)
        
        logger.info(f"Created placeholder binary: {filename}")
        
    except Exception as e:
        logger.error(f"Error creating placeholder binary {filename}: {e}")
        raise

@app.get("/api/download/{os_type}")
async def get_download_info(os_type: str):
    """Get download information for agent binaries"""
    try:
        # Production-ready download information
        download_info = {
            "macos": {
                "binary_name": "carboncompliance-agent-macos",
                "download_url": "http://192.168.1.242:8081/downloads/carboncompliance-agent-macos",
                "single_command": "curl -s http://192.168.1.242:8081/downloads/carboncompliance-agent-macos -o carboncompliance-agent-macos && chmod +x carboncompliance-agent-macos && ./carboncompliance-agent-macos --api-url=https://carboncompliance.carbonteq.build",
                "instructions": "chmod +x carboncompliance-agent-macos && ./carboncompliance-agent-macos --api-url=https://carboncompliance.carbonteq.build",
                "docker_command": "docker run -d --name carboncompliance-agent --restart unless-stopped -e API_BASE_URL=https://carboncompliance.carbonteq.build carbonteq/carboncompliance-agent:latest"
            },
            "linux": {
                "binary_name": "carboncompliance-agent-linux", 
                "download_url": "http://192.168.1.242:8081/downloads/carboncompliance-agent-linux",
                "single_command": "curl -s http://192.168.1.242:8081/downloads/carboncompliance-agent-linux -o carboncompliance-agent-linux && chmod +x carboncompliance-agent-linux && ./carboncompliance-agent-linux --api-url=https://carboncompliance.carbonteq.build",
                "instructions": "chmod +x carboncompliance-agent-linux && ./carboncompliance-agent-linux --api-url=https://carboncompliance.carbonteq.build",
                "docker_command": "docker run -d --name carboncompliance-agent --restart unless-stopped -e API_BASE_URL=https://carboncompliance.carbonteq.build carbonteq/carboncompliance-agent:latest"
            },
            "windows": {
                "binary_name": "carboncompliance-agent-windows.exe",
                "download_url": "http://192.168.1.242:8081/downloads/carboncompliance-agent-windows.exe", 
                "single_command": "powershell -Command \"Invoke-WebRequest -Uri 'http://192.168.1.242:8081/downloads/carboncompliance-agent-windows.exe' -OutFile 'carboncompliance-agent-windows.exe'; .\\carboncompliance-agent-windows.exe --api-url=https://carboncompliance.carbonteq.build\"",
                "instructions": ".\\carboncompliance-agent-windows.exe --api-url=https://carboncompliance.carbonteq.build",
                "docker_command": "docker run -d --name carboncompliance-agent --restart unless-stopped -e API_BASE_URL=https://carboncompliance.carbonteq.build carbonteq/carboncompliance-agent:latest"
            }
        }
        
        if os_type not in download_info:
            logger.warning(f"Unsupported OS type requested: {os_type}")
            raise HTTPException(status_code=400, detail="Unsupported OS type")
        
        logger.info(f"Download info requested for OS: {os_type}")
        return download_info[os_type]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting download info for {os_type}: {e}")
        raise HTTPException(status_code=500, detail="Error getting download information")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        return {
            "status": "healthy", 
            "service": "agent-download",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "unhealthy", "error": str(e)}
        )

@app.get("/api/system-info")
async def get_system_info():
    """Get system information for debugging"""
    try:
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "working_directory": os.getcwd(),
            "static_files_dir": "static" if os.path.exists("static") else "not found",
            "downloads_dir": DOWNLOADS_DIR if os.path.exists(DOWNLOADS_DIR) else "not found"
        }
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        raise HTTPException(status_code=500, detail="Error getting system information")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting CarbonCompliance Agent Download Service on port 8081")
    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="info") 