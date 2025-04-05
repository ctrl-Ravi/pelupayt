# 🎥 Playlist Length Analyzer :💓

Analyze YouTube playlists and videos with ease! Get detailed information about video durations and playlist lengths.

## 🌟 Features

- 📋 Analyze multiple playlists and individual videos
- ⏱️ Calculate total duration of playlists
- 🚀 Estimate playback times at different speeds (1.25x, 1.50x, 1.75x, 2.00x)
- 🔢 Support for custom playback speeds
- 📅 View average video length in playlists
- 🔍 Analyze specific video ranges within playlists
- 📈 Asynchronous requests and caching layer to speed up processing

## 🚧 Future additions (if I ever get around to it)
- [ ] Add more analytics related to the videos (like average views, likes, etc.)

## 🚀 Getting Started

1. Clone the repository:
   ```
   git clone 
   cd 
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your YouTube API key:
   - Create a `.env` file in the project root
   - Add your API key(s):
     ```
     APIS=YOUR_API_KEY
     ```

4. Run the application:
   ```
   fastapi dev .\app.py

   or
   uvicorn app:fapp --reload

   ```

5. Open your browser and navigate to `http://localhost:8000`

## 📝 Usage

1. Enter YouTube playlist or video URLs in the input box
2. (Optional) Specify a range of videos to analyze within playlists
3. (Optional) Enter a custom playback speed
4. Click "Analyze" to get detailed information about the playlists and videos

## 👏 Technologies Used

- [Python](https://www.python.org/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [Halfmoon](https://www.gethalfmoon.com/)

Made with ❤️ by [Sharat Sachin](https://github.com/sharatsachin)