from dotenv import load_dotenv

load_dotenv()

import logging
import os
from typing import Annotated, Optional
from urllib.parse import urlencode

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

from src.itemlist import ItemList

YOUTUBE_APIS = os.environ["APIS"].split(";")
MONGO_URL = os.environ.get("MONGO_URL")

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

fapp = FastAPI()

fapp.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# MongoDB for usage stats
if MONGO_URL:
    mongo_db = MongoClient(MONGO_URL)["ytplaylistdb"]
else:
    mongo_db = None


def get_total_analyses():
    """Get total number of playlist analyses from MongoDB."""
    try:
        if mongo_db:
            pipeline = [{"$group": {"_id": None, "total": {"$sum": "$count"}}}]
            result = list(mongo_db["ytplaylistcounts"].aggregate(pipeline))
            return result[0]["total"] if result else 0
    except Exception as e:
        logger.error(f"Error fetching analysis count: {e}")
    return 0


@fapp.get("/", response_class=HTMLResponse)
async def home(request: Request):
    total_analyses = get_total_analyses()
    return templates.TemplateResponse("home.html", {"request": request, "total_analyses": total_analyses})


@fapp.post("/", response_class=HTMLResponse)
async def home(
    request: Request,
    search_string: Annotated[str, Form()],
    range_start: Annotated[Optional[str], Form()],
    range_end: Annotated[Optional[str], Form()],
    custom_speed: Annotated[Optional[str], Form()],
    youtube_api: Annotated[Optional[str], Form()],
):

    range_start = int(range_start) if range_start else 1
    range_end = int(range_end) if range_end else 500
    custom_speed = float(custom_speed) if custom_speed else None

    if range_start > range_end:
        range_start, range_end = range_end, range_start

    try:
        logger.info(f"Input request: {search_string}")
        youtube_api = youtube_api if youtube_api else YOUTUBE_APIS[0]
        items = ItemList(
            search_string, range_start, range_end, custom_speed, youtube_api
        )
        await items.do_async_work()
        output = items.get_output_string()

    except Exception as e:
        output = [[f"Error: {e}"]]
        logger.error(f"{output}")

    return templates.TemplateResponse(
        "home.html", {"request": request, "playlist_detail": output}
    )


@fapp.get("/healthz")
def healthz():
    return "Success"


@fapp.get("/ads.txt", response_class=PlainTextResponse)
def static_from_root_google():
    return "google.com, pub-8874895270666721, DIRECT, f08c47fec0942fa0"


@fapp.get("/style.css", response_class=FileResponse)
def get_style():
    return FileResponse("templates/style.css", media_type="text/css")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:fapp", host="0.0.0.0", port=10000, reload=True, access_log=False)
