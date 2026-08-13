"""
Wallpaper Gallery — local web app to browse history and save favorites.
Run this, then open http://localhost:5000 in a browser (or your phone,
if on the same WiFi network — see note at the bottom).
"""

from pathlib import Path
from flask import Flask, render_template_string, send_from_directory, redirect, url_for
import shutil

app = Flask(__name__)

WALLPAPER_DIR = Path.home() / "Pictures" / "AutoWallpapers"
FAVORITES_DIR = WALLPAPER_DIR / "favorites"
FAVORITES_DIR.mkdir(parents=True, exist_ok=True)

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Wallpaper Gallery</title>
    <style>
        body { background: #111; color: #eee; font-family: sans-serif; margin: 0; padding: 20px; }
        h1 { font-weight: 300; }
        h2 { font-weight: 300; color: #999; margin-top: 40px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
        .card { background: #1c1c1c; border-radius: 10px; overflow: hidden; }
        .card img { width: 100%; height: 260px; object-fit: cover; display: block; }
        .card-footer { padding: 10px; display: flex; justify-content: space-between; align-items: center; }
        .filename { font-size: 12px; color: #888; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 130px; }
        form { margin: 0; }
        button { background: #e63946; border: none; color: white; padding: 6px 10px; border-radius: 6px; cursor: pointer; font-size: 13px; }
        button:hover { background: #ff4d5e; }
        .fav-badge { color: #ffb703; font-size: 13px; }
        .empty { color: #666; padding: 40px 0; }
    </style>
</head>
<body>
    <h1>🚗 Wallpaper Gallery</h1>

    <h2>⭐ Favorites</h2>
    {% if favorites %}
    <div class="grid">
        {% for f in favorites %}
        <div class="card">
            <img src="/image/favorites/{{ f }}">
            <div class="card-footer">
                <span class="filename">{{ f }}</span>
                <span class="fav-badge">Saved</span>
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p class="empty">No favorites saved yet — click "Save" on any wallpaper below.</p>
    {% endif %}

    <h2>🕓 Recent History</h2>
    <div class="grid">
        {% for f in recent %}
        <div class="card">
            <img src="/image/main/{{ f }}">
            <div class="card-footer">
                <span class="filename">{{ f }}</span>
                <form method="POST" action="/favorite/{{ f }}">
                    <button type="submit">❤️ Save</button>
                </form>
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""


@app.route("/")
def gallery():
    recent = sorted(
        [f.name for f in WALLPAPER_DIR.glob("wallpaper_*.*")],
        reverse=True
    )
    favorites = sorted(
        [f.name for f in FAVORITES_DIR.glob("*.*")],
        reverse=True
    )
    return render_template_string(PAGE_TEMPLATE, recent=recent, favorites=favorites)


@app.route("/image/main/<filename>")
def serve_main_image(filename):
    return send_from_directory(WALLPAPER_DIR, filename)


@app.route("/image/favorites/<filename>")
def serve_favorite_image(filename):
    return send_from_directory(FAVORITES_DIR, filename)


@app.route("/favorite/<filename>", methods=["POST"])
def save_favorite(filename):
    src = WALLPAPER_DIR / filename
    dst = FAVORITES_DIR / filename
    if src.exists():
        shutil.copy(src, dst)
    return redirect(url_for("gallery"))


if __name__ == "__main__":
    print("Gallery running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
    
