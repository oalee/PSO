import random

import numpy as np

from InertiaStrategies import RandomInertiaEvolutionaryStrategy


def gradient_descent_op(
    iterations, function, alpha=0.1, initial_random_guess=1
):
    position = [
        random.uniform(-initial_random_guess, initial_random_guess),
        random.uniform(-initial_random_guess, initial_random_guess),
    ]
    MAX_GRADIENT = 1
    positions = [position]

    for i in range(iterations):
        gradient = function.gradient(position)
        if abs(gradient[0]) > MAX_GRADIENT:
            gradient[0] = MAX_GRADIENT * 1 if gradient[0] > 0 else -1
        if abs(gradient[1]) > MAX_GRADIENT:
            gradient[1] = MAX_GRADIENT * 1 if gradient[1] > 0 else -1

        position[0] = position[0] - alpha * gradient[0]
        position[1] = position[1] - alpha * gradient[1]
        positions.append(position.copy())

    # print("gradient descent")
    # print(position, function(position))
    return positions


# gradient_descent_op(1000, gradient_function=gradient_rastgirin)
