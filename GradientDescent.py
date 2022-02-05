import random

import numpy as np

from PSO import f_rosenbrock


def rosenbroch_gradient(x):
    a = 0
    b = 1
    dx1 = -2 * (a - x[0]) + b * -4 * x[0] * (x[1] - (x[0] ** 2))
    dx2 = 2 * b * (x[1] - (x[0] ** 2))
    return [dx1, dx2]


def gradient_descent_op(iterations, alpha=0.5):
    position = [random.uniform(-1, 1), random.uniform(-1, 1)]
    MAX_GRADIENT = 5000

    for i in range(iterations):
        gradient = rosenbroch_gradient(position)
        if abs(gradient[0]) > MAX_GRADIENT:
            gradient[0] = -MAX_GRADIENT
        if abs(gradient[1]) > MAX_GRADIENT:
            gradient[1] = MAX_GRADIENT

        position[0] = position[0] - alpha * gradient[0]
        position[1] = position[1] - alpha * gradient[1]

    print('gradient descent')
    print(position, f_rosenbrock(position))


gradient_descent_op(100)
