from typing import List

from lab4.circle import Circle, Point


def _ritter_initial_ball(points: List[Point]) -> Circle:
    main_point = points[0]
    first_farthest_point = main_point.find_farthest_from(points)
    second_farthest_point = first_farthest_point.find_farthest_from(points)
    return Circle.from_two_points(first_farthest_point, second_farthest_point)


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
