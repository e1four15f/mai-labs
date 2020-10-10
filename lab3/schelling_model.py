from typing import List, Optional

import numpy as np
from lab3.utils import rolling_window2d


class SchellingModel:
    def __init__(
        self,
        board_size: int,
        race_probabilities: Optional[List[float]] = None,
        same_color_threshold: int = 2,
    ):
        race_probabilities = race_probabilities or [0.45, 0.45]
        assert (
            sum(race_probabilities) <= 1
        ), f'Sum of race probabilities can\'t be greater than 1, got {sum(race_probabilities)}'
        self._same_color_threshold = same_color_threshold
        self.board = self._create_board(board_size, race_probabilities)

    @staticmethod
    def _create_board(board_size: int, race_probabilities: List[float]) -> np.ndarray:
        race_probabilities.insert(0, 1 - sum(race_probabilities))  # type: ignore
        number_of_races = len(race_probabilities)
        return np.random.choice(
            range(number_of_races), size=(board_size, board_size), p=race_probabilities
        )

    def _is_cell_unhappy(self, cell_neighbours: np.ndarray) -> bool:
        cell_color = cell_neighbours[4]
        if cell_color == 0:
            return False
        same_color_cells = (cell_neighbours == cell_color).sum()
        return same_color_cells < self._same_color_threshold + 1

    def step(self):
        padded_board = np.pad(
            self.board, [(1, 1), (1, 1)], mode='constant', constant_values=0
        )
        cells = rolling_window2d(array=padded_board, kernel_size=(3, 3))
        cells = cells.reshape(*cells.shape[:2], -1)

        unhappy_cells = np.argwhere(
            np.apply_along_axis(self._is_cell_unhappy, axis=-1, arr=cells)
        )
        empty_cells = np.argwhere(self.board == 0)

        for unhappy_cell in unhappy_cells:
            if len(empty_cells) == 0:
                print('No empty cells')
                break
            random_index = np.random.choice(len(empty_cells))
            empty_cell = empty_cells[random_index]
            empty_cells = np.delete(empty_cells, random_index, axis=0)

            self.board[tuple(empty_cell)], self.board[tuple(unhappy_cell)] = (
                self.board[tuple(unhappy_cell)],
                self.board[tuple(empty_cell)],
            )
