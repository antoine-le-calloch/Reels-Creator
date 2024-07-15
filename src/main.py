from bs4 import BeautifulSoup
import os

from bezier_curve import get_points_from_svg_divs
from youtube import get_youtube_clip
from graph import draw_graph

if __name__ == '__main__':
    youtube_clip = get_youtube_clip('x7bDk4Jvh6s')
    if youtube_clip is None:
        print("Error: unable to retrieve the video clip.")
        exit(1)

    html_object = BeautifulSoup(youtube_clip, 'html.parser')
    heat_map = html_object.find(class_='ytp-chrome-bottom')
    if heat_map is None:
        print("Error: heat map not found for this video.")
        exit(1)

    path_divs = heat_map.find_all('path')
    points = get_points_from_svg_divs(path_divs)
    draw_graph(points)
