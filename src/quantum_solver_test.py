from data_collection import calculate_returns_and_risk
from problem_formulation import construct_qubo
from quantum_solver import solve_qubo

import os
import numpy as np
import pandas as pd

def main():
    data_path = os.path.join("data", "stock_data.csv")
    df = pd.read_csv(data_path, index_col=0, parse_dates=True)
    mean_returns, cov_matrix = calculate_returns_and_risk(df)
    budget = 2
    risk_aversion = 0.1
    Q = construct_qubo(mean_returns, cov_matrix, budget, risk_aversion)
    max_allowed = 5.0
    max_abs = np.abs(Q).max()
    if max_abs > max_allowed:
        scale = max_abs / max_allowed
        print(f"Scaling QUBO by {scale}")
        Q = Q / scale

    Q = np.array(Q, dtype=np.float32)  # <- Extra safe conversion

    print("QUBO matrix:\n", Q)
    result = solve_qubo(Q, reps=1)

    print("\nQuantum Optimization Result:")
    if hasattr(result, "x"):
        solution = np.array(result.x)
        print("Quantum best portfolio selection:", solution)
        print("Quantum objective value:", result.fval)
        tickers = list(mean_returns.index)
        selected = np.where(solution == 1)[0]
        print("Selected tickers:", [tickers[i] for i in selected])
    else:
        print("Result object does not have 'x' attribute! Raw result:")
        print(result)

if __name__ == "__main__":
    main()
