from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np


def matrix2str(container: np.ndarray) -> str:
    _COLORS = ['\033[0m'] + [f'\033[1;3{i}m' for i in range(1, 8)]
    _CELL_SYMBOL = '██'

    colored_board = np.vectorize(
        lambda x: f'{_COLORS[x]}{_CELL_SYMBOL}{_COLORS[0]}' if x != 0 else '░░'
    )(container).T
    string = '\n'.join([''.join([str(cell) for cell in row]) for row in colored_board])
    return string


class Node:
    def __init__(
        self, container: np.ndarray, childs: Optional[Tuple['Node', 'Node']] = None
    ):
        self.container = container
        self.childs = childs

    def __str__(self) -> str:
        return matrix2str(self.container)

    def insert(self, box: np.ndarray) -> Optional['Node']:
        if self.childs:
            new_node = self.childs[0].insert(box)
            if new_node:
                return new_node
            return self.childs[1].insert(box)

        if self.container.sum() != 0:
            return None

        c_w, c_h = self.container.shape
        b_w, b_h = box.shape
        if c_h < b_h or c_w < b_w:
            return None

        if c_h == b_h and c_w == b_w:
            return self

        if c_w - b_w < c_h - b_h:
            left_child = Node(self.container[b_w:, :b_h])
            right_child = Node(self.container[:, b_h:])
        else:
            left_child = Node(self.container[:b_w, b_h:])
            right_child = Node(self.container[b_w:])
        self.childs = (left_child, right_child)

        return self


def fit_container(
    container: np.ndarray, boxes: List[np.ndarray]
) -> Optional[np.ndarray]:
    root = Node(container.copy())
    log = 'Container\n'
    log += f'{matrix2str(root.container)}\n\n'

    for i, box in enumerate(boxes):
        log += f'Step {i}\n'

        unfolded_box = box.to_numpy()
        result = root.insert(unfolded_box)
        if result is None:
            return None
        result.container[: box.height, : box.width] = unfolded_box
        log += f'{matrix2str(root.container)}\n\n'

    print(log)
    return root.container

