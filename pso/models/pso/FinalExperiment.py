import random as rand

from .inertia_strategies import DynamicAdaptiveStrategy
from ObjectiveFunctions import Rosenbrock, Rastrigin
from PSO import PSO

iterations = 1000
no_grad = []
with_grad = []

hist = {}
for func in (Rosenbrock(), Rastrigin()):
    hist[func.name] = {}
    total = 0
    for i in range(100):
        history, best, position, convergence_iteration = PSO(
            objective_function=func,
            n_param=2,
            n_particles=30,
            iterations=iterations,
            inertia_strategy=DynamicAdaptiveStrategy(
                iterations
            ),  # RandomInertiaEvolutionaryStrategy(iterations),
            guess_random_range=10,
            gradient_coef=0,
            use_random_gradients=False,
            seed=rand.randint(0, 1241231)
        )
        total += convergence_iteration

    no_grad.append((func.name, total / 100))


print('------- now with random gradients -----------')
for func in (Rosenbrock(), Rastrigin()):
    hist[func.name] = {}
    total = 0
    for i in range(100):
        history, best, position, convergence_iteration = PSO(
            objective_function=func,
            n_param=2,
            n_particles=30,
            iterations=iterations,
            inertia_strategy=DynamicAdaptiveStrategy(
                iterations
            ),  # RandomInertiaEvolutionaryStrategy(iterations),
            guess_random_range=10,
            gradient_coef=0.2,
            use_random_gradients=True,
            seed=rand.randint(0, 1241231)
        )
        total += convergence_iteration

    with_grad.append((func.name, total / 100))


for i in no_grad:
    print("no gradient:", i)

for i in with_grad:
    print("with gradient:", i)

