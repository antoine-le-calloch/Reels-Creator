import matplotlib.pyplot as plt


def draw_graph(points):
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    # Tracer le graphique
    plt.figure(figsize=(40, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='b')
    plt.title('Graph of the bezier curve')
    plt.grid(True)
    plt.show()
