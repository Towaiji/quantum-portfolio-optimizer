Quantum Portfolio Optimizer
Overview
Quantum Portfolio Optimizer is a quantum computing project that integrates real financial data with quantum optimization techniques to select an optimal portfolio of assets. The project downloads historical stock prices, computes expected annual returns and risk (covariance), formulates the portfolio optimization problem as a Quadratic Unconstrained Binary Optimization (QUBO) problem, and then solves it using both classical and quantum solvers (QAOA via Qiskit).

This project serves as an impressive portfolio piece demonstrating the application of quantum computing to real-world finance challenges.

Motivation
Modern portfolio optimization is an NP-hard problem, where selecting the best mix of assets to maximize returns while minimizing risk is computationally challenging. Quantum computing, particularly algorithms like QAOA, offers new ways to tackle these problems efficiently. This project aims to:

Showcase the integration of real financial data with quantum computing methods.

Compare classical brute-force solutions with quantum optimization.

Provide interactive analysis and visualizations to understand risk-return trade-offs.

Features
Real Data Integration:
Downloads historical stock data using Yahoo Finance via the data_collection.py module .

Data Processing:
Cleans data and calculates daily returns, annualized mean returns, and the covariance matrix.

QUBO Formulation:
Converts the portfolio optimization problem into a QUBO model using financial metrics (μ and Σ) via problem_formulation.py .

Classical and Quantum Solvers:
Benchmarks portfolio selection using both a classical brute-force solver (classical_solver.py ) and a quantum solver using QAOA (quantum_solver.py ).

Interactive Analysis:
Provides Jupyter notebooks (notebooks/analysis.ipynb) for data visualization and comparative analysis of results.

Repository Structure
graphql
Copy
quantum-portfolio-optimizer/
├── data/                     # Contains downloaded CSV data files
│   └── stock_data.csv        # Cleaned stock data (generated at runtime)
├── notebooks/                # Jupyter notebooks for interactive analysis
│   └── analysis.ipynb        # Notebook for visualizations and comparisons
├── src/                      # Source code for the project
│   ├── classical_solver.py   # Classical brute-force QUBO solver
│   ├── data_collection.py    # Module to download and process stock data
│   ├── problem_formulation.py# Constructs the QUBO matrix from financial data
│   ├── quantum_solver.py     # Quantum optimization using QAOA (Qiskit)
│   └── main.py               # Main script that integrates the full pipeline
├── tests/                    # (Optional) Unit tests for modules
├── README.md                 # This file
└── requirements.txt          # List of Python dependencies
