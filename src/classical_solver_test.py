import pandas as pd
import numpy as np
from problem_formulation import construct_qubo
from classical_solver import solve_qubo_classically

# Load your data
df = pd.read_csv('data/stock_data.csv', index_col=0, parse_dates=True)
daily_returns = df.pct_change().dropna()
mu = daily_returns.mean() * 252
sigma = daily_returns.cov() * 252

Q = construct_qubo(mu, sigma, 3, lambda_val=1.0, gamma=1000.0)

best_solution, best_value = solve_qubo_classically(Q)
print("Best portfolio selection:", best_solution)
print("Minimum objective value:", best_value)

# Optionally, print which tickers were picked:
print("Selected tickers:", [ticker for i, ticker in enumerate(df.columns) if best_solution[i] == 1])
