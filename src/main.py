# Main
# from youtube_API.processVideo import get_most_replayed_moment
# from svgpathtools import svg2paths
from svgpathtools import parse_path
from bs4 import BeautifulSoup
svg_data = '<path d="M 0.0,100.0 C 0.0,95.3 -14.3,81.3 0.0,76.7 C 14.3,72.0 28.6,74.0 71.4,76.7 C 114.3,79.3 157.1,87.3 214.3,90.0 C 271.4,92.7 300.0,90.0 357.1,90.0 C 414.3,90.0 442.9,91.7 500.0,90.0 C 557.1,88.3 585.7,85.2 642.9,81.6 C 700.0,77.9 728.6,71.7 785.7,71.9 C 842.9,72.1 885.7,80.5 928.6,82.6 C 971.4,84.8 985.7,79.2 1000.0,82.6 C 1014.3,86.1 1000.0,96.5 1000.0,100.0" fill="white"/>'

if __name__ == '__main__':
    # get_most_replayed_moment("Squeezie")
    # with open('one_graph_part.txt', 'r') as f:
    #     contenu = f.read()

    objet_html = BeautifulSoup(svg_data, 'html.parser')
    valeurs_d = [balise['d'] for balise in objet_html]
    print(valeurs_d[0])
    pathObject = parse_path(valeurs_d[0])
    print(pathObject)
    # abs_norms = [abs(complex(point.real, point.imag)) for point in points]
    # print(abs_norms)