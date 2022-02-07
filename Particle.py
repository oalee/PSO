import random
import numpy as np

from ObjectiveFunctions import gradient_rastgirin, rosenbroch_gradient, f_rosenbrock

max_velocity = 0.5


class Globals:
    def __init__(self, n_dimension):
        self.best_position = []
        self.best_value = float("inf")
        self.n_dimension = n_dimension


class Particle:
    # D is the gradient hyper parameter
    def __init__(self, globals, objective_function, position_range=100, d=0):
        self.globals = globals
        self.position = []
        self.velocity = []
        self.personal_best_position = []
        self.objective_function = objective_function
        self.all_fitnesses = []
        self.d = d

        # initialize the position and velocity of particle
        for i in range(self.globals.n_dimension):
            self.position.append(random.uniform(-position_range, position_range))
            self.personal_best_position.append(random.uniform(-1, 1))
            self.velocity.append(random.uniform(-1, 1))
            self.globals.best_position.append(random.uniform(-1, 1))

        self.fitness = objective_function(self.position)
        self.all_fitnesses.append(self.fitness)

    def update(self, a):

        # calculate and update position and velocity

        gradient_func = rosenbroch_gradient if self.objective_function == f_rosenbrock else gradient_rastgirin

        for i in range(self.globals.n_dimension):
            # maybe have R1, R2 etc?
            R = random.random()
            b, c = 2, 2
            gradient = gradient_func(self.position)
            new_velocity = (
                    a * self.velocity[i]
                    + b * R * (self.personal_best_position[i] - self.position[i])
                    + c * R * (self.globals.best_position[i] - self.position[i])
                    - self.d * (1 - a) * gradient[i]
            )
            # cap velocity at
            if abs(new_velocity) > max_velocity:
                new_velocity = np.sign(new_velocity) * max_velocity

            # update the velocity
            self.velocity[i] = new_velocity

            # update the position
            new_position = self.position[i] + new_velocity
            self.position[i] = new_position

        # calculate and update personal and global best
        new_fitness = self.objective_function(self.position)

        if new_fitness < self.fitness:
            self.personal_best_position = self.position.copy()
            # Update the gbest
            if new_fitness < self.globals.best_value:
                self.globals.best_position = self.position.copy()
                self.globals.best_value = self.objective_function(self.position)

        self.fitness = new_fitness
        self.all_fitnesses.append(self.fitness)

    def get_fitness_iteration(self, i):
        return self.all_fitnesses[i]
