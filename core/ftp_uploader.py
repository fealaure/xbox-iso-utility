import os
from ftplib import FTP

def upload_directory(local_path, remote_path, ip, logger, user="xbox", password="xbox"):
    logger(f"Connecting to Xbox FTP at {ip}")
    ftp = FTP(ip)
    ftp.login(user, password)

    try:
        ftp.cwd(remote_path)
    except:
        ftp.mkd(remote_path)
        ftp.cwd(remote_path)

    for root, _, files in os.walk(local_path):
        rel_path = os.path.relpath(root, local_path)
        if rel_path != ".":
            try: ftp.mkd(rel_path)
            except: pass
            ftp.cwd(rel_path)

        for file in files:
            with open(os.path.join(root, file), "rb") as f:
                ftp.storbinary(f"STOR {file}", f)

        if rel_path != ".":
            ftp.cwd("..")

    ftp.quit()
    logger("FTP upload finished.")
