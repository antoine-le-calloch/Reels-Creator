# processVideo.py
import json
import requests
import re
from bs4 import BeautifulSoup
from bezier_curve import get_points_from_svg_divs


def get_youtube_page_content(video_id):
    video_url = "https://www.youtube.com/watch?v=" + video_id
    headers = {
        'Accept-Language': 'en-US,en;q=0.5',
    }
    response = requests.get(video_url, headers=headers)
    response.raise_for_status()
    if response.text is None:
        print("Error: unable to retrieve the video clip.")
        exit(1)

    return response.text


def get_most_replayed_points(video_id):
    page_content = get_youtube_page_content(video_id)
    html_object = BeautifulSoup(page_content, 'html.parser')

    heat_map = html_object.find(class_='ytp-chrome-bottom')
    if heat_map is None:
        print("Error: heat map not found for this video.")
        exit(1)

    path_divs = heat_map.find_all('path')
    return get_points_from_svg_divs(path_divs)


def get_most_replayed_infos(video_id):
    page_content = get_youtube_page_content(video_id)
    html_object = BeautifulSoup(page_content, 'html.parser')

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

        return replayed_info
