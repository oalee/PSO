from InertiaStrategies import DynamicAdaptiveStrategy, RandomInertiaEvolutionaryStrategy
from ObjectiveFunctions import f_rosenbrock
from Particle import Particle, Globals
import json


def f(x):
    # simple function
    return 2 * x[0] ** 2 - 8 * x[0] + 1


def PSO(objective_function, n_particles, iterations, n_param, inertia_strategy, guess_random_range):
    # initialize the particles
    particles = []

    globals = Globals(n_param)
    for i in range(n_particles):
        particle = Particle(globals, objective_function, guess_random_range)
        particles.append(particle)

    positions = []
    global_best_history = []

    for i in range(iterations):
        positions.append([])
        for particle in particles:
            w = inertia_strategy.get_inertia(i, particles)
            particle.update(w)
            positions[i].append({'position': particle.position, 'velocity': particle.velocity})
        global_best_history.append(globals.best_value)

    with open('plot/position.json', 'w') as f:
        json.dump(positions, f, indent=4)
    print(
        "found minimum : {} at {}".format(
            globals.best_value, globals.best_position
        )
    )
    return global_best_history, globals.best_value, globals.best_position


(history, best, position) = PSO(objective_function=f_rosenbrock,
                                n_param=2,
                                n_particles=10,
                                iterations=100,
                                inertia_strategy=RandomInertiaEvolutionaryStrategy(),
                                guess_random_range=60
                                )

print(position)
print(best)
