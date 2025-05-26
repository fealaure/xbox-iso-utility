import os
from core.extractor import ensure_extract_xiso, extract_iso
from core.ftp_uploader import upload_directory

ISO_DIR = "isos"
EXTRACTED_DIR = "extracted"
FTP_DEST = "/F/Games"

def main():
    print("=== Xbox ISO Utility ===\n")

    os.makedirs(ISO_DIR, exist_ok=True)
    os.makedirs(EXTRACTED_DIR, exist_ok=True)

    # 1. Ensure extract-xiso is available
    ensure_extract_xiso(print)

    # 2. Ask for IP manually
    user_ip = input("Enter your Xbox IP address: ").strip()
    if user_ip:
        xbox_ip = user_ip

    print(f"\n📡 Using Xbox IP: {xbox_ip}\n")

    # 3. Process all .iso files in the folder
    for filename in os.listdir(ISO_DIR):
        if not filename.lower().endswith(".iso"):
            continue

        iso_path = os.path.join(ISO_DIR, filename)
        game_name = os.path.splitext(filename)[0]
        extracted_path = os.path.join(EXTRACTED_DIR, game_name)

        print(f"📁 Processing {filename}")

        if not os.path.exists(extracted_path):
            print("🗂️ Extracting...")
            extract_iso(iso_path, print)
        else:
            print("✅ Already extracted.")

        print("🚀 Uploading via FTP...")
        upload_directory(extracted_path, f"{FTP_DEST}/{game_name}", xbox_ip, print)
        print("✅ Done!\n")

    print("🎉 All games processed and uploaded!")

if __name__ == "__main__":
    main()
