from datetime import datetime

from classical_solver import solve_qubo_classically
from data_collection import calculate_returns_and_risk, clean_and_save_data, download_stock_data
from problem_formulation import construct_qubo
from quantum_solver import solve_qubo


def main():
    # Load and process the data
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'JPM']
    start_date = '2020-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')
    csv_filename = 'data/stock_data.csv'

    stock_data = download_stock_data(tickers, start_date, end_date)
    clean_data = clean_and_save_data(stock_data, csv_filename)
    mu, Sigma = calculate_returns_and_risk(clean_data)

    # Construct the QUBO matrix using real data
    # Convert mu and Sigma to numpy arrays if needed
    Q = construct_qubo(mu.values, Sigma.values, K=2, lambda_val=1.0, gamma=10.0)

    # Solve using classical and quantum solvers
    classical_solution, classical_obj = solve_qubo_classically(Q)
    quantum_result = solve_qubo(Q, p=1)

    print("Classical Solver Result:", classical_solution, classical_obj)
    print("Quantum Solver Result:", quantum_result)

if __name__ == "__main__":
    main()
