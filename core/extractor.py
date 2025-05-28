import os
import platform
import subprocess
import zipfile
import json
import urllib.request
from io import BytesIO
from core.config import XISO_BINARY, GITHUB_API_URL, IS_WINDOWS

def ensure_extract_xiso(logger):
    if os.path.exists(XISO_BINARY):
        logger("extract-xiso found.")
        return

    logger("🖥️ Detected OS: Windows" if IS_WINDOWS else "🖥️ Detected OS: macOS")
    logger("Downloading extract-xiso from GitHub...")

    with urllib.request.urlopen(GITHUB_API_URL) as response:
        release = json.load(response)
        download_url = None

        for asset in release["assets"]:
            if IS_WINDOWS and 'extract-xiso-Win64_Release.zip' in asset["name"]:
                download_url = asset["browser_download_url"]
                break
            elif not IS_WINDOWS and 'macOS' in asset["name"] and asset["name"].endswith(".zip"):
                download_url = asset["browser_download_url"]
                break

        if not download_url:
            raise Exception("❌ No compatible release found for your OS.")

    with urllib.request.urlopen(download_url) as response:
        zip_data = BytesIO(response.read())

    with zipfile.ZipFile(zip_data) as zip_file:
        zip_file.extractall(os.path.dirname(XISO_BINARY))

    if not IS_WINDOWS:
        extracted_files = os.listdir(os.path.dirname(XISO_BINARY))
        for file in extracted_files:
            full_path = os.path.join(os.path.dirname(XISO_BINARY), file)
            if os.path.isfile(full_path) and "extract-xiso" in file and not file.endswith(".zip"):
                os.chmod(full_path, 0o755)
                logger(f"extract-xiso is ready at: {full_path}")
                break
        else:
            raise Exception("extract-xiso binary not found after extraction.")
    else:
        if not os.path.exists(XISO_BINARY):
            raise Exception("extract-xiso.exe not found after download.")
        logger("extract-xiso.exe is ready.")

def extract_iso(iso_path, logger, output_dir=None):
    logger(f"Extracting ISO: {iso_path}")

    iso_path = os.path.abspath(iso_path)
    os.makedirs(output_dir, exist_ok=True)

    try:
        result = subprocess.run(
            [XISO_BINARY, "-x", iso_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=output_dir
        )

        if result.returncode != 0:
            logger("❌ extract-xiso failed!")
            logger(f"stderr: {result.stderr}")
            raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout, stderr=result.stderr)

        logger("✅ Extraction successful.")

    finally:
        pass
