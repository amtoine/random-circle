#!/usr/bin/env python

from typing import Callable, Tuple

import argparse
from random import random

import numpy as np
import matplotlib.pyplot as plt

Point = Tuple[float, float]
Distribution = Callable[None, Point]


def random_cartesian() -> Point:
    while True:
        x = random() * 2 - 1
        y = random() * 2 - 1
        if x * x + y * y < 1:
            return x, y


def random_polar() -> Point:
    theta = random() * 2 * np.pi
    r = random()
    return r * np.cos(theta), r * np.sin(theta)


DISTRIBUTIONS = {
    "cartesian": random_cartesian,
    "polar": random_polar,
}


def plot_distribution(
    distribution: Distribution,
    *,
    n: int = 3141,
    color: str = "#008888"
) -> None:
    points = np.array([distribution() for _ in range(n)]).transpose()
    plt.scatter(*points, c=color)


def plot_circle(
    *,
    center: Tuple[float, float] = (0.0, 0.0),
    radius: float = 1.0,
    color: str = "#ff0000",
    width: int = 5,
) -> None:
    angles = np.linspace(0, 2 * np.pi, 1000)
    x = np.cos(angles)
    y = np.sin(angles)
    plt.plot(x, y, c=color, linewidth=width)


def main(*, distribution: Distribution, n: int):
    plt.style.use("dark_background")

    plot_distribution(distribution, n=n)
    plot_circle()

    plt.axis([-1.1, 1.1, -1.1, 1.1])
    plt.grid(False)
    plt.gca().set_aspect("equal")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    choices = list(DISTRIBUTIONS.keys())
    default = choices[0]
    parser.add_argument(
        "--distribution",
        "-d",
        choices=choices,
        default=default,
        help=f"the distribution to use (defaults to '{default}').",
    )
    parser.add_argument(
        "--nb-points",
        "-n",
        type=int,
        default=3141,
        help="the number of points to sample and plot (defaults to 3141).",
    )

    args = parser.parse_args()

    main(distribution=DISTRIBUTIONS[args.distribution], n=args.nb_points)
