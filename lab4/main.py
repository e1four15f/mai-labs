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


if __name__ == '__main__':
    points = _generate_points(number_of_points=5)
    circle = find_smallest_circle(points)
    draw_circle_points(circle, points)
