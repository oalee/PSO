import random

import numpy as np

from InertiaStrategies import RandomInertiaEvolutionaryStrategy
from PSO import f_rosenbrock


def rosenbroch_gradient(x):
    a = 0
    b = 1
    dx1 = -2 * (a - x[0]) + b * -4 * x[0] * (x[1] - (x[0] ** 2))
    dx2 = 2 * b * (x[1] - (x[0] ** 2))
    return [dx1, dx2]


def gradient_descent_op(iterations, alpha=0.1,
                        initial_random_guess=10
                        ):
    position = [random.uniform(-initial_random_guess, initial_random_guess),
                random.uniform(-initial_random_guess, initial_random_guess)]
    MAX_GRADIENT = 100

    for i in range(iterations):
        gradient = rosenbroch_gradient(position)
        if abs(gradient[0]) > MAX_GRADIENT:
            gradient[0] = MAX_GRADIENT * 1 if gradient[0] > 0 else -1
        if abs(gradient[1]) > MAX_GRADIENT:
            gradient[1] = MAX_GRADIENT

        position[0] = position[0] - alpha * gradient[0]
        position[1] = position[1] - alpha * gradient[1]

    print('gradient descent')
    print(position, f_rosenbrock(position))


gradient_descent_op(1000)
