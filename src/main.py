from svgpathtools import svg2paths
from bs4 import BeautifulSoup
import io
import os

from src.graph.draw_graph import draw_graph


def getPointsFromBezierCurve(curve, origin):
    points = []
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
        points.append([x + origin, y * -1])
    return points


if __name__ == '__main__':
    file_name = '../html_yt_graphique_part.html'

    if not os.path.exists(file_name):
        print("The file does not exist.")
        exit(0)

    with open(file_name, 'r', encoding='utf-8') as file:
        html_content = file.read()
    html_object = BeautifulSoup(html_content, 'html.parser')
    path_divs = html_object.find_all('path')

    points = []
    origin = 0
    for index, path_div in enumerate(path_divs):
        paths, attributes = svg2paths(io.StringIO(str(path_div)))
        # process one path div
        for path in paths:
            for bezierCurve in path:
                points.extend(getPointsFromBezierCurve(bezierCurve, origin))
        # update origin by the last point of the current path
        origin = points[-1][0]

    draw_graph(points)
    print(points)
