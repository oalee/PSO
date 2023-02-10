import random

# import numpy as np

from .GradientDescent import gradient_descent_op

from .ParticleVectorized import Particle, Globals

import json

epsilon = 0.00000001


def f(x):
    # simple function
    return 2 * x[0] ** 2 - 8 * x[0] + 1


def PSO(
    objective_function,
    n_particles,
    iterations,
    n_param,
    inertia_strategy,
    guess_random_range,
    gradient_coef=0,
    seed=random.randint(0, 1241231),
    use_random_gradients=False,
    save_path = None,
):
    params = {
        "obj_f": objective_function,
        "n_par": n_particles,
        "iter": iterations,
        "in_srat": inertia_strategy,
        "rng": guess_random_range,
        "grd_coef": gradient_coef,
        "seed": seed,
        "rnd_grad": use_random_gradients,
    }

    # initialize the particles
    particles = []
    # np.random.seed(seed)
    random.seed(seed)

    globals = Globals(n_param, guess_random_range)
    for i in range(n_particles):
        particle = Particle(
            globals,
            objective_function,
            guess_random_range,
            gradient_coef,
            use_random_gradients,
        )
        particles.append(particle)

    positions = []
    global_best_history = []

    convergence_iteration = 1000

    for i in range(iterations):
        positions.append([])
        for particle in particles:
            w = inertia_strategy.get_inertia(i, particles)
            particle.update(w)
            positions[i].append(
                {
                    "position": particle.position.tolist(),
                    "velocity": particle.velocity.tolist(),
                }
            )
        global_best_history.append(globals.best_value)
        if globals.best_value < epsilon and convergence_iteration > i:
            convergence_iteration = i

    gd_positions = gradient_descent_op(
        iterations,
        objective_function,
    )
    file_name = (
        json.dumps(params, default=str)
        .replace(" ", "")
        .replace('"', "")
        .replace("{", "")
        .replace("}", "")
    )
    if save_path is None:
        save_path = "./plot/data/"
    else :
        save_path = save_path + "plot/data/"
    
    file_name = f"{save_path}{objective_function.name}.json"

    with open(
        file_name,
        "w",
    ) as f:
        json.dump(positions, f, indent=4)

    gd_file_name = f"{save_path}{objective_function.name}_gd.json"

    with open(
        gd_file_name,
        "w",
    ) as f:
        json.dump([[{"position": p}] for p in gd_positions], f, indent=4)

    print(f"found minimum of {objective_function.name}: {globals.best_value} at {globals.best_position}")
    return (
        global_best_history,
        globals.best_value,
        globals.best_position,
        convergence_iteration,
    )

