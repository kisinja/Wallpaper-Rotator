# Wallpaper Rotator — Car Aesthetic Edition

Automatically refreshes your Windows desktop background (and lock screen)
with a new car-aesthetic photo (Porsche, Bugatti, Koenigsegg, and other
supercars/automotive art), on whatever schedule you want (default: every
6 hours). Also adjusts the mood based on current weather, and can be
triggered on-demand from your phone via Telegram.

## What's in this folder
- `wallpaper_rotator.py` — fetches a photo from Wallhaven (weather-aware),
  sets it as your desktop wallpaper, and syncs it to your lock screen
- `set_lockscreen.ps1` — PowerShell helper that applies the lock screen image
- `telegram_bot.py` — listens for messages from your phone to trigger an
  instant rotation on demand
- `setup_task.bat` — registers the Windows scheduled task for the
  automatic rotation
- `.env` — holds your Wallhaven and Telegram credentials (not committed to Git)
- `.gitignore` — keeps `.env` and other local files out of your repo
- `README.md` — this file

## Setup (10–15 minutes)

### 1. Install Python (skip if you already have it)
Download from https://python.org — during install, check **"Add Python to PATH"**.

### 2. Install the dependencies
Open Command Prompt and run:

### 3. (Optional) Get a free Wallhaven API key
Wallhaven works **without** a key for basic searches — you can skip this
step entirely and the script will still work. An API key just raises your
rate limit if you end up wanting more frequent refreshes later.

1. Go to https://wallhaven.cc and sign in / sign up
2. Go to **Account Settings → API** and copy your key

### 4. Set up your `.env` file
Create a file named `.env` in this folder:

Leave `WALLHAVEN_API_KEY` blank if you skipped step 3. See the **Telegram
bot setup** section below for how to fill in the other two.

This file is already excluded from Git via `.gitignore`, so it stays local
to your machine.

### 5. Test the wallpaper rotation manually
Double-click `wallpaper_rotator.py`, or run from Command Prompt:

Your desktop wallpaper and lock screen should both update. Downloaded
images are saved to `Pictures\AutoWallpapers` (only the last 10 are kept,
older ones auto-delete).

### 6. Schedule automatic rotation
Right-click `setup_task.bat` → **"Run as administrator"**.
This registers a Windows Scheduled Task called **WallpaperRotator** that runs
every 6 hours from midnight (00:00, 06:00, 12:00, 18:00).

Want it daily instead? Open `setup_task.bat` in a text editor, comment out
the `/sc HOURLY /mo 6` line and uncomment the `DAILY` line right below it
(you can also just change the time in that line), then re-run the .bat.

## Customizing the style
Inside `wallpaper_rotator.py`, the `QUERIES` list controls what kind of
photos get pulled by default:
```python
QUERIES = [
    "porsche dark",
    "porsche 911 gt",
    "bugatti chiron",
    "bugatti veyron",
    "koenigsegg agera",
    "koenigsegg jesko",
    "hypercar",
    "supercar dark",
    "car blueprint",
    "automotive poster",
]
```
Add, remove, or edit these terms any time to steer the vibe — e.g. add
`"ferrari"`, `"lamborghini aesthetic"`, or `"car wallpaper 4k"` for a
narrower look. Mix in more of one theme by just repeating similar terms —
more entries for a theme means it gets picked more often. Keep queries
short (1–2 words); Wallhaven requires **all** words in a query to match,
so longer phrases can return zero results on some runs.

## Weather-linked mood
The script checks current weather near you (via the free Open-Meteo API,
no key needed) and picks from a different query set depending on
conditions — bright shots on clear days, darker/moodier shots when it's
overcast, rainy, or stormy:
```python
WEATHER_QUERY_SETS = {
    "clear": [...],
    "cloudy": [...],
    "rain": [...],
    "storm": [...],
}
```
Edit any of these lists in `wallpaper_rotator.py` the same way you'd edit
`QUERIES`. If the weather API is ever unreachable, it safely falls back to
the "cloudy" set so a rotation never fails because of it. The location
used is set near the top of `get_weather_mood()` — update the `lat, lon`
values if you're not in Thika, Kenya.

## Lock screen sync
Every rotation also updates your Windows lock screen to match the new
desktop wallpaper, using `set_lockscreen.ps1` behind the scenes. No setup
needed — it runs automatically as part of `wallpaper_rotator.py`. Lock
your PC (`Win + L`) after a test run to confirm it's showing the new image.

## Telegram bot (trigger from your phone)
Message your bot from anywhere to force an instant wallpaper rotation,
independent of the 6-hour schedule.

### Setup
1. In Telegram, message **@BotFather** → send `/newbot` → follow the
   prompts to name your bot → copy the **token** it gives you
2. Message your new bot anything (e.g. "hi")
3. In a browser, visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   and find `"chat":{"id":...}` — that number is your chat ID
4. Add both values to your `.env` file:

### Test it manually

Leave it running, then message your bot `/rotate` or `new wallpaper` from
your phone. Your wallpaper should update within seconds, with a
confirmation reply back in Telegram. Press `Ctrl+C` to stop the test.

### Run it automatically at every login
Once the manual test works, register it as a "run at logon" task (this is
different from the timed `WallpaperRotator` task — the bot needs to run
continuously in the background, not on a fixed schedule):

1. Find your Python path: `where pythonw`
2. Find the bot script's full path: right-click `telegram_bot.py` →
   **Copy as path**
3. Open Command Prompt **as administrator** and run (substituting your
   real paths):

   4. To start it immediately without logging out/in: open Task Scheduler
   (`taskschd.msc`), find **WallpaperBot**, right-click → **Run**

From then on, the bot starts automatically every time you log into
Windows and keeps listening for your messages in the background (locking
your PC doesn't stop it — only logging off or restarting does).

## Managing the scheduled tasks
- Open Task Scheduler (`Win + R` → `taskschd.msc`) to find **WallpaperRotator**
  (timed rotation) and **WallpaperBot** (Telegram listener) under the
  Task Scheduler Library — pause, edit, or delete either from there.
- To remove them via command line:

## Pushing to GitHub
The `.env` file (and anything else listed in `.gitignore`) will **not** be
committed, so it's safe to push this whole folder. Anyone who clones the
repo just needs to create their own `.env` file with their own Wallhaven
key (optional) and Telegram bot credentials (only needed if they want the
phone-trigger feature) to run it.

## Notes
- Wallhaven works without an API key; with one, rate limits are higher.
- The script avoids repeating recent photos by remembering the last 40
  wallpaper IDs in `history.json`.
- Weather lookups use Open-Meteo, which requires no API key or signup.
- The Telegram bot only responds to messages from the chat ID in your
  `.env` file — messages from anyone else are silently ignored.
- Everything runs locally — no data leaves your machine except requests
  to Wallhaven (photo), Open-Meteo (weather), and Telegram (bot messages).