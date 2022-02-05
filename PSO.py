import numpy as np
from Particle import Particle


def f(x):
    #simple function
    return 2*x[0]**2-8*x[0]+1


def PSO(objective_function, start_location, n_particles, iterations):

    #initialize the particles
    particles = []

    for i in range(n_particles):
            particle = Particle(start_location, objective_function)
            particles.append(particle)

    #will do this in a betterway
    inertia_list = np.linspace(0.9, 0.4, iterations)
    #update the particles
    for i in range(len(inertia_list)):
        for particle in particles:
            particle.update(inertia_list[i])
        print("iteration {} best at {}".format(particles[0].get_g_best_value(), particles[0].get_g_best_position() ))

    print("found minimum : {} at {}".format(particles[0].get_g_best_value(), particles[0].get_g_best_position() ))
    return particles[0].get_g_best_value(), particles[0].get_g_best_position()


#Running the PSO

value, position = PSO(objective_function=f, start_location=[10], n_particles=10, iterations=100)
#gives the wrong position but correct minimum
print(f(position))

