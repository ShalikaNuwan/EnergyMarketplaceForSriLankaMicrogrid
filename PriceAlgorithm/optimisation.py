import numpy as np
import pyswarms as ps

# Define constants
total_demand = 1000   # Example demand
energy_gen = 600      # Example solar generation
grid_supply = 500     # Grid supply (extra capacity)
solar_cost = 0.05     # Solar cost per unit

# Objective function (negated for minimization)
def objective(x):
    market_price = x[0]  # Single-variable optimization
    profit = total_demand * market_price - energy_gen * solar_cost
    
    # Constraint violations (penalty function)
    penalty = 0
    if total_demand > (energy_gen + grid_supply):  # Demand must be met
        penalty += 1000 * (total_demand - (energy_gen + grid_supply))
    if profit < 0:  # Profit must be non-negative
        penalty += 1000 * abs(profit)
    
    return -(profit - penalty)  # Subtract penalty to penalize bad solutions

# Define bounds
bounds = (np.array([10]), np.array([1000]))  # Market price range

# Set up PSO optimizer
optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=1, options={'c1': 1.5, 'c2': 1.5, 'w': 0.5}, bounds=bounds)

# Run optimization
best_cost, best_pos = optimizer.optimize(objective, iters=100)

print(f"Optimal Market Price: {best_pos[0]}")
