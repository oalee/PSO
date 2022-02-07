import numpy as np

max_gradient = 10


def f(x):
    # simple function
    return 2 * x[0] ** 2 - 8 * x[0] + 1


class Rosenbrock:
    name = "rosenbrock"
    def __str__(self):
        return self.name
    def __call__(self, x):
        a = 0
        b = 1
        return (a - x[0]) ** 2 + b * (x[1] - x[0] ** 2) ** 2

    def gradient(self, x, max_gradient=max_gradient):
        a = 0
        b = 1
        dx1 = -2 * (a - x[0]) + b * -4 * x[0] * (x[1] - (x[0] ** 2))
        dx2 = 2 * b * (x[1] - (x[0] ** 2))
        return np.array([np.clip(dx1, -max_gradient, max_gradient), np.clip(dx2, -max_gradient, max_gradient)])


class Rastrigin:
    name = "rastrigin"
    def __str__(self):
        return self.name

    def __call__(self, x):
        value = (
                (x[0] ** 2 - 10 * np.cos(2 * np.pi * x[0]))
                + (x[1] ** 2 - 10 * np.cos(2 * np.pi * x[1]))
                + 20
        )
        return value

    def gradient(self, x, max_gradient=max_gradient):
        dx1 = 2 * x[0] + 20 * np.pi * np.sin(2 * np.pi * x[0])
        dx2 = 2 * x[1] + 20 * np.pi * np.sin(2 * np.pi * x[1])
        return np.array([np.clip(dx1, -max_gradient, max_gradient), np.clip(dx2, -max_gradient, max_gradient)])
