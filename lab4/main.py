import argparse
import pathlib
from typing import List

import numpy as np
from lab4.circle import Point
from lab4.smallest_enclosing_distance import find_smallest_circle
from lab4.visualize import draw_circle_points


def _generate_points(
    low: int = -15, high: int = 15, number_of_points: int = 60
) -> List[Point]:
    x_coordinates = np.random.uniform(low, high, size=number_of_points)
    y_coordinates = np.random.uniform(low, high, size=number_of_points)
    return [Point(x, y) for x, y in zip(x_coordinates, y_coordinates)]


def _points_from_file(path: pathlib.Path) -> List[Point]:
    points = []  # noqa
    with path.open() as file:
        lines = file.read().split('\n')
        for line in lines:
            x, y = line.split(sep=',')
            points.append(Point(x=float(x), y=float(y)))
    return points


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Smallest enclosing distance algorithm'
    )
    parser.add_argument(
        '-f',
        '--file',
        type=pathlib.Path,  # noqa
        default=None,
        help='Path to file with points coordinates in comma separated style',
    )
    parser.add_argument(
        '-n',
        '--number_of_points',
        type=int,
        default=60,
        help='Number of generated points',
    )
    args = parser.parse_args()

    if args.file:
        points = _points_from_file(args.file)
    else:
        points = _generate_points(number_of_points=args.number_of_points)

    circle = find_smallest_circle(points)
    draw_circle_points(circle, points)
