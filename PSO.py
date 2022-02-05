import numpy as np
from Particle import Particle, Globals


def f(x):
    # simple function
    return 2 * x[0] ** 2 - 8 * x[0] + 1


def f_rosenbrock(x):
    a = 0
    b = 1
    return (a - x[0]) ** 2 + b * (x[1] - x[0] ** 2) ** 2

def f_rastrigin(x):
    Y = (x[0] ** 2 - 10 * np.cos(2 * np.pi * x[0])) + \
        (x[1] ** 2 - 10 * np.cos(2 * np.pi * x[1])) + 20
    return Y


def PSO(objective_function, start_location, n_particles, iterations):
    # initialize the particles
    particles = []
    globals = Globals(len(start_location))
    for i in range(n_particles):
        particle = Particle(globals, start_location, objective_function)
        particles.append(particle)

    # TODO will do this in a betterway, but it works!
    inertia_list = np.linspace(0.9, 0.4, iterations)

    # update the particles
    for i in range(len(inertia_list)):
        for particle in particles:
            particle.update(inertia_list[i])
        print("iteration {}, {} best at {}".format(i, globals.best_value, globals.best_position))

    print(
        "found minimum : {} at {}".format(
            globals.best_value, globals.best_position
        )
    )
    return globals.best_value, globals.best_position


# Running the PSO

value, position = PSO(
    objective_function=f_rastrigin,
    start_location=[1,2],
    n_particles=10,
    iterations=1000,
)
# gives the wrong position but correct minimum
print(position)
print(f_rastrigin(position))
