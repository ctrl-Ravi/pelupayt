# 🎬 YouTube Playlist Duration Calculator

A fast, minimal web app to calculate the total duration of any YouTube playlist — with playback speed breakdowns.

**Live:** [pelupayt.onrender.com](https://pelupayt.onrender.com)

---

## Features

- **Instant Duration** — Paste a playlist URL and get the total watch time
- **Speed Benchmarks** — See durations at 1.25×, 1.5×, 1.75×, 2× speeds
- **Custom Speed** — Enter any playback multiplier
- **Range Selection** — Calculate duration for a specific range of videos
- **Batch Input** — Analyze multiple playlists in one go (up to 5)
- **Single Videos** — Also supports individual video links
- **Chrome Extension** — One-click analysis directly from YouTube
- **Dark Mode** — Full dark/light theme support
- **Copy to Clipboard** — Click any stat to copy it instantly
- **Social Sharing** — Share results on Twitter/WhatsApp
- **Usage Analytics** — Live counter powered by MongoDB

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) (Python) |
| Templates | [Jinja2](https://jinja.palletsprojects.com/) |
| Styling | Vanilla CSS with CSS custom properties |
| API | YouTube Data API v3 |
| Cache | Redis (optional, falls back to in-memory) |
| Database | MongoDB (optional, for usage analytics) |
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
├── Procfile                # Deployment config (Render)
└── .gitignore
```

---

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/ctrl-ravi/pelupayt.git
cd pelupayt
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
APIS=YOUR_YOUTUBE_API_KEY
REDIS_URL=                   # Optional — leave empty for in-memory cache
MONGO_URL=                   # Optional — leave empty to skip analytics
```

> **Getting a YouTube API key:**
> 1. Go to [Google Cloud Console](https://console.cloud.google.com/)
> 2. Create a new project (or select existing)
> 3. Enable **YouTube Data API v3**
> 4. Go to **Credentials** → Create **API Key**
> 5. Copy the key into your `.env` file

### 3. Run Locally

```bash
python app.py
```

Open **http://localhost:10000** in your browser.

Alternatively, use uvicorn directly:

```bash
uvicorn app:fapp --reload --port 10000
```

---

## Architecture

### Request Flow

```
User submits URL
  → FastAPI POST handler (app.py)
    → ItemList parses input (itemlist.py)
      → Identifies playlist IDs & video IDs
      → Fetches playlist metadata (YouTube API)
      → Fetches video details in parallel (asyncio.gather)
    → Results rendered via Jinja2 template
  → Response with analytics cards
```

### Core Components

#### `app.py` — Web Server
- **GET `/`** — Renders landing page with usage counter from MongoDB
- **POST `/`** — Processes form submission, returns analytics results
- **GET `/style.css`** — Serves CSS from templates directory
- **GET `/healthz`** — Health check endpoint for deployment platforms

#### `src/itemlist.py` — Input Orchestrator
- Parses multi-line input into playlist IDs and video IDs
- Supports URL formats: full URLs, shortened URLs, raw IDs
- Deduplicates inputs automatically
- Coordinates async API calls for all items

#### `src/playlist.py` — Playlist Engine
- Fetches all video IDs via paginated `playlistItems` API calls
- Fetches video details in parallel using `asyncio.gather` (50 videos per batch)
- Calculates: total duration, average duration, video counts, speed adjustments
- **Redis caching:** Stores video data for 24 hours to reduce API calls
- **MongoDB tracking:** Increments per-playlist analysis count

#### `src/video.py` — Video Model
- Parses video metadata from YouTube API response
- Stores: title, channel, duration, views, likes, comments
- Handles unavailable videos (zero duration = excluded)
- Serializes to/from dict for Redis caching

#### `src/utils.py` — Utilities
- `call_youtube_api()` — Async HTTP client with automatic key rotation on 403 errors
- `parse()` — Converts `timedelta` to compact format (`12h 30m 54s`)
- `find_time_slice()` — Determines API key rotation based on time of day

### Frontend Architecture

#### Template (`home.html`)
The Jinja2 template intelligently parses the backend's flat string output into structured visual zones:

| Zone | Content | CSS Class |
|------|---------|-----------|
| Header | Title + YouTube icon + ID/Creator meta tags | `.result-header` |
| Notices | Warnings (e.g., "limited to 500") | `.result-notice` |
| Stat Grid | Video count, average length, total duration | `.stat-grid` |
| Speed Chips | Playback speeds in a compact grid | `.speed-grid` |
| Share | Twitter, WhatsApp, copy link buttons | `.share-section` |

#### Landing Page Sections
Shown only when no results are displayed:

| Section | Description |
|---------|-------------|
| Hero | Title + usage counter badge |
| Form | URL input + advanced options (range, speed, API key) |
| Overview | Tool description |
| Extension | Chrome extension promo card |
| Features | 6-item capability grid |
| Showcase | 3 curated popular playlists |
| Comparison | Feature comparison table |
| How-to | 4-step usage guide |
| FAQ | 5-item accordion |

---

## API Key Rotation

The app supports multiple YouTube API keys for automatic quota management:

```env
APIS=key1;key2;key3
```

**How it works:**
1. First key is used for all requests
2. If a key returns `403 Quota Exceeded`, the app automatically tries the next key
3. If all keys are exhausted, an error message is shown to the user
4. Users can also provide their own API key via the "Passkey" field

---

## Caching Strategy

### Redis (Production)
- Video data is cached per playlist ID for **24 hours**
- Key format: `playlist:{playlist_id}`
- Significantly reduces YouTube API quota usage for popular playlists

### In-Memory (Development)
- Falls back to a simple dict-based cache when `REDIS_URL` is not set
- Same TTL behavior, but resets on server restart

---

## Deployment

### Render (Recommended)

1. Push to GitHub
2. Connect repo to [Render](https://render.com)
3. Set environment variables (`APIS`, `REDIS_URL`, `MONGO_URL`)
4. Deploy — the `Procfile` handles the rest:

```
web: uvicorn app:fapp --host 0.0.0.0 --port $PORT
```

### Docker (Alternative)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 10000
CMD ["uvicorn", "app:fapp", "--host", "0.0.0.0", "--port", "10000"]
```

---

## Chrome Extension

The Chrome extension adds a one-click "Calculate Duration" button on YouTube playlist pages. It redirects to the web app with the playlist URL pre-filled.

**How it integrates:**
1. Extension navigates to `https://playlistduration.pelupa.in/?search_string=<playlist_url>`
2. The `home.html` script detects the `search_string` query parameter
3. Form auto-submits, showing a loading spinner
4. Results display automatically with smooth scroll

> **Installation guide:** [How to install the extension](https://pelupa.in/how-to-download-and-use-the-playlist-duration-analyzer-chrome-extension/)

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is open source. See the repository for license details.

## Author

Built by [Ravi Prakash](https://pelupa.in) — [@ctrl-ravi](https://github.com/ctrl-ravi)
