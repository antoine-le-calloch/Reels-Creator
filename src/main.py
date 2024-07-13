# Main
# from youtube_API.processVideo import get_most_replayed_moment
from svgpathtools import svg2paths
from bs4 import BeautifulSoup
import io
import os

svg_data = ('<path d="M 0.0,100.0 C 0.0,95.3 -14.3,81.3 0.0,76.7 C 14.3,72.0 28.6,74.0 71.4,76.7 C 114.3,79.3 157.1,'
            '87.3 214.3,90.0 C 271.4,92.7 300.0,90.0 357.1,90.0 C 414.3,90.0 442.9,91.7 500.0,90.0 C 557.1,'
            '88.3 585.7,85.2 642.9,81.6 C 700.0,77.9 728.6,71.7 785.7,71.9 C 842.9,72.1 885.7,80.5 928.6,'
            '82.6 C 971.4,84.8 985.7,79.2 1000.0,82.6 C 1014.3,86.1 1000.0,96.5 1000.0,100.0" fill="white"/>')
svg_file = io.StringIO(svg_data)


def getPointsFromBezierCurve(points, curve):
    p1 = curve.start
    p2 = curve.control1
    p3 = curve.control2
    p4 = curve.end
    for i in range(10):
        t = i / 10.0
        x = ((1 - t) ** 3) * p1.real + 3 * (1 - t) ** 2 * t * p2.real + 3 * (
                    1 - t) * t ** 2 * p3.real + t ** 3 * p4.real
        y = ((1 - t) ** 3) * p1.imag + 3 * (1 - t) ** 2 * t * p2.imag + 3 * (
                    1 - t) * t ** 2 * p3.imag + t ** 3 * p4.imag
        points.append([x, y])


if __name__ == '__main__':
    file_name = 'html_yt_graphique_part.html'
    
    if not os.path.exists(file_name):
        print("The file does not exist.")
        exit(0)
        
    with open(file_name, 'r', encoding='utf-8') as file:
        html_content = file.read()
    html_object = BeautifulSoup(html_content, 'html.parser')

    print(html_object.prettify())
    paths, attributes = svg2paths(svg_file)
    points = []

    for path in paths:
        for bezierCurve in path:
            getPointsFromBezierCurve(points, bezierCurve)
    print(points)

