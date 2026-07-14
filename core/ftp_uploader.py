import os
from ftplib import FTP
import re
from core.config import MAX_FATX_NAME_LENGTH

def sanitize_fatx_component(name, max_length=MAX_FATX_NAME_LENGTH):
    """Sanitize a single path component (folder or file name) for the Xbox's FATX filesystem."""
    name = name.strip().replace(" ", "_")
    name = "".join(c for c in name if c.isalnum() or c in (".", "_"))
    while "__" in name:
        name = name.replace("__", "_")

    if len(name) <= max_length:
        return name

    base, ext = os.path.splitext(name)
    if ext and len(ext) < max_length:
        return base[: max_length - len(ext)] + ext
    return name[:max_length]

def ensure_ftp_dirs(ftp, path, logger):
    dirs = path.strip("/").split("/")
    for d in dirs:
        if d == "." or d == "":
            continue
        try:
            current_dir = ftp.pwd()
            logger(f"Checking directory: {current_dir}/{d}")
            ftp.cwd(d)
        except Exception:
            try:
                logger(f"Creating remote directory: {d}")
                ftp.mkd(d)
                ftp.cwd(d)
            except Exception as e:
                logger(f"Error creating directory {d}: {e}")
                raise Exception(f"Failed to create directory {d} on FTP server: {e}")

def upload_directory(local_path, remote_path, ip, logger, port=21, user="xbox", password="xbox"):
    logger(f"Connecting to Xbox FTP at {ip}:{port}")
    ftp = FTP()
    ftp.connect(ip, port)
    ftp.login(user, password)

    # Navigate to (creating if needed) the destination directory for this game
    try:
        remote_parts = [sanitize_fatx_component(p) for p in remote_path.strip("/").split("/") if p]
        ftp.cwd("/")
        for part in remote_parts:
            try:
                ftp.cwd(part)
            except Exception:
                ftp.mkd(part)
                ftp.cwd(part)
        base_remote_dir = ftp.pwd()
    except Exception as e:
        logger(f"Failed to change directory to {remote_path}: {e}")
        return

    logger(f"Connected to {ip}:{port} and changed directory to {base_remote_dir}")
    logger("Starting FTP upload...")

    for root, _, files in os.walk(local_path):
        rel_path = os.path.relpath(root, local_path)
        rel_path = rel_path.replace("\\", "/")

        if rel_path != ".":
            parts = [sanitize_fatx_component(p) for p in rel_path.split("/") if p not in ("", ".")]
            rel_path = "/".join(parts)

        logger(f"Preparing to upload files from: {rel_path}")

        # Garantee the remote directory exists
        if rel_path != ".":
            ensure_ftp_dirs(ftp, rel_path, logger)

        for file in files:
            file_path = os.path.join(root, file)
            remote_name = sanitize_fatx_component(file)
            with open(file_path, "rb") as f:
                logger(f"Uploading {file} as {remote_name}...")
                ftp.storbinary(f"STOR {remote_name}", f)

        # Change back to the game's base directory for the next iteration
        if rel_path != ".":
            ftp.cwd(base_remote_dir)

    ftp.quit()
    logger("FTP upload finished.")
