"""
Telegram remote trigger for Wallpaper Rotator.
Runs continuously in the background — message the bot from your phone
to trigger an instant wallpaper rotation.
"""

import os
import time
import subprocess
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
SCRIPT_DIR = Path(__file__).parent
ROTATOR_SCRIPT = SCRIPT_DIR / "wallpaper_rotator.py"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(text):
    requests.post(f"{API_URL}/sendMessage", data={"chat_id": CHAT_ID, "text": text})


def trigger_rotation():
    result = subprocess.run(["python", str(ROTATOR_SCRIPT)], capture_output=True, text=True)
    if result.returncode == 0:
        send_message("🚗 Wallpaper updated!")
    else:
        send_message(f"⚠️ Failed to update wallpaper:\n{result.stderr[-300:]}")


def main():
    if not BOT_TOKEN or not CHAT_ID:
        print("ERROR: Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in your .env file.")
        return

    print("Telegram wallpaper bot running... (Ctrl+C to stop)")
    offset = None

    while True:
        try:
            resp = requests.get(
                f"{API_URL}/getUpdates",
                params={"offset": offset, "timeout": 30},
                timeout=35
            )
            for update in resp.json().get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                chat_id = str(message.get("chat", {}).get("id", ""))
                text = message.get("text", "").strip().lower()

                if chat_id != str(CHAT_ID):
                    continue  # ignore anyone but you

                if text in ("/newwallpaper", "/rotate", "new wallpaper"):
                    send_message("Fetching a new wallpaper...")
                    trigger_rotation()

        except requests.exceptions.RequestException:
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()