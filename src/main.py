from datetime import datetime

from classical_solver import solve_qubo_classically
from data_collection import calculate_returns_and_risk, clean_and_save_data, download_stock_data
from problem_formulation import construct_qubo
from quantum_solver import solve_qubo
import numpy as np

def main():
    # Load and process the data
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'JPM']
    start_date = '2020-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')
    csv_filename = 'data/stock_data.csv'

    stock_data = download_stock_data(tickers, start_date, end_date)
    clean_data = clean_and_save_data(stock_data, csv_filename)
    mu, Sigma = calculate_returns_and_risk(clean_data)

    # --- Keep mu and Sigma as pandas for .iloc in construct_qubo ---
    budget = 2
    risk_aversion = 1.0
    gamma = 10.0
    Q = construct_qubo(mu, Sigma, K=budget, lambda_val=risk_aversion, gamma=gamma)

    # Optionally scale Q for quantum solver to avoid overflow
    max_allowed = 5.0
    max_abs = np.abs(Q).max()
    if max_abs > max_allowed:
        scale = max_abs / max_allowed
        print(f"Scaling QUBO by {scale}")
        Q = Q / scale
    Q = np.array(Q, dtype=np.float32)

    # --- Solve classically ---
    classical_solution, classical_obj = solve_qubo_classically(Q)
    classical_selected = [tickers[i] for i, bit in enumerate(classical_solution) if bit == 1]
    print("\nClassical Solver Result:")
    print("  Best bitstring:", classical_solution)
    print("  Objective value:", classical_obj)
    print("  Selected tickers:", classical_selected)

    # --- Solve with Quantum (QAOA) ---
    quantum_result = solve_qubo(Q, reps=1)
    if hasattr(quantum_result, "x"):
        quantum_solution = np.array(quantum_result.x)
        quantum_selected = [tickers[i] for i, bit in enumerate(quantum_solution) if bit == 1]
        print("\nQuantum Solver Result:")
        print("  Best bitstring:", quantum_solution)
        print("  Objective value:", quantum_result.fval)
        print("  Selected tickers:", quantum_selected)
    else:
        print("\nQuantum Solver did not return solution bitstring. Raw result:", quantum_result)

if __name__ == "__main__":
    main()
