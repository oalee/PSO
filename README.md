# Particle Swarm Optimization and Gradient Descent
Particle Swarm Optimization(PSO) is an optimization method to find the global minimum of a function using multiple particles, velocity and information sharing between the particles about their knowledge of closet minimum. Gradient Descent uses the gradient of the function to update it position and hopefully reach the global minima. Gradient Descent falls short to PSO when we have a non-convex function with large spaces of local minimas, while as the PSO can find the global minima, GD cannot converge using the Rosenbroch or Rastigirn function.

# Running
For running this project, you need to run the PSO.py `python PSO.py`, note that the hyperparameters are hardcoded in the main method of the PSO, by changing the parameters such as the range initial position of the particle and running the `PSO.py`, a json file will be generated. To run the visualization of the particles and the objective function, you can use a static file server on the `docs` folder, such as:
```
cd /path/to/project
cd docs
python -m http.server
``` 

Note that the green particle is the visualization for Gradient Descent position and the orange particles are PSO particles.

# Live version
You can find the live version on [this](https://lrhm.github.io/particle-swarm-optimization-and-gradient-descent/) link. 

# Parameters
Here is the list of the parameters used in our PSO:
## Iterations
The number of iterations used for both PSO and GD.

## Objective Function
The objective function for the optimization problem, can be Rastigin or Rosenbroch  or any objective function class that implements the nessecary methods defined in `ObjectiveFunctions.py`

## N_Particles
The number of particles for the PSO

## Inertia Strategy
When using the PSO, we need to have a strategy for exploration vs exploitation. In the vanilla PSO, its a linear function from a number such as 0.9 to 0.4, meaning at first iterations it favors exploration and linearly converges to exploitation. 
Here we have implemented 4 different strategies that you can try and use, namely `LinearInertia`, `DynamicAdaptive`, `RandomInertiaEvolutionaryStrategy` and `ChaoticDescendingInertia`. While the linear inertia usually works with enough interations, a more advanced method such as `RandomInertiaEvolutionaryStrategy` can converge quicker with doing exploration at more iterations and thus has a better chance of escaping the local minima.

## Guess Random Range
The initial guess range for the position of both PSO and GD particles. The bigger the range the harder this problem becomes as the particles are further away from the global minima.

## Gradient Coeff
Used for combining the PSO and GD.
Must be between 0 and 1, when setting to 0 the algorithm is the vanilla PSO, with other values it uses the gradient of the function and adds it to the velocity of particles with `-(1-a) * d * gradient(at_this_point)` whereas a is the inertia at that iteration and d is this gradient coefficient. Using (1-a) allows us to do more exploration at first, and eventually use more exploitation using the gradient. This gradient coefficient does not help when we use the rastigin or rosenbroch objective function as the gradient is actually misleading in this situation, however, if the gradient is useful using this variable would increase the performance of the PSO.

## Use Random Gradients
Used for combining PSO and GD. When set to true, at 20% of time randomly it uses the gradient of the function to calculate the next point and uses the vanilla PSO rules the other 80%.