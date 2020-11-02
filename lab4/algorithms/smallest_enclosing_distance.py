from typing import List

import numpy as np
from lab4.circle import Circle, Point


def smallest_enclosing_circle(points: List[Point]) -> Circle:
    if not points:
        raise Exception('No points passed to function')
    if len(points) == 1:
        return Circle(center=points[0], radius=0)

    np.random.shuffle(points)
    circle = Circle.from_two_points(points[0], points[1])

    for i in range(2, len(points)):
        if not circle.is_point_inside(points[i]):
            circle = _smallest_enclosing_circle_one_boundary_point(
                points[:i], points[i]
            )
    return circle


def _smallest_enclosing_circle_one_boundary_point(
    points: List[Point], p_i: Point
) -> Circle:
    np.random.shuffle(points)
    circle = Circle.from_two_points(points[0], p_i)

    for i in range(1, len(points)):
        if not circle.is_point_inside(points[i]):
            circle = _smallest_enclosing_circle_two_boundary_points(
                points[:i], p_i, points[i]
            )
    return circle


def _smallest_enclosing_circle_two_boundary_points(
    points: List[Point], p_i: Point, p_j: Point
) -> Circle:
    circle = Circle.from_two_points(p_i, p_j)

    for point in points:
        if not circle.is_point_inside(point):
            circle = Circle.from_three_points(p_i, p_j, point)
    return circle
