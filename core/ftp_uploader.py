import os
from ftplib import FTP

def upload_directory(local_path, remote_path, ip, logger, port=21, user="xbox", password="xbox"):
    logger(f"Connecting to Xbox FTP at {ip}:{port}")
    ftp = FTP()
    ftp.connect(ip, port)
    ftp.login(user, password)

    #navega para o diretorio /F/games
    try:
        ftp.cwd(remote_path)
    except Exception as e:
        logger(f"Failed to change directory to {remote_path}: {e}")
        return
    
    logger(f"Connected to {ip}:{port} and changed directory to {remote_path}")
    logger("Starting FTP upload...")

    # Upload de arquivos da pasta local
    for root, _, files in os.walk(local_path):
        rel_path = os.path.relpath(root, local_path)
        # verifica se o caminho remoto está dentro da pasta F/Games
        if not rel_path.startswith("F/Games"):
            logger(f"Skipping {rel_path} as it is outside the target directory.")
            continue
        
        if rel_path != ".":
            try:
                ftp.mkd(rel_path)
            except:
                pass
            ftp.cwd(rel_path)

        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                logger(f"Uploading {file}...")
                ftp.storbinary(f"STOR {file}", f)

        if rel_path != ".":
            ftp.cwd("..")

    ftp.quit()
    logger("FTP upload finished.")
