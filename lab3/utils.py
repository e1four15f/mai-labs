import os
from typing import Tuple

import numpy as np


def rolling_window2d(
    array: np.ndarray, kernel_size: Tuple[int, int] = (3, 3)
) -> np.ndarray:
    view_shape = tuple(np.subtract(array.shape, kernel_size) + 1) + kernel_size
    strides = array.strides + array.strides
    return np.lib.stride_tricks.as_strided(array, view_shape, strides)


class TerminalBoardVisualizer:
    _COLORS = ['\033[0m'] + [f'\033[1;3{i}m' for i in range(1, 8)]
    _CELL_SYMBOL = '[]'

    def visualize(self, board: np.ndarray):
        os.system('clear')
        colored_board = np.vectorize(
            lambda x: f'{self._COLORS[x]}{self._CELL_SYMBOL}{self._COLORS[0]}'
            if x != 0
            else '  '
        )(board)
        string = '\n'.join(
            [''.join([str(cell) for cell in row]) for row in colored_board]
        )
        print(string)
