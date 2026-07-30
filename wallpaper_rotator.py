"""
Wallpaper Rotator - Street Style / Fashion Edition
----------------------------------------------------
Fetches a fresh street-style / fashion-editorial photo from Unsplash
and sets it as your Windows desktop wallpaper. Designed to be run on
a schedule (every 6 hrs, daily, etc.) via Windows Task Scheduler.

SETUP (one-time):
1. Get a free Unsplash API key: https://unsplash.com/developers
   -> Create an app -> copy the "Access Key"
2. pip install requests
3. Paste your Access Key below where it says YOUR_ACCESS_KEY_HERE
   (or set it as an environment variable UNSPLASH_ACCESS_KEY instead)
4. Run this file once manually to test: python wallpaper_rotator.py
5. Use setup_task.bat to schedule it automatically (see README.md)
"""

import os
import sys
import random
import ctypes
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

import requests

# ---------------- CONFIG ----------------
load_dotenv()
ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "YOUR ACCESS KEY HERE")

# Feel free to tweak/add search terms to steer the style further
QUERIES = [
    "beautiful city aesthetic",
    "aesthetic cityscape night",
    "old European city street",
    "scenic city skyline",
    "vintage jazz club",
    "old jazz aesthetic",
    "1920s jazz bar",
    "moody city street photography",
]

SAVE_DIR = Path.home() / "Pictures" / "AutoWallpapers"
HISTORY_FILE = SAVE_DIR / "history.json"
MAX_HISTORY = 40          # how many past photo IDs to remember (avoids repeats)
KEEP_LAST_N_FILES = 10    # how many downloaded images to keep on disk
# -----------------------------------------


def get_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text())
        except json.JSONDecodeError:
            return []
    return []


def save_history(history):
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(history[-MAX_HISTORY:]))


def cleanup_old_files():
    """Keep only the most recent N downloaded wallpapers to avoid clutter."""
    if not SAVE_DIR.exists():
        return
    files = sorted(
        [f for f in SAVE_DIR.glob("wallpaper_*.jpg")],
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    for old_file in files[KEEP_LAST_N_FILES:]:
        try:
            old_file.unlink()
        except OSError:
            pass


def fetch_wallpaper():
    query = random.choice(QUERIES)
    url = "https://api.unsplash.com/photos/random"
    params = {
        "query": query,
        "orientation": "landscape",
        "content_filter": "high",
        "client_id": ACCESS_KEY,
    }

    history = get_history()
    data = None
    for _ in range(5):  # try up to 5 times to avoid a repeat
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        candidate = resp.json()
        if candidate["id"] not in history:
            data = candidate
            break
        data = candidate  # fall back to last fetched if all attempts repeat

    img_url = data["urls"]["full"]
    photo_id = data["id"]
    photographer = data["user"]["name"]

    img_resp = requests.get(img_url, timeout=30)
    img_resp.raise_for_status()

    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    filename = SAVE_DIR / f"wallpaper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    filename.write_bytes(img_resp.content)

    history.append(photo_id)
    save_history(history)
    cleanup_old_files()

    print(f"Downloaded: {filename.name}  (photo by {photographer} on Unsplash, query: '{query}')")
    return filename


def set_wallpaper(path: Path):
    """Windows-only: sets the desktop background via the Win32 API."""
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDCHANGE = 0x02
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, str(path), SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )


def main():
    if ACCESS_KEY == "YOUR_ACCESS_KEY_HERE":
        print("ERROR: You haven't set your Unsplash Access Key yet.")
        print("Open wallpaper_rotator.py and paste it in, or set the")
        print("UNSPLASH_ACCESS_KEY environment variable. See README.md.")
        sys.exit(1)

    try:
        img_path = fetch_wallpaper()
        set_wallpaper(img_path)
        print("Wallpaper updated successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Network/API error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to update wallpaper: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
