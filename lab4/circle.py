from dataclasses import dataclass
from typing import List

import numpy as np

EPSILON = 1e-12


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
    def from_two_points(cls, p_i: Point, p_j: Point) -> 'Circle':
        return cls(center=(p_i + p_j) / 2, radius=p_i.distance_to(p_j) / 2)

    @classmethod
    def from_three_points(cls, p_i: Point, p_j: Point, p_k: Point) -> 'Circle':
        sides = sorted(
            [
                (p_i.distance_to(p_j), p_i, p_j),
                (p_j.distance_to(p_k), p_j, p_k),
                (p_i.distance_to(p_k), p_i, p_k),
            ]
        )
        distance = sides[2][0] ** 2 - (sides[0][0] ** 2 + sides[1][0] ** 2)
        if distance < EPSILON:
            return _circumcircle(p_i, p_j, p_k)
        return cls.from_two_points(sides[2][1], sides[2][2])

    def is_point_inside(self, point: Point) -> bool:
        return self.center.distance_to(point) <= self.radius + EPSILON


def _circumcircle(p_i: Point, p_j: Point, p_k: Point) -> Circle:
    A = np.array([[p_k.x - p_i.x, p_k.y - p_i.y], [p_k.x - p_j.x, p_k.y - p_j.y]])

    if np.linalg.det(A) == 0:
        raise Exception('Can\'t create Circle from given points')

    Y = np.array(
        [
            (p_k.x ** 2 + p_k.y ** 2 - p_i.x ** 2 - p_i.y ** 2),
            (p_k.x ** 2 + p_k.y ** 2 - p_j.x ** 2 - p_j.y ** 2),
        ]
    )
    center_x, center_y = 0.5 * np.dot(np.linalg.inv(A), Y)

    radius = np.sqrt((center_x - p_i.x) ** 2 + (center_y - p_i.y) ** 2)
    center = Point(center_x, center_y)

    return Circle(center, radius=radius)
