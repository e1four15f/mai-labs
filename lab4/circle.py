from dataclasses import dataclass
from typing import List

import numpy as np


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

    def to_numpy(self) -> np.ndarray:
        return np.array([self.x, self.y])

    def distance_to(self, other: 'Point') -> float:
        return np.linalg.norm((self - other).to_numpy())

    def find_farthest_from(self, points: List['Point']) -> 'Point':
        return max(points, key=self.distance_to)


@dataclass
class Circle:
    center: Point
    radius: float

    def __str__(self) -> str:
        return f'Circle(center={self.center}, radius={self.radius:.2f})'
