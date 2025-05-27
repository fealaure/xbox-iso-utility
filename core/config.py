import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
XISO_EXE = os.path.join(PROJECT_ROOT, "artifacts/extract-xiso.exe")
GITHUB_API_URL = "https://api.github.com/repos/XboxDev/extract-xiso/releases/latest"
ISO_DIR = "isos"
EXTRACTED_DIR = "extracted"
FTP_DEST = "/F/Games/"

