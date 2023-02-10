import matplotlib.pyplot as plt
from InertiaStrategies import (
    LinearInertia,
    RandomInertiaEvolutionaryStrategy,
    ChaoticDescendingInertia,
    DynamicAdaptiveStrategy,
)
from ObjectiveFunctions import f_rosenbrock, f_rastrigin
from PSO import PSO

objective_function = f_rosenbrock
n_particles = 10
n_iteration = 100
random_range = 50


def plot_history(history_list):
    x = [i for i in range(n_iteration)]
    plt.xlim(-1, n_iteration)
    LinearInertia = history_list[0]
    RandomInertiaEvolutionaryStrategy = history_list[1]
    ChaoticDescendingInertia = history_list[2]
    DynamicAdaptiveStrategy = history_list[3]
    plt.plot(x, LinearInertia, label="Linear Inertia")
    plt.plot(
        x,
        RandomInertiaEvolutionaryStrategy,
        label="Random Inertia Evolutionary Strategy",
    )
    plt.plot(x, ChaoticDescendingInertia, label="Chaotic Descending Inertia")
    plt.plot(x, DynamicAdaptiveStrategy, label="Dynamic Adaptive Strategy")
    plt.xlabel("iteration")
    plt.ylabel("global best value")
    plt.legend()
    plt.show()


histories = []

history, value, position = PSO(
    objective_function=objective_function,
    n_param=2,
    n_particles=n_particles,
    iterations=n_iteration,
    inertia_strategy=LinearInertia(iterations=n_iteration),
    guess_random_range=random_range,
)

histories.append(history)

history, value, position = PSO(
    objective_function=objective_function,
    n_param=2,
    n_particles=n_particles,
    iterations=n_iteration,
    inertia_strategy=RandomInertiaEvolutionaryStrategy(),
    guess_random_range=random_range,
)

histories.append(history)

history, value, position = PSO(
    objective_function=objective_function,
    n_param=2,
    n_particles=n_particles,
    iterations=n_iteration,
    inertia_strategy=ChaoticDescendingInertia(iterations=n_iteration),
    guess_random_range=random_range,
)

histories.append(history)


history, value, position = PSO(
    objective_function=objective_function,
    n_param=2,
    n_particles=n_particles,
    iterations=n_iteration,
    inertia_strategy=DynamicAdaptiveStrategy(iterations=n_iteration),
    guess_random_range=random_range,
)


histories.append(history)

plot_history(histories)


# Running the PSO
# inertia_strategies = [LinearInertia, RandomInertiaEvolutionaryStrategy, ChaoticDescendingInertia,
#                       DynamicAdaptiveStrategy]
# histories = []
# for strategy in inertia_strategies:
#     history, value, position = PSO(
#         objective_function=f_rosenbrock,
#         n_param=2,
#         n_particles=10,
#         iterations=n_iteration,
#         inertia_strategy=strategy
#     )
#     histories.append(history)
#
# plot_history(histories)
#
# print(position)
# print(f_rosenbrock(position))
