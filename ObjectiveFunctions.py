import numpy as np


def f(x):
    # simple function
    return 2 * x[0] ** 2 - 8 * x[0] + 1


def f_rosenbrock(x):
    a = 0
    b = 1
    return (a - x[0]) ** 2 + b * (x[1] - x[0] ** 2) ** 2


def f_rastrigin(x):
    value = (
        (x[0] ** 2 - 10 * np.cos(2 * np.pi * x[0]))
        + (x[1] ** 2 - 10 * np.cos(2 * np.pi * x[1]))
        + 20
    )
    return value
