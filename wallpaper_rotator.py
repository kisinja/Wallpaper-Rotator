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
# ---------------- CONFIG ----------------
WALLHAVEN_API_KEY = os.environ.get(
    "WALLHAVEN_API_KEY", ""
)  # optional, works without one

QUERIES = [
    "porsche",
    "sports car",
    "supercar",
    "car blueprint art",
    "jdm car",
    "automotive poster art",
    "car aesthetic wallpaper",
]

SAVE_DIR = Path.home() / "Pictures" / "AutoWallpapers"
HISTORY_FILE = SAVE_DIR / "history.json"
MAX_HISTORY = 40
KEEP_LAST_N_FILES = 10
# -----------------------------------------   # how many downloaded images to keep on disk
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
        [f for f in SAVE_DIR.glob("wallpaper_*.*")],
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
    url = "https://wallhaven.cc/api/v1/search"
    params = {
        "q": query,
        "categories": "111",  # general + anime + people
        "purity": "100",  # SFW only
        "sorting": "random",
        "atleast": "1080x1920",  # decent quality for a laptop wallpaper
    }
    if WALLHAVEN_API_KEY:
        params["apikey"] = WALLHAVEN_API_KEY

    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    results = resp.json().get("data", [])

    if not results:
        raise RuntimeError(f"No results found for query '{query}'")

    history = get_history()
    unseen = [w for w in results if w["id"] not in history]
    choice = random.choice(unseen) if unseen else random.choice(results)

    img_url = choice["path"]
    wallpaper_id = choice["id"]

    img_resp = requests.get(img_url, timeout=30)
    img_resp.raise_for_status()

    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    ext = img_url.split(".")[-1]
    filename = SAVE_DIR / f"wallpaper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    filename.write_bytes(img_resp.content)

    history.append(wallpaper_id)
    save_history(history)
    cleanup_old_files()

    print(
        f"Downloaded: {filename.name}  (Wallhaven ID: {wallpaper_id}, query: '{query}')"
    )
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
