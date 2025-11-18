"""System update API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from app.api.auth import get_current_user
from app.core.config import settings
import logging
import subprocess
import os
import requests

logger = logging.getLogger(__name__)

router = APIRouter()

# Update server configuration
UPDATE_SERVER = "http://deploy.agit8or.net"
UPDATE_ENDPOINT = f"{UPDATE_SERVER}/api/v1/system-updates/version"


class UpdateCheckResponse(BaseModel):
    current_version: str
    latest_version: str
    update_available: bool
    download_url: Optional[str] = None
    release_notes: Optional[str] = None


@router.get("/check")
def check_for_updates(current_user=Depends(get_current_user)):
    """Check if updates are available from the main server"""
    try:
        # Get current version
        current_version = settings.APP_VERSION

        # Query update server for latest version
        try:
            response = requests.get(UPDATE_ENDPOINT, timeout=10)
            if response.status_code == 200:
                update_info = response.json()
                latest_version = update_info.get("version", current_version)

                # Simple version comparison (assumes semantic versioning)
                update_available = latest_version != current_version

                return UpdateCheckResponse(
                    current_version=current_version,
                    latest_version=latest_version,
                    update_available=update_available,
                    download_url=update_info.get("download_url") if update_available else None,
                    release_notes=update_info.get("release_notes")
                )
            else:
                raise Exception(f"Update server returned {response.status_code}")
        except requests.RequestException as e:
            logger.warning(f"Could not reach update server: {e}")
            return UpdateCheckResponse(
                current_version=current_version,
                latest_version=current_version,
                update_available=False,
                release_notes="Could not reach update server"
            )

    except Exception as e:
        logger.error(f"Failed to check for updates: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check for updates: {str(e)}"
        )


@router.get("/version")
def get_version_info():
    """
    Serve version information for update clients
    This endpoint is called BY OTHER INSTANCES to check for updates
    """
    return {
        "version": settings.APP_VERSION,
        "download_url": f"{UPDATE_SERVER}/api/v1/system-updates/download",
        "install_url": f"{UPDATE_SERVER}/install.sh",
        "release_notes": f"""
Depl0y {settings.APP_VERSION} Release Notes:

✨ New Features:
- Automated cloud image deployment
- Inter-node SSH setup for clusters
- Real-time deployment progress tracking
- Enhanced storage validation

🔧 Improvements:
- Node-specific template VMIDs
- Better error messages
- Improved documentation

📚 Documentation:
- One-line installation command
- Automated setup wizards
        """.strip()
    }


@router.get("/download")
def download_update():
    """Download the latest update package (public endpoint for automated updates)"""
    try:
        # Use pre-packaged file
        package_path = "/opt/depl0y/depl0y-v1.1.0.tar.gz"
        
        if not os.path.exists(package_path):
            # Fallback: create package on-the-fly
            temp_package = "/tmp/depl0y-update.tar.gz"
            create_package_cmd = f"""
cd /home/administrator/depl0y && \
tar -czf {temp_package} \
  --exclude='node_modules' \
  --exclude='dist' \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='venv' \
  backend/ frontend/ *.md *.sh 2>/dev/null || true
"""
            subprocess.run(create_package_cmd, shell=True, check=True)
            package_path = temp_package

        if not os.path.exists(package_path):
            raise HTTPException(status_code=500, detail="Failed to find or create update package")

        return FileResponse(
            package_path,
            media_type="application/gzip",
            filename="depl0y-latest.tar.gz",
            headers={
                "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )

    except Exception as e:
        logger.error(f"Failed to serve update package: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to serve update package: {str(e)}"
        )


@router.post("/apply")
def apply_update(current_user=Depends(get_current_user)):
    """Download and apply update from main server"""
    try:
        logger.info("Starting update process...")

        # Download update package
        download_url = f"{UPDATE_SERVER}/api/v1/system-updates/download"
        package_path = "/tmp/depl0y-update.tar.gz"

        logger.info(f"Downloading update from {download_url}")

        # Use requests with authentication from current session
        response = requests.get(download_url, stream=True, timeout=300)
        if response.status_code != 200:
            raise Exception(f"Download failed with status {response.status_code}")

        # Save package
        with open(package_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logger.info("Update package downloaded successfully")

        # Create backup
        backup_script = """
#!/bin/bash
BACKUP_DIR="/opt/depl0y-backups/backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r /opt/depl0y/backend "$BACKUP_DIR/"
cp -r /opt/depl0y/frontend "$BACKUP_DIR/"
echo "Backup created at $BACKUP_DIR"
"""
        subprocess.run(backup_script, shell=True, check=True)
        logger.info("Backup created")

        # Extract update
        extract_script = f"""
cd /tmp && \\
tar -xzf {package_path} && \\
sudo systemctl stop depl0y-backend && \\
sudo cp -r backend/* /opt/depl0y/backend/ && \\
sudo chown -R depl0y:depl0y /opt/depl0y/backend && \\
sudo chmod -R 755 /opt/depl0y/backend && \\
cd frontend && npm install && npm run build && \\
sudo rm -rf /opt/depl0y/frontend/dist/* && \\
sudo cp -r dist/* /opt/depl0y/frontend/dist/ && \\
sudo chown -R www-data:www-data /opt/depl0y/frontend/dist/ && \\
sudo chmod -R 755 /opt/depl0y/frontend/dist/ && \\
sudo systemctl start depl0y-backend && \\
rm {package_path}
"""

        # Execute update in background
        subprocess.Popen(extract_script, shell=True)

        return {
            "success": True,
            "message": "Update is being applied. The service will restart automatically."
        }

    except Exception as e:
        logger.error(f"Failed to apply update: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to apply update: {str(e)}"
        )
