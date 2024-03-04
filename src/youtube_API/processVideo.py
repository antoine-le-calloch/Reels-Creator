# processVideo.py
import json
import requests
import html_to_json
import re
from bs4 import BeautifulSoup
from .youtube import get_youtube

youtube = get_youtube()


def get_most_replayed_moment(query):
    # Request forgery and execution
    response = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=1  # nb results
    ).execute()

    video_id = response['items'][0]['id']['videoId']

    get_most_replayed_infos(video_id)

    # if video_json is not None:
    #     formatted_json = json.dumps(video_json, indent=2)
    #     print(formatted_json)
    # else:
    #     print("Unable to retrieve video information.")


def get_most_replayed_infos(video_id):
    video_url = "https://www.youtube.com/watch?v=" + video_id
    headers = {
        'Accept-Language': 'en-US,en;q=0.5',
    }

    try:
        # HTTP request to get the HTML
        response = requests.get(video_url, headers=headers)
        response.raise_for_status()

        # Convert HTML to an object
        html_object = BeautifulSoup(response.text, 'html.parser')

        # Find 'ytInitialData' in the HTML
        ytInitialData_script = html_object.find('script', string=re.compile('ytInitialData'))
        if ytInitialData_script is None:
            print("Error: most replayed information not found!")
            return

        # Extract is value
        match = re.search(r'ytInitialData\s*=\s*([^;]+);', ytInitialData_script.string)
        if match is None:
            print("Error: ytInitialData format does not match!")
            return
        ytInitialData = json.loads(match.group(1))

        # Extraction of 'replayedInfo' if necessary key are available
        if 'frameworkUpdates' in ytInitialData and 'entityBatchUpdate' in ytInitialData['frameworkUpdates']:
            mutations = ytInitialData['frameworkUpdates']['entityBatchUpdate']['mutations']
            for mutation in mutations:
                if 'payload' in mutation:
                    payload = mutation['payload']
                    break
            else:
                print("Error: payload not found!")
                return

            replayed_info = payload['macroMarkersListEntity']['markersList']
            # # Removing durationMillis and extract startMillis markers
            # for marker in replayed_info['markers']:
            #     del marker['durationMillis']
            #     marker['startMillis'] = int(marker['startMillis'])

            # Extract timed decoration and removing decoration markers
            replayed_info['timedMarkerDecorations'] = replayed_info['markersDecoration'][
                'timedMarkerDecorations']
            for marker_decoration in replayed_info['timedMarkerDecorations']:
                for key in ['label', 'icon', 'decorationTimeMillis']:
                    del marker_decoration[key]

            # Removing not needed key
            for key in ['markerType', 'markersMetadata', 'markersDecoration']:
                del replayed_info[key]

            print(replayed_info)

    except requests.RequestException as e:
        print(f"Une erreur s'est produite lors de la récupération de la page : {e}")
        return None
