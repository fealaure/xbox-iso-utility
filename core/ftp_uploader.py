import os
from ftplib import FTP
import re

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

    # navigate to the base directory
    try:
        ftp.cwd("F")
        ftp.cwd("games")
    except Exception as e:
        logger(f"Failed to change directory to {remote_path}: {e}")
        return

    logger(f"Connected to {ip}:{port} and changed directory to {remote_path}")
    logger("Starting FTP upload...")

    for root, _, files in os.walk(local_path):
        rel_path = os.path.relpath(root, local_path)
        rel_path = rel_path.replace("\\", "/")
        rel_path = rel_path.replace(" ", "_")
        rel_path = "".join(c for c in rel_path if c.isalnum() or c in ('.', '_', '/'))
        rel_path = rel_path.replace("__", "_")
        logger(f"Preparing to upload files from: {rel_path}")

        # Garantee the remote directory exists
        if rel_path != ".":
            ensure_ftp_dirs(ftp, rel_path, logger)

        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                logger(f"Uploading {file}...")
                ftp.storbinary(f"STOR {file}", f)

        # Change to the parent directory for the next iteration
        if rel_path != ".":
            ftp.cwd("/F/games")

    ftp.quit()
    logger("FTP upload finished.")
