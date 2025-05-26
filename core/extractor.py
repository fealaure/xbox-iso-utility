import os
import subprocess
import zipfile
import json
import urllib.request
from io import BytesIO
from core.config import XISO_EXE, GITHUB_API_URL

def ensure_extract_xiso(logger):
    if os.path.exists(XISO_EXE):
        logger("extract-xiso.exe found.")
        return

    logger("Downloading extract-xiso.exe from GitHub...")
    with urllib.request.urlopen(GITHUB_API_URL) as response:
        release = json.load(response)
        for asset in release["assets"]:
            if 'extract-xiso-Win64_Release.zip' in asset["name"]:
                download_url = asset["browser_download_url"]
                break
        else:
            raise Exception("No compatible Windows release found.")

    with urllib.request.urlopen(download_url) as response:
        zip_data = BytesIO(response.read())

    with zipfile.ZipFile(zip_data) as zip_file:
        zip_file.extractall(os.path.dirname(XISO_EXE))

    if not os.path.exists(XISO_EXE):
        raise Exception("extract-xiso.exe not found after download.")

    logger("extract-xiso.exe is ready.")

def extract_iso(iso_path, logger):
    logger(f"Extracting ISO: {iso_path}")
    subprocess.run([XISO_EXE, "-x", iso_path], check=True)
