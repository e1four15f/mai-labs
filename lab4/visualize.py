from typing import List

from lab4.circle import Circle, Point
from matplotlib import pyplot as plt


def draw_circle_points(circle: Circle, points: List[Point]):
    _, axis = plt.subplots()
    axis.set_xlim(
        left=circle.center.x - 2 * circle.radius,
        right=circle.center.x + 2 * circle.radius,
    )
    axis.set_ylim(
        bottom=circle.center.y - 2 * circle.radius,
        top=circle.center.y + 2 * circle.radius,
    )

    for point in points:
        plt.scatter(point.x, point.y, c='deeppink')
    plt.scatter(circle.center.x, circle.center.y, c='blue', marker='x')

    circle_plot = plt.Circle(
        (circle.center.x, circle.center.y), circle.radius, fill=False
    )
    axis.add_artist(circle_plot)

    plt.title(circle)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
