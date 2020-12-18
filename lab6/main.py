import operator
from dataclasses import dataclass
from node import fit_container
from typing import List

import numpy as np
from more_itertools import powerset


@dataclass
class Box:
    width: int
    height: int
    weight: int

    @property
    def area(self) -> int:
        return self.height * self.width

    @property
    def value(self) -> int:
        return self.area * self.weight

    def to_numpy(self) -> np.ndarray:
        return np.array([[self.weight] * self.width] * self.height)


def solution_score(boxes: List[Box]) -> int:
    score = 0
    for box in boxes:
        score += box.value
    return score


if __name__ == '__main__':
    container = np.zeros(shape=(7, 4), dtype=np.int)
    boxes = [
        Box(3, 2, 1),
        Box(2, 1, 2),
        Box(1, 4, 4),
        Box(2, 1, 5),
        Box(3, 4, 2),
        Box(1, 2, 6),
    ]

    max_container_volume = operator.mul(*container.shape)
    candidates = sorted(
        [
            sub_set
            for sub_set in powerset(boxes)
            if sum([box.area for box in sub_set]) <= max_container_volume
        ],
        key=solution_score,
        reverse=True,
    )

    for solution in candidates:
        fitted_container = fit_container(container, solution)
        if fitted_container is not None:
            print(f'Решение: {solution_score(solution)}')
            print(solution)

            row_maxmin = fitted_container.min(axis=1).max()
            print(f'Максимум среди минимумов по всем строкам: {row_maxmin}')
            print(f'Координаты:\n{np.argwhere(fitted_container == row_maxmin)}')

            col_maxmin = fitted_container.min(axis=0).max()
            print(f'Максимум среди минимумов по всем столбцам: {col_maxmin}')
            print(f'Координаты:\n{np.argwhere(fitted_container == col_maxmin)}')

            break
    else:
        print('Can\'t find any solution')
