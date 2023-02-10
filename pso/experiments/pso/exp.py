from ...models.pso import PSO, LinearInertia, RandomInertiaEvolutionaryStrategy, ChaoticDescendingInertia, DynamicAdaptiveStrategy, Rosenbrock, Rastrigin
import yerbamate

env = yerbamate.Environment()

if env.rastgirin:
    objective_function = Rastrigin()
else:
    objective_function = Rosenbrock()

history, b_value, b_position, convergance_iteration = PSO(
    objective_function=objective_function,
    n_param=2,
    n_particles=30,
    iterations=1000,
    inertia_strategy=DynamicAdaptiveStrategy(iterations=1000),
    guess_random_range=10,
    gradient_coef=0,
    use_random_gradients=False,
    seed=42,
)

