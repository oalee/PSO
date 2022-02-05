import numpy as np

from InertiaStrategies import ChaoticDescendingInertia, RandomInertiaEvolutionaryStrategy
from Particle import Particle, Globals
import json


def f(x):
    # simple function
    return 2 * x[0] ** 2 - 8 * x[0] + 1


def f_rosenbrock(x):
    a = 0
    b = 1
    return (a - x[0]) ** 2 + b * (x[1] - x[0] ** 2) ** 2


def f_rastrigin(x):
    value = (x[0] ** 2 - 10 * np.cos(2 * np.pi * x[0])) + \
            (x[1] ** 2 - 10 * np.cos(2 * np.pi * x[1])) + 20
    return value


def PSO(objective_function, n_particles, iterations, n_param, inertia_strategy):
    # initialize the particles
    particles = []
    globals = Globals(n_param)
    for i in range(n_particles):
        particle = Particle(globals, objective_function)
        particles.append(particle)

    positions = []

    for i in range(iterations):
        positions.append([])
        for particle in particles:
            w = inertia_strategy.get_inertia(i, particles)
            particle.update(w)
            positions[i].append({'position': particle.position, 'velocity': particle.velocity})

        # print("iteration {} best at {}".format(particles[0].get_g_best_value(), particles[0].get_g_best_position()))
    with open('plot/position.json', 'w') as f:
        json.dump(positions, f, indent=4)
    print(
        "found minimum : {} at {}".format(
            globals.best_value, globals.best_position
        )
    )
    return globals.best_value, globals.best_position


# Running the PSO

value, position = PSO(
    objective_function=f_rosenbrock,
    n_param=2,
    n_particles=10,
    iterations=100,
    inertia_strategy=RandomInertiaEvolutionaryStrategy()
)
# gives the wrong position but correct minimum
print(position)
print(f_rosenbrock(position))
