#!/usr/bin/env python

from typing import Callable, Tuple

import argparse
from random import random
from tqdm import trange

import numpy as np
import matplotlib.pyplot as plt

Point = Tuple[float, float]
Distribution = Callable[None, Point]


def random_cartesian() -> Point:
    """See https://youtu.be/4y_nmpv-9lI?t=142"""
    while True:
        x = random() * 2 - 1
        y = random() * 2 - 1
        if x * x + y * y < 1:
            return x, y


def random_polar() -> Point:
    """See https://youtu.be/4y_nmpv-9lI?t=258"""
    theta = random() * 2 * np.pi
    r = random()
    return r * np.cos(theta), r * np.sin(theta)


def random_polar_sqrt() -> Point:
    """See https://youtu.be/4y_nmpv-9lI?t=602"""
    theta = random() * 2 * np.pi
    r = np.sqrt(random())
    return r * np.cos(theta), r * np.sin(theta)


def random_polar_triangle() -> Point:
    """See https://youtu.be/4y_nmpv-9lI?t=728"""
    theta = random() * 2 * np.pi
    r = random() + random()  # sum the coordinates in the triangle
    if r >= 1:  # reflect the half triangle
        r = 2 - r
    return r * np.cos(theta), r * np.sin(theta)


def random_polar_max() -> Point:
    """See https://youtu.be/4y_nmpv-9lI?t=996"""
    theta = random() * 2 * np.pi
    r = random()
    r2 = random()
    if r2 >= r:
        r = r2
    return r * np.cos(theta), r * np.sin(theta)


DISTRIBUTIONS = {
    "cartesian": random_cartesian,
    "polar": random_polar,
    "inverse": random_polar_sqrt,
    "triangle": random_polar_triangle,
    "max": random_polar_max,
}


def plot_distribution(
    distribution: Distribution,
    *,
    n: int = 3141,
    color: str = "#008888"
) -> None:
    points = np.array(
        [distribution() for _ in trange(n, desc="Sampling points")]
    ).transpose()
    plt.scatter(*points, c=color, s=1)


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
