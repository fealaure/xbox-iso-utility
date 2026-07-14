import os
import platform

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
IS_WINDOWS = platform.system().lower() == "windows"
IS_MAC = platform.system().lower() == "darwin"
IS_LINUX = platform.system().lower() == "linux"
XISO_FILENAME = "extract-xiso.exe" if IS_WINDOWS else "extract-xiso"
XISO_BINARY = os.path.join(PROJECT_ROOT, "artifacts", XISO_FILENAME)
GITHUB_API_URL = "https://api.github.com/repos/XboxDev/extract-xiso/releases/latest"
ISO_DIR = "isos"
EXTRACTED_DIR = "extracted"
FTP_DEST = "/F/Games/"

# Original Xbox uses the FATX filesystem, which caps file/folder names at 42 characters.
# Names longer than this cause the dashboard to fail to read the directory entry.
MAX_FATX_NAME_LENGTH = 42

