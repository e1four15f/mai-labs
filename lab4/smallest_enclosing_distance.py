from typing import List

from lab4.circle import Circle, Point


def _ritter_initial_ball(points: List[Point]) -> Circle:
    point_1 = points[0]
    point_2 = point_1.find_farthest_from(points)
    point_3 = point_2.find_farthest_from(points)

    diameter = point_2.distance_to(point_3)
    center = (point_2 + point_3) / 2

    return Circle(center=center, radius=diameter / 2)


def find_smallest_circle(points: List[Point]) -> Circle:
    bounding_circle = _ritter_initial_ball(points)

    for point in points:
        distance = point.distance_to(bounding_circle.center)
        alpha = 1
        while distance > bounding_circle.radius:
            bounding_circle.radius += distance / alpha
            bounding_circle.center += point / alpha
            alpha *= 2

    return bounding_circle
