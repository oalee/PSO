from matplotlib import pyplot as plt

from InertiaStrategies import LinearInertia, DynamicAdaptiveStrategy
from ObjectiveFunctions import Rastrigin, Rosenbrock
from PSO import PSO

objective_function = Rosenbrock()
n_iteration = 1000
n_particle_list = [i for i in range(10, 110, 15)]
random_ranges = [i for i in range(1000, 11000, 1000)]

line_list = []

for random_range in random_ranges:
    convergence_iteration_list = []
    for n_particle in n_particle_list:
        history, value, position, convergence_iteration = PSO(
            objective_function=objective_function,
            n_param=2,
            n_particles=n_particle,
            iterations=n_iteration,
            inertia_strategy=DynamicAdaptiveStrategy(iterations=n_iteration),
            guess_random_range=random_range,
            gradient_coef=0.4
        )
        print(value, random_range,n_particle)
        convergence_iteration_list.append(value)
    line_list.append(convergence_iteration_list)




def plot_results(line_list):
    x = n_particle_list
    plt.yscale("log")
    for i, item in enumerate(line_list):
        plt.plot(x, item, label=f"random range: {random_ranges[i]}")
    plt.xlabel("number of particles")
    plt.ylabel("best global value")
    plt.legend()
    plt.show()

plot_results(line_list)
