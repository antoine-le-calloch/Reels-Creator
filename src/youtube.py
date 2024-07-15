import requests
from bs4 import BeautifulSoup


def get_youtube_clip(video_id):
    video_url = "https://www.youtube.com/watch?v=" + video_id
    headers = {
        'Accept-Language': 'en-US,en;q=0.5',
    }

    try:
        # HTTP request to get the HTML
        response = requests.get(video_url, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(e)
        return None
