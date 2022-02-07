import random
import numpy as np
import ipdb


def rosenbroch_gradient(x):
    a = 0
    b = 1
    dx1 = -2 * (a - x[0]) + b * -4 * x[0] * (x[1] - (x[0] ** 2))
    dx2 = 2 * b * (x[1] - (x[0] ** 2))
    return np.array([dx1, dx2])


max_velocity = 3


class Globals:
    def __init__(self, n_dimension, position_range):
        self.best_position = np.random.uniform(
            -position_range, position_range, n_dimension
        )
        self.best_value = float("inf")
        self.n_dimension = n_dimension


class Particle:
    # D is the gradient hyper parameter
    def __init__(self, globals, objective_function, position_range=100, d=0):
        self.globals = globals
        self.personal_best_position = []
        self.objective_function = objective_function
        self.all_fitnesses = []
        self.d = d

        # initialize the position and velocity of particle
        self.position = np.random.uniform(
            -position_range, position_range, globals.n_dimension
        )
        self.personal_best_position = np.random.uniform(
            -position_range, position_range, globals.n_dimension
        )
        self.velocity = np.random.uniform(
            -max_velocity, max_velocity, globals.n_dimension
        )

        self.fitness = objective_function(self.position)
        self.all_fitnesses.append(self.fitness)

    def update(self, a):

        # calculate and update position and velocity
        # maybe have R1, R2 etc?
        R = np.random.random(2)
        b, c = 2, 2

        gradient = self.objective_function.gradient(self.position)
        new_velocity = (
            a * self.velocity
            + b * R * (self.personal_best_position - self.position)
            + c * R * (self.globals.best_position - self.position)
            - self.d * (1 - a) * gradient
        )
        # cap velocity at
        new_velocity = np.clip(new_velocity, -max_velocity, max_velocity)

        # update the velocity
        self.velocity = new_velocity

        # update the position
        self.position += new_velocity

        # calculate and update personal and global best
        new_fitness = self.objective_function(self.position)

        if new_fitness < self.fitness:
            self.personal_best_position = self.position.copy()
            # Update the gbest
            if new_fitness < self.globals.best_value:
                self.globals.best_position = self.position.copy()
                self.globals.best_value = self.objective_function(
                    self.position
                )

        self.fitness = new_fitness
        self.all_fitnesses.append(self.fitness)

    def get_fitness_iteration(self, i):
        return self.all_fitnesses[i]


"""
class Particle:
    # D is the gradient hyper parameter
    def __init__(self, globals, objective_function, position_range=100, d=0):
        self.globals = globals
        self.objective_function = objective_function
        self.all_fitnesses = []
        self.d = d
        self.position = np.random.uniform(
            -position_range, position_range, globals.n_dimension
        )
        self.personal_best_position = np.random.uniform(
            -1, 1, globals.n_dimension
        )
        self.velocity = np.random.uniform(-1, 1, globals.n_dimension)
        self.fitness = objective_function(self.position)
        self.all_fitnesses.append(self.fitness)

    def update(self, a):

        # calculate and update position and velocity
        # for i in range(self.globals.n_dimension):
        # maybe have R1, R2 etc?
        R = np.random.random(2)
        b, c = 2, 2
        gradient = rosenbroch_gradient(self.position)
        new_velocity = (
            a * self.velocity
            + b * R * (self.personal_best_position - self.position)
            + c * R * (self.globals.best_position - self.position)
            - self.d * a * gradient
        )

        # cap velocity
        new_velocity = np.clip(new_velocity, -max_velocity, max_velocity)

        # update the velocity
        self.velocity = new_velocity

        # update the position
        self.position += new_velocity

        # calculate and update personal and global best
        new_fitness = self.objective_function(self.position)

        if new_fitness < self.fitness:
            self.personal_best_position = self.position.copy()
            # Update the gbest
            if new_fitness < self.globals.best_value:
                self.globals.best_position = self.position.copy()
                self.globals.best_value = self.objective_function(
                    self.position
                )

        self.fitness = new_fitness
        self.all_fitnesses.append(self.fitness)

    def get_fitness_iteration(self, i):
        return self.all_fitnesses[i]
"""
