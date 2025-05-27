import os
from core.extractor import ensure_extract_xiso, extract_iso
from core.ftp_uploader import upload_directory
from utils.config import load_config, save_config

ISO_DIR = "isos"
EXTRACTED_DIR = "extracted"
FTP_DEST = "/F/Games"

def main():
    print("=== Xbox ISO Utility ===\n")

    os.makedirs(ISO_DIR, exist_ok=True)
    os.makedirs(EXTRACTED_DIR, exist_ok=True)

    # 1. Ensure extract-xiso is available
    ensure_extract_xiso(print)

    # 2. Load config
    config = load_config()
    xbox_ip = config.get("xbox_ip")
    xbox_port = config.get("xbox_port", 21)

    if xbox_ip and xbox_port:
        print(f"📡 Saved IP: {xbox_ip}")
        print(f"🔌 Saved Port: {xbox_port}")

        use_saved = input("Use saved IP and port? (Y/n): ").strip().lower()
    
        if use_saved != "n":
            print(f"\n📡 Using Xbox IP: {xbox_ip}")
            print(f"🔌 Using FTP port: {xbox_port}\n")
        else:
            xbox_ip = None
            xbox_port = None
    
    else:
        xbox_ip = None
        xbox_port = None

    if not xbox_ip:
        xbox_ip = input("Enter your Xbox IP address: ").strip()
        port_input = input("Enter FTP port (default is 21): ").strip()
        xbox_port = int(port_input) if port_input else 21

        config["xbox_ip"] = xbox_ip
        config["xbox_port"] = xbox_port
        save_config(config)

        print(f"\n📡 Using Xbox IP: {xbox_ip}")
        print(f"🔌 Using FTP port: {xbox_port}\n")

    # 3. Process all .iso files in the folder
    iso_files = [f for f in os.listdir(ISO_DIR) if f.lower().endswith(".iso")]
    print(f"Found {len(iso_files)} ISO(s) to process.\n")

    for index, filename in enumerate(iso_files, 1):
        print(f"=== [{index}/{len(iso_files)}] Processing {filename} ===")
        
        iso_path = os.path.join(ISO_DIR, filename)
        game_name = os.path.splitext(filename)[0]
        extracted_path = os.path.join(EXTRACTED_DIR, game_name)

        if not os.path.exists(extracted_path):
            print("🗂️ Extracting...")
            extract_iso(iso_path, print, output_dir=EXTRACTED_DIR)
        else:
            print("✅ Already extracted.")

        print("🚀 Uploading via FTP...")
        upload_directory(EXTRACTED_DIR, f"{FTP_DEST}/{game_name}", xbox_ip, print, port=xbox_port)
        print("✅ Done!\n")

    print("🎉 All games processed and uploaded!")
    print("Cleaning started...\n")
    for game_name in os.listdir(EXTRACTED_DIR):
        game_path = os.path.join(EXTRACTED_DIR, game_name)
        if os.path.isdir(game_path):
            print(f"🗑️ Cleaning up extracted directory: {game_path}")
            os.rmdir(game_path)

    print("🗑️ Cleaned up extracted directories.\n")

if __name__ == "__main__":
    main()
