Quantum Portfolio Optimizer
Overview
Quantum Portfolio Optimizer is a quantum computing project that leverages real-world financial data to optimize an investment portfolio. The project uses historical stock prices to compute expected returns and risk (via covariance), formulates a portfolio optimization problem as a QUBO (Quadratic Unconstrained Binary Optimization) problem, and then solves it using both classical brute-force methods and quantum algorithms (QAOA via Qiskit).

This project is designed to showcase the potential of quantum computing in finance and optimization, and it serves as an impressive portfolio piece for roles in quantum computing engineering and related fields.

Motivation
In traditional portfolio optimization, selecting the best combination of assets to maximize returns and minimize risk is a complex, NP-hard problem. Quantum computing promises a new approach by exploiting quantum parallelism and novel optimization algorithms like QAOA. This project aims to:

Demonstrate end-to-end integration of real financial data with quantum optimization.

Compare classical and quantum solution approaches.

Provide insights and visualizations of portfolio selection, risk, and return trade-offs.

Features
Real Data Integration: Downloads and cleans historical stock data using Yahoo Finance.

Data Processing: Calculates daily returns, annualized mean returns, and covariance matrices.

QUBO Formulation: Converts the portfolio optimization problem into a QUBO model.

Classical Solver: Implements a brute-force classical solver for small-scale problems.

Quantum Solver: Uses Qiskit's QAOA to solve the QUBO on a quantum simulator.

Analysis & Visualization: Interactive Jupyter notebooks to explore, analyze, and visualize the data and optimization results.

Repository Structure
graphql
Copy
quantum-portfolio-optimizer/
├── data/                     # Contains downloaded CSV data files
│   └── stock_data.csv        # Cleaned stock data
├── notebooks/                # Jupyter notebooks for interactive analysis
│   └── analysis.ipynb        # Analysis and visualization of data and results
├── src/                      # Source code for the project
│   ├── classical_solver.py   # Classical brute-force QUBO solver
│   ├── data_collection.py    # Module to download and clean stock data
│   ├── problem_formulation.py# Constructs the QUBO matrix from financial data
│   ├── quantum_solver.py     # Quantum optimization using QAOA and Qiskit
│  
