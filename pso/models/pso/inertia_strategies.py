# Random Inertia Weight and Evolutionary Strategy PSO
import math
import random

import numpy as np


class RandomInertiaEvolutionaryStrategy:

    def __str__(self):
        return "RandomInertiaEvolutionaryStrategy"

    def __init__(self, iterations=None, alpha_one=0.4, alpha_two=0.9):
        # Hyper parameters
        self.alpha_one = alpha_one
        self.alpha_two = alpha_two
        self.r = 0.1
        self.k = 1

    def get_inertia(self, i, all_particles):

        # self.r = random.uniform(0,1)

        probability = self.calc_probability(i, all_particles)
        if probability >= self.r:
            return self.alpha_one + self.r / 2.0
        return self.alpha_two + self.r / 2.0

    def calc_probability(self, i, all_particles):

        k = 1
        if i < k:
            return 1

        best_before = self.best_fitness(i - k, all_particles)
        now_best = self.best_fitness(i, all_particles)

        if best_before <= now_best:
            return 1

        return math.exp(-(best_before - now_best) / self.temperature(i, all_particles))

    def average_fitness(self, i, all_particles):
        return (1 / len(all_particles)) * (
            sum([particle.get_fitness_iteration(i) for particle in all_particles])
        )

    def best_fitness(self, i, all_particles):
        return min([particle.get_fitness_iteration(i) for particle in all_particles])

    def temperature(self, i, all_particles):
        avg = self.average_fitness(i, all_particles)
        best = self.best_fitness(i, all_particles)
        if best == 0:
            best = 1
        return (avg / best) - 1


class LinearInertia:

    def __str__(self):
        return "LinearInertia"

    def __init__(self, iterations, w_start=0.9, w_end=0.4):
        self.w_start = w_start
        self.w_end = w_end
        self.iterations = iterations
        self.inertia_list = np.linspace(w_start, w_end, iterations)

    def get_all_inertias(self):
        return self.inertia_list

    def get_inertia(self, i, all_particles):
        return self.inertia_list[i]


class ChaoticDescendingInertia:

    def __str__(self):
        return "ChaoticDescendingInertia"

    def __init__(self, iterations, initial_chaos=0.9, w_start=0.9, w_end=0.4):
        self.initial_chaos = initial_chaos
        self.chaos = initial_chaos
        self.w_start = w_start
        self.w_end = w_end
        self.iterations = iterations
        self.inertia = self.get_all_inertias()

    def chaos_value(self, prev_chaos):
        u = 4
        return u * prev_chaos * (1 - prev_chaos)

    def chaotic_descending_inertia(self, i, chaos):
        return (self.w_start - self.w_end) * (
                (self.iterations - i) / self.iterations
        ) + self.w_end * chaos

    def get_inertia(self, i, all_particles):
        return self.inertia[i]

    def get_all_inertias(self):
        result = []
        chaos = self.initial_chaos
        for i in range(self.iterations):
            w = self.chaotic_descending_inertia(i, chaos)
            chaos = self.chaos_value(chaos)
            # print(i, w, chaos)
            result.append(w)
        return result


class DynamicAdaptiveStrategy:

    def __str__(self):
        return "DynamicAdaptiveStrategy"

    def __init__(self, iterations, w_start=0.9, w_end=0.2):
        # Hyper parameters
        self.w_start = w_start
        self.w_end = w_end
        self.iterations = iterations

    def phi(self, i):
        return math.exp(-(i ** 2) / (2 * (self.iterations / 3) ** 2))

    def calc_E(self, i, all_particles):
        avg_fitness = self.average_fitness(i, all_particles)
        return (1 / len(all_particles)) * sum(
            [(particle.fitness - avg_fitness) ** 2 for particle in all_particles]
        )

    def calc_F(self, i, all_particles):
        return 1 - (2 / math.pi) * (math.atan(self.calc_E(i, all_particles)))

    def get_inertia(self, i, all_particles):
        return self.w_end + (self.w_start - self.w_end) * self.calc_F(
            i, all_particles
        ) * self.phi(i)

    def average_fitness(self, i, all_particles):
        return (1 / len(all_particles)) * (
            sum([particle.get_fitness_iteration(i) for particle in all_particles])
        )
