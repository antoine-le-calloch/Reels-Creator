# processVideo.py
import json
from .youtube import get_youtube
from googleapiclient.errors import HttpError

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

    get_video_json(video_id)

    # if video_json is not None:
    #     formatted_json = json.dumps(video_json, indent=2)
    #     print(formatted_json)
    # else:
    #     print("Unable to retrieve video information.")


def get_video_json(video_id):
    video_url = "https://www.youtube.com/watch?v=" + video_id
    headers = {
        'Accept-Language': 'en-US,en;q=0.5',  # Replace with the desired language code
    }

    print(video_url)

    # try:
    #     response = requests.get(video_url, headers=headers)
    #     response.raise_for_status()
    #
    #     soup = BeautifulSoup(response.content, 'html.parser')
    #
    #     # Trouvez la balise script qui contient les données JSON
    #     script_tag = soup.find('script', {'name': 'ytplayer.config'})
    #
    #     # Extraire et analyser les données JSON
    #     if script_tag:
    #         json_data = script_tag.string
    #         json_start = json_data.find('{')
    #         json_end = json_data.rfind('}') + 1
    #         json_content = json_data[json_start:json_end]
    #
    #         return json_content
    #     else:
    #         print("La balise script n'a pas été trouvée.")
    #
    # except requests.RequestException as e:
    #     print(f"Une erreur s'est produite lors de la récupération de la page : {e}")
    #
    # return None
