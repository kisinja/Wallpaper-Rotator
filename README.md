# Wallpaper Rotator — Car Aesthetic Edition

Automatically refreshes your Windows desktop background (and lock screen)
with a new car-aesthetic photo (Porsche, Bugatti, Koenigsegg, and other
supercars/automotive art), on whatever schedule you want (default: every
6 hours). Adjusts the mood based on current weather, can be triggered
on-demand from your phone via Telegram, and has a local web gallery to
browse history and save favorites.

## What's in this folder
- `wallpaper_rotator.py` — fetches a photo from Pexels (weather-aware),
  sets it as your desktop wallpaper, and syncs it to your lock screen
- `set_lockscreen.ps1` — PowerShell helper that applies the lock screen image
- `telegram_bot.py` — listens for messages from your phone to trigger an
  instant rotation on demand
- `gallery.py` — local web app to browse wallpaper history and save favorites
- `setup_task.bat` — registers the Windows scheduled task for the
  automatic rotation
- `.env` — holds your Pexels and Telegram credentials (not committed to Git)
- `.gitignore` — keeps `.env`, `history.json`, and other local files out of your repo
- `README.md` — this file

## Setup (10–15 minutes)

### 1. Install Python (skip if you already have it)
Download from https://python.org — during install, check **"Add Python to PATH"**.

### 2. Install the dependencies
Open Command Prompt and run:

4. To start it immediately without logging out/in: open Task Scheduler
   (`taskschd.msc`), find **WallpaperBot**, right-click → **Run**

From then on, the bot starts automatically every time you log into
Windows and keeps listening for your messages in the background (locking
your PC doesn't stop it — only logging off or restarting does).

## Gallery (browse history & save favorites)
A local web app to see everything the rotator has pulled and permanently
save the ones you like — favorites are never touched by the auto-cleanup
that limits the main history to 10 files.

### Run it

Then open **http://localhost:5000** in a browser. Click **❤️ Save** on any
wallpaper to copy it into `Pictures\AutoWallpapers\favorites`, where it'll
stay indefinitely.

### View it from your phone
Since the server listens on all network interfaces, it's reachable from
any device on the same WiFi:
1. On your PC, run `ipconfig` in Command Prompt and find your **IPv4 Address**
   (e.g. `192.168.1.42`)
2. On your phone (same WiFi), visit `http://192.168.1.42:5000`

To reach it from outside your home WiFi too, a tool like **Tailscale**
can make this address reachable from anywhere without exposing it
publicly — ask if you want help setting that up.

## Managing the scheduled tasks
- Open Task Scheduler (`Win + R` → `taskschd.msc`) to find **WallpaperRotator**
  (timed rotation) and **WallpaperBot** (Telegram listener) under the
  Task Scheduler Library — pause, edit, or delete either from there.
- To remove them via command line:

## Pushing to GitHub
The `.env` file, `history.json`, and anything else listed in `.gitignore`
will **not** be committed, so it's safe to push this whole folder. Anyone
who clones the repo just needs to create their own `.env` file with their
own Pexels key and (optionally) Telegram bot credentials to run it.

## Notes
- Pexels' free tier allows 200 requests/hour and 20,000/month — far more
  than this project needs even with the Telegram bot and gallery running
  alongside the scheduled rotation.
- The script avoids repeating recent photos by remembering the last 40
  photo IDs in `history.json`.
- Weather lookups use Open-Meteo, which requires no API key or signup.
- The Telegram bot only responds to messages from the chat ID in your
  `.env` file — messages from anyone else are silently ignored.
- Everything runs locally — no data leaves your machine except requests
  to Pexels (photo), Open-Meteo (weather), and Telegram (bot messages).