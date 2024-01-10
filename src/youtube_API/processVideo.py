# processVideo.py
import json
import requests
import html_to_json
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
        html_string = response.text

        pageInJson = html_to_json.convert(html_string)
        # print((pageInJson['html']).keys())
        for key, value in pageInJson.items():
            print(value)


        # Analyse du contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Recherche de la balise <script> contenant 'ytplayer.config' dans le HTML
        script_tag = soup.find('script', text=lambda text: text and 'ytplayer.config' in text)


        if 0:
            for script_tag in script_tags:
                # Get start and end of the JSON chain
                json_start = script_tag.string.find('{')
                json_end = script_tag.string.rfind('}') + 1

                if json_start != -1 and json_end != -1:
                    # Extraction and conversion to Python object
                    json_content = script_tag.string[json_start:json_end]
                    data = json.loads(json_content)

                    # Extraction of 'replayedInfo' if necessary key are available
                    if 'frameworkUpdates' in data and 'entityBatchUpdate' in data['frameworkUpdates']:
                        replayed_info = data['frameworkUpdates']['entityBatchUpdate']['mutations'][0]['payload']['macroMarkersListEntity'][
                            'markersList']

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

                        return replayed_info

    except requests.RequestException as e:
        print(f"Une erreur s'est produite lors de la récupération de la page : {e}")
        return None
