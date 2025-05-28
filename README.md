# Xbox ISO Utility

A command-line tool written in Python to extract original Xbox ISO files and upload them via FTP to a modded Xbox console.
This tool is compatible with Windows, Linux and MacOS

This project automates the process of:
1. Extracting Redump-compatible Xbox ISOs using `extract-xiso`;
2. Uploading the extracted folder directly to the desired path on the Xbox (e.g. `F:/Games`);
3. Saving your Xbox IP and FTP port in a config file for future use.

---

## 🔧 Requirements

- Python 3.8+
- A modded Xbox console with FTP access (e.g. UnleashX, Avalaunch, etc.)
- `extract-xiso.exe` (automatically downloaded on first run)
- An active network connection between your PC and the Xbox

---

## 📂 Project Structure

```
xbox_uploader/
├── main.py                # Main script (entry point)
├── core/
│   ├── config.py          # Paths and constants
│   ├── extractor.py       # ISO extraction logic
│   └── ftp_uploader.py    # FTP upload logic
├── utils/
│   └── config.py          # Load/save user config (IP, port)
├── isos/                  # Place your .iso files here
├── extracted/             # Extracted folders will be created here
├── config.json            # Stores your Xbox IP and FTP port (auto-generated)
```

---

## ▶️ How to Use

1. Clone or download this repository.
2. Place your Redump-compatible Xbox `.iso` files in the `isos/` directory.
3. Run the script:

```bash
python main.py
```

4. On the first run:
   - You will be asked for your Xbox IP and FTP port;
   - These values will be saved to `config.json` for future runs.

5. The script will:
   - Extract each `.iso` to a subfolder in `extracted/`;
   - Upload the folder to the configured path on your Xbox (default: `F:/Games`).

---

## 💾 Where Are Games Installed?

By default, games are uploaded to:

```
/F/Games/GameFolder
```

If your Xbox uses a different drive (like `E:/Games`), just edit the `FTP_DEST` variable in `main.py`.

---

## 💡 Notes

- This tool does not support `.iso` files that are not in original Xbox format.
- You can cancel and re-run the script safely; it skips already extracted games.
