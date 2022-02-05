import numpy as np

from InertiaStrategies import ChaoticDescendingInertia, RandomInertiaEvolutionaryStrategy
from Particle import Particle, Globals


def f(x):
    # simple function
    return 2 * x[0] ** 2 - 8 * x[0] + 1


def f_rosenbrock(x):
    a = 0
    b = 1
    return (a - x[0]) ** 2 + b * (x[1] - x[0] ** 2) ** 2


def PSO(objective_function, start_location, n_particles, iterations,
        inertia_strategy):
    # initialize the particles
    particles = []
    globals = Globals(len(start_location))
    for i in range(n_particles):
        particle = Particle(globals, start_location, objective_function)
        particles.append(particle)

    # update the particles
    for i in range(iterations):
        for particle in particles:
            w = inertia_strategy.get_inertia(i, particles)
            particle.update(w)
        # print("iteration {} best at {}".format(particles[0].get_g_best_value(), particles[0].get_g_best_position()))

    print(
        "found minimum : {} at {}".format(
            globals.best_value, globals.best_position
        )
    )
    return globals.best_value, globals.best_position


# Running the PSO

value, position = PSO(
    objective_function=f_rosenbrock,
    start_location=[1, 2],
    n_particles=10,
    iterations=100,
    inertia_strategy=RandomInertiaEvolutionaryStrategy()
)
# gives the wrong position but correct minimum
print(position)
print(f_rosenbrock(position))
