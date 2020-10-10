from time import sleep

from lab3.schelling_model import SchellingModel
from lab3.utils import TerminalBoardVisualizer


def main():
    model = SchellingModel(
        board_size=50,
        race_probabilities=[0.35, 0.35],
        same_color_threshold=2,
    )
    visualizer = TerminalBoardVisualizer()

    for _ in range(1000):
        model.step()
        visualizer.visualize(model.board)
        sleep(0.1)


if __name__ == '__main__':
    main()
