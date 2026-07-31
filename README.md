# Wallpaper Rotator — Car Aesthetic Edition

Automatically refreshes your Windows desktop background with a new
car-aesthetic photo (sports cars, supercars, automotive art), on whatever
schedule you want (default: every 6 hours).

## What's in this folder
- `wallpaper_rotator.py` — fetches a photo from Wallhaven and sets it as your wallpaper
- `setup_task.bat` — registers the Windows scheduled task so it runs automatically
- `.env` — holds your optional Wallhaven API key (not committed to Git)
- `.gitignore` — keeps `.env` and other local files out of your repo
- `README.md` — this file

## Setup (5 minutes)

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
Create a file named `.env` in this folder (leave it blank if you skipped step 3):

This file is already excluded from Git via `.gitignore`, so it stays local
to your machine.

### 5. Test it once manually
Double-click `wallpaper_rotator.py`, or run from Command Prompt:

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
    "porsche",
    "sports car",
    "supercar",
    "car blueprint art",
    "jdm car",
    "automotive poster art",
    "car aesthetic wallpaper",
]
```
Add, remove, or edit these terms any time to steer the vibe — e.g. add
`"ferrari"`, `"lamborghini aesthetic"`, or `"car wallpaper 4k"` for a
narrower look. Mix in more of one theme by just repeating similar terms —
more entries for a theme means it gets picked more often.

## Managing the scheduled task
- Open Task Scheduler (`Win + R` → `taskschd.msc`) → find **WallpaperRotator**
  under the Task Scheduler Library to pause, edit timing, or delete it.
- To remove it entirely: `schtasks /delete /tn "WallpaperRotator" /f`

## Pushing to GitHub
The `.env` file (and anything else listed in `.gitignore`) will **not** be
committed, so it's safe to push this whole folder. Anyone who clones the
repo just needs to create their own `.env` file to run it (or leave it
blank, since a Wallhaven key is optional).

## Notes
- Wallhaven works without an API key; with one, rate limits are higher.
- The script avoids repeating recent photos by remembering the last 40
  wallpaper IDs in `history.json`.
- Everything runs locally — no data leaves your machine except the
  request to Wallhaven for a photo.