from InertiaStrategies import DynamicAdaptiveStrategy
from ObjectiveFunctions import Rosenbrock, Rastrigin
from PSO import PSO

iterations = 200
hist = {}
for func in (Rosenbrock(), Rastrigin()):
    hist[func.name] = {}
    total = 0
    for i in range(1000):
        history, best, position, convergence_iteration = PSO(
            objective_function=func,
            n_param=2,
            n_particles=10,
            iterations=iterations,
            inertia_strategy=DynamicAdaptiveStrategy(
                iterations
            ),  # RandomInertiaEvolutionaryStrategy(iterations),
            guess_random_range=200,
            gradient_coef=0,
            use_random_gradients=False
        )
        total += convergence_iteration

    print(func.name, total / 1000)


print('------- now with random gradients -----------')
for func in (Rosenbrock(), Rastrigin()):
    hist[func.name] = {}
    total = 0
    for i in range(1000):
        history, best, position, convergence_iteration = PSO(
            objective_function=func,
            n_param=2,
            n_particles=10,
            iterations=iterations,
            inertia_strategy=DynamicAdaptiveStrategy(
                iterations
            ),  # RandomInertiaEvolutionaryStrategy(iterations),
            guess_random_range=200,
            gradient_coef=0,
            use_random_gradients=True
        )
        total += convergence_iteration

    print(func.name, total / 1000)
