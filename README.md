# 🎬 YouTube Playlist Duration Calculator

A fast, minimal web app to calculate the total duration of any YouTube playlist — with playback speed breakdowns.

**Live:** [playlistaws.pelupa.in](https://playlistaws.pelupa.in)

---

## Features

- **Instant Duration** — Paste a playlist URL and get the total watch time
- **Speed Benchmarks** — See durations at 1.25×, 1.5×, 1.75×, 2× speeds
- **Custom Speed** — Enter any playback multiplier
- **Range Selection** — Calculate duration for a specific range of videos
- **Batch Input** — Analyze multiple playlists in one go
- **Single Videos** — Also supports individual video links
- **Chrome Extension** — One-click analysis directly from YouTube
- **Dark Mode** — Full dark/light theme support

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) (Python) |
| Templates | [Jinja2](https://jinja.palletsprojects.com/) |
| Styling | Vanilla CSS with CSS variables |
| API | YouTube Data API v3 |
| Cache | Redis (optional, falls back to in-memory) |
| Database | MongoDB (optional, for analytics) |
| Hosting | Render / any platform with `Procfile` support |

## Project Structure

```
pelupayt/
├── app.py                  # FastAPI application & routes
├── src/
│   ├── itemlist.py         # Input parsing & orchestration
│   ├── playlist.py         # Playlist data fetching & caching
│   ├── video.py            # Video data model
│   └── utils.py            # YouTube API calls & duration formatting
├── templates/
│   ├── home.html           # Main page template (Jinja2)
│   └── style.css           # All CSS styles
├── static/
│   ├── logo.png            # Site logo
│   ├── favicon.png         # Favicon
│   └── form_validation.js  # Client-side form validation
├── .env                    # Environment variables (not in git)
├── requirements.txt        # Python dependencies
├── Procfile                # Deployment config
└── .gitignore
```

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/ctrl-ravi/pelupayt.git
cd pelupayt
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

### 2. Configure

Create a `.env` file:

```env
APIS=YOUR_YOUTUBE_API_KEY
REDIS_URL=                   # Optional — leave empty for in-memory cache
MONGO_URL=                   # Optional — leave empty to skip analytics
```

> Get a YouTube Data API v3 key from [Google Cloud Console](https://console.cloud.google.com/apis/credentials). Multiple keys can be separated with `;` for automatic rotation.

### 3. Run

```bash
python app.py
```

Open **http://localhost:10000** in your browser.

## API Key Rotation

The app supports multiple YouTube API keys for quota management. Add multiple keys in `.env` separated by semicolons:

```env
APIS=key1;key2;key3
```

If one key hits its quota, the app automatically rotates to the next.

## Deployment

The included `Procfile` is configured for platforms like Render:

```
web: uvicorn app:fapp --host 0.0.0.0 --port $PORT
```

## Author

Built by [Ravi Prakash](https://pelupa.in)
