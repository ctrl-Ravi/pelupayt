import datetime
import json
import os
from urllib.parse import urlencode

import aiohttp


# find out which time slice an time lies in, to decide which API key to use
def find_time_slice():
    time_slice = datetime.datetime.now().time().hour // 4
    return time_slice

# def find_time_slice():
#     apis_count = len(os.environ["APIS"].split(";"))
#     time_slice = datetime.datetime.now().time().hour // 4
#     return time_slice % apis_count  # safe mod



async def call_youtube_api(url_type, api, **kwargs):

    base_url = f"https://www.googleapis.com/youtube/v3/{url_type}"
    url_params = {
        "playlists": {
            "part": "snippet",
            "fields": "items/snippet/title,items/snippet/channelTitle",
            "id": ",".join(kwargs.get("playlist_ids", [])),
        },
        "playlistItems": {
            "part": "contentDetails",
            "maxResults": "50",
            "fields": "items/contentDetails/videoId,nextPageToken",
            "playlistId": kwargs.get("playlistId"),
            "pageToken": kwargs.get("pageToken", ""),  # Optional Page Token
        },
        "videos": {
            "part": "contentDetails,statistics,snippet",
            "id": ",".join(kwargs.get("video_ids", [])),  # List of video IDs
            "fields": "items/contentDetails/duration,items/statistics/likeCount,"
            "items/statistics/viewCount,items/statistics/commentCount,"
            "items/snippet/title,items/snippet/channelTitle,items/snippet/publishedAt",
        },
    }

    params = url_params.get(url_type, {})
    if not params:
        raise ValueError(f"Invalid URL type: {url_type}")

    apis_to_try = [api]
    # If the user didn't explicitly override it, load the rotating env keys
    if api in os.environ.get("APIS", "").split(";"):
        apis_to_try = os.environ.get("APIS", "").split(";")

    async with aiohttp.ClientSession() as session:
        for current_api in apis_to_try:
            params["key"] = current_api
            url = f"{base_url}?{urlencode(params, safe=',')}"
            
            async with session.get(url) as response:
                response_json = json.loads(await response.text())
                
                # Check for YouTube API errors (specifically Quota Exceeded 403)
                if "error" in response_json and response_json["error"].get("code") == 403:
                    logging.warning(f"YouTube DB API Quota Exceeded using key starting with {current_api[:10]}. Rotating...")
                    continue # Try the next API key in the list
                
                return response_json
        
        # If the loop exhausts and returns nothing, it means all keys failed
        raise Exception("All YouTube API keys have exhausted their quota. Please try again later or provide a custom key.")


def parse(a):
    ts, td = a.seconds, a.days
    th, tr = divmod(ts, 3600)
    tm, ts = divmod(tr, 60)
    parts = []
    if td:
        parts.append(f"{td}d")
    if th:
        parts.append(f"{th}h")
    if tm:
        parts.append(f"{tm}m")
    if ts:
        parts.append(f"{ts}s")
    return " ".join(parts) if parts else "0s"
