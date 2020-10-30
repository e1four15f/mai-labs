from dataclasses import dataclass
from typing import List

import numpy as np

EPSILON = 1e-3


@dataclass
class Point:
    x: float
    y: float

    def __add__(self, other: 'Point') -> 'Point':
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(x=self.x - other.x, y=self.y - other.y)

    def __truediv__(self, num: float) -> 'Point':
        return Point(x=self.x / num, y=self.y / num)

    def __str__(self) -> str:
        return f'({self.x:.2f}, {self.y:.2f})'

    def distance_to(self, other: 'Point' = None) -> float:
        if not other:
            other = Point(0, 0)
        point = self - other
        return np.linalg.norm([point.x, point.y])

    def find_farthest_from(self, points: List['Point']) -> 'Point':
        return max(points, key=self.distance_to)


@dataclass
class Circle:
    center: Point
    radius: float

    def __str__(self) -> str:
        return f'Circle(center={self.center}, radius={self.radius:.2f})'

    @classmethod
    def from_two_points(cls, point_i: Point, point_j: Point) -> 'Circle':
        return cls(
            center=(point_i + point_j) / 2, radius=point_i.distance_to(point_j) / 2
        )

    @classmethod
    def from_three_points(
        cls, point_p: Point, point_q: Point, point_z: Point
    ) -> 'Circle':
        # TODO wtf
        sides = sorted(
            [
                (point_p.distance_to(point_q), point_p, point_q),
                (point_q.distance_to(point_z), point_q, point_z),
                (point_p.distance_to(point_z), point_p, point_z),
            ]
        )
        # TODO what distance
        distance = sides[2][0] ** 2 - (sides[0][0] ** 2 + sides[1][0] ** 2)
        if distance < EPSILON:
            return _circumcircle(point_p, point_q, point_z)
        return cls.from_two_points(sides[2][1], sides[2][2])

    def is_point_inside(self, point: Point) -> bool:
        return self.center.distance_to(point) <= self.radius + EPSILON


def _circumcircle(point_i: Point, point_j: Point, point_k: Point) -> Circle:
    # TODO numpy?
    d = (
        point_i.x * (point_j.y - point_k.y)
        + point_j.x * (point_k.y - point_i.x)
        + point_k.x * (point_i.y - point_j.y)
    ) * 2

    if d == 0:
        # TODO
        raise Exception('TODO')

    x = (
        (point_i.distance_to() ** 2) * (point_j.y - point_k.y)
        + (point_j.distance_to() ** 2) * (point_k.y - point_i.y)
        + (point_k.distance_to() ** 2) * (point_i.y - point_j.y)
    ) / d
    y = (
        (point_i.distance_to() ** 2) * (point_k.x - point_j.x)
        + (point_j.distance_to() ** 2) * (point_i.x - point_k.x)
        + (point_k.distance_to() ** 2) * (point_j.x - point_i.x)
    ) / d

    center = Point(x, y)
    radius = center.distance_to(point_i)

    return Circle(center, radius)
