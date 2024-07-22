from graph import draw_graph
from youtube import (
    get_most_replayed_infos,
    get_most_replayed_points
)

if __name__ == '__main__':
    most_replayed_infos = get_most_replayed_infos('x7bDk4Jvh6s')
    draw_graph([[info['startMillis'], info['intensityScoreNormalized']] for info in most_replayed_infos['markers']])

    most_replayed_points = get_most_replayed_points('x7bDk4Jvh6s')
    draw_graph(most_replayed_points)
