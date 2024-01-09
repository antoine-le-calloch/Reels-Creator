# youtube.py
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# env loading to get the youtube API key
load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")


def get_youtube():
    return build('youtube', 'v3', developerKey=api_key)
