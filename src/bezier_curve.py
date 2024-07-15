import io

from svgpathtools import svg2paths


def get_points_from_bezier_curve(curve, origin):
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


def get_points_from_svg_divs(svg_divs):
    points = []
    origin = 0
    path_divs = svg_divs
    for index, path_div in enumerate(path_divs):
        paths, attributes = svg2paths(io.StringIO(str(path_div)))
        # process one path div
        for path in paths:
            for bezierCurve in path:
                points.extend(get_points_from_bezier_curve(bezierCurve, origin))
        # update origin by the last point of the current path
        origin = points[-1][0]

    return points