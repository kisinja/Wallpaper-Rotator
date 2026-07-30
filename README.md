# Wallpaper Rotator — Cities & Old Jazz Aesthetic Edition

Automatically refreshes your Windows desktop background with a new
scenic-city or old-jazz-aesthetic photo, on whatever schedule you want
(default: every 6 hours).

## What's in this folder
- `wallpaper_rotator.py` — fetches a photo from Unsplash and sets it as your wallpaper
- `setup_task.bat` — registers the Windows scheduled task so it runs automatically
- `README.md` — this file

## Setup (5 minutes)

### 1. Install Python (skip if you already have it)
Download from https://python.org — during install, check **"Add Python to PATH"**.

### 2. Install the one dependency
Open Command Prompt and run:
```
pip install requests
```

### 3. Get a free Unsplash API key
1. Go to https://unsplash.com/developers and sign in / sign up
2. Click **"New Application"**, accept the terms, name it anything (e.g. "My Wallpaper Rotator")
3. Copy the **Access Key** shown on the app's page

### 4. Add your key to the script
Open `wallpaper_rotator.py` in any text editor and replace:
```python
ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "YOUR_ACCESS_KEY_HERE")
```
with your key in place of `YOUR_ACCESS_KEY_HERE`.

(Alternatively, set it as a permanent environment variable named
`UNSPLASH_ACCESS_KEY` if you don't want the key sitting in the file.)

### 5. Test it once manually
Double-click `wallpaper_rotator.py`, or run from Command Prompt:
```
python wallpaper_rotator.py
```
Your wallpaper should change immediately. Downloaded images are saved to
`Pictures\AutoWallpapers` (only the last 10 are kept, older ones auto-delete).

### 6. Schedule it
Right-click `setup_task.bat` → **"Run as administrator"**.
This registers a Windows Scheduled Task called **WallpaperRotator** that runs
every 6 hours from midnight (00:00, 06:00, 12:00, 18:00).

Want it daily instead? Open `setup_task.bat` in a text editor, comment out
the `/sc HOURLY /mo 6` line and uncomment the `DAILY` line right below it
(you can also just change the time in that line), then re-run the .bat.

## Customizing the style
Inside `wallpaper_rotator.py`, the `QUERIES` list controls what kind of
photos get pulled:
```python
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
```
Add, remove, or edit these terms any time to steer the vibe — e.g. add
`"Paris street at night"`, `"Tokyo neon city"`, or `"vintage saxophone jazz"`
for a narrower look. Mix in more of one theme (cities vs. jazz) by just
repeating similar terms — more entries for a theme means it gets picked
more often.

## Managing the scheduled task
- Open Task Scheduler (`Win + R` → `taskschd.msc`) → find **WallpaperRotator**
  under the Task Scheduler Library to pause, edit timing, or delete it.
- To remove it entirely: `schtasks /delete /tn "WallpaperRotator" /f`

## Notes
- Unsplash's free tier allows 50 requests/hour, which is far more than
  you'll need for this (max 4 requests/day even on the 6-hour schedule).
- The script avoids repeating recent photos by remembering the last 40
  photo IDs in `history.json`.
- Everything runs locally — no data leaves your machine except the
  request to Unsplash for a photo.
