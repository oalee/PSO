import random

import numpy as np

from InertiaStrategies import (
    DynamicAdaptiveStrategy,
    RandomInertiaEvolutionaryStrategy,
)
from GradientDescent import gradient_descent_op
from ObjectiveFunctions import (
    Rosenbrock,
    Rastrigin,
)
from ParticleVectorized import Particle, Globals

import json

epsilon = 0.00000001

def f(x):
    # simple function
    return 2 * x[0] ** 2 - 8 * x[0] + 1


def PSO(
        objective_function,
        n_particles,
        iterations,
        n_param,
        inertia_strategy,
        guess_random_range,
        gradient_coef=0,
        seed=random.randint(0, 1241231),
        use_random_gradients=False
):
    # initialize the particles
    particles = []
    np.random.seed(seed)
    random.seed(seed)

    globals = Globals(n_param, guess_random_range)
    for i in range(n_particles):
        particle = Particle(
            globals, objective_function, guess_random_range, gradient_coef, use_random_gradients
        )
        particles.append(particle)

    positions = []
    global_best_history = []

    convergence_iteration = 1000

    for i in range(iterations):
        positions.append([])
        for particle in particles:
            w = inertia_strategy.get_inertia(i, particles)
            particle.update(w)
            positions[i].append(
                {
                    "position": particle.position.tolist(),
                    "velocity": particle.velocity.tolist(),
                }
            )
        global_best_history.append(globals.best_value)
        if globals.best_value < epsilon and convergence_iteration > i:
            convergence_iteration = i

    gd_positions = gradient_descent_op(
        iterations,
        objective_function,
    )
    with open(f"plot/{objective_function.name}.json", "w") as f:
        json.dump(positions, f, indent=4)

    with open(f"plot/{objective_function.name}_gd.json", "w") as f:
        json.dump(gd_positions, f, indent=4)

    print(f"found minimum: {globals.best_value} at {globals.best_position}")
    return global_best_history, globals.best_value, globals.best_position, convergence_iteration


def main():
    for func in (Rosenbrock(), Rastrigin()):
        iterations = 200
        history, best, position, convergence_iteration = PSO(
            objective_function=func,
            n_param=2,
            n_particles=10,
            iterations=iterations,
            inertia_strategy=DynamicAdaptiveStrategy(
                iterations
            ),  # RandomInertiaEvolutionaryStrategy(iterations),
            guess_random_range=60,
            gradient_coef=0,
            use_random_gradients=False
        )

        print(position)
        print(best)
        print(convergence_iteration)


if __name__ == "__main__":
    main()
