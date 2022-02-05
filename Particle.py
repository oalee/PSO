import random
import numpy as np

g_best_position = []
g_best_value = float("inf")

max_velocity = 0.5


class Particle:
    def __init__(self, start_location, objective_function):
        global n_dimension
        n_dimension = len(start_location)
        self.position = []
        self.velocity = []
        self.personal_best_position = []
        self.objective_function = objective_function

        # initialize the position and velocity of particle
        for i in range(n_dimension):
            self.position.append(random.uniform(-1, 1))
            self.personal_best_position.append(random.uniform(-1, 1))
            self.velocity.append(random.uniform(-1, 1))
            g_best_position.append(random.uniform(-1, 1))

        self.fitness = objective_function(self.position)


    def update(self, w):

        global g_best_position
        global g_best_value

        # calculate and update position and velocity
        for i in range(n_dimension):
            # maybe have R1, R2 etc?
            R = random.random()
            b, c = 2, 2
            new_velocity = w * self.velocity[i] + b * R * (self.personal_best_position[i] - self.position[i]) + c * R * (g_best_position[i] - self.position[i])
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
            self.personal_best_position = self.position
            # Update the gbest
            if new_fitness < g_best_value:
                g_best_position = self.position
                g_best_value = self.objective_function(self.position)

        self.fitness = new_fitness

    def get_g_best_position(self):
        return g_best_position
    def get_g_best_value(self):
        return g_best_value


