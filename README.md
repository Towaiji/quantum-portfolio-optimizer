# Quantum Portfolio Optimizer

## Overview

**Quantum Portfolio Optimizer** is a quantum computing project that integrates real financial data with quantum optimization techniques to select an optimal portfolio of assets.  
The project downloads historical stock prices, computes expected annual returns and risk (covariance), formulates the portfolio optimization problem as a Quadratic Unconstrained Binary Optimization (QUBO) problem, and solves it using both classical and quantum solvers (QAOA via Qiskit).

This project serves as an impressive portfolio piece demonstrating the application of quantum computing to real-world finance challenges.

---

## Motivation

Modern portfolio optimization is an NP-hard problem, where selecting the best mix of assets to maximize returns while minimizing risk is computationally challenging.  
Quantum computing, particularly algorithms like QAOA, offers new ways to tackle these problems efficiently.

This project aims to:
- Showcase the integration of real financial data with quantum computing methods.
- Compare classical brute-force solutions with quantum optimization.
- Provide interactive analysis and visualizations to understand risk-return trade-offs.

---

## Features

- **Real Data Integration:**  
  Downloads historical stock data using Yahoo Finance (`data_collection.py`).

- **Data Processing:**  
  Cleans data and calculates daily returns, annualized mean returns, and the covariance matrix.

- **QUBO Formulation:**  
  Converts the portfolio optimization problem into a QUBO model (`problem_formulation.py`).

- **Classical and Quantum Solvers:**  
  Benchmarks solutions using a classical brute-force solver (`classical_solver.py`) and a quantum solver with QAOA (`quantum_solver.py`).

- **Interactive Analysis:**  
  Provides a Jupyter Notebook (`notebooks/analysis.ipynb`) for visualizations and comparative analysis.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Towaiji/quantum-portfolio-optimizer.git
cd quantum-portfolio-optimizer
```

2. Create and Activate Virtual Environment
For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```
For Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
Ensure you have the latest versions:
```
```bash
pip install --upgrade qiskit qiskit-optimization
```
Usage
Running the Full Pipeline

```bash
python src/main.py
This script will:
```

Download and clean stock data

Calculate annual returns and risks

Build the QUBO model

Solve it using both classical and quantum methods

Print results

Running Interactive Analysis
```bash
jupyter notebook notebooks/analysis.ipynb
```

## Use the notebook to explore:

Stock data

Daily returns

Risk-return profiles

QUBO matrix

Comparison of classical vs quantum solutions

**Contributing**

Contributions are welcome! Please open issues or pull requests.

## License

[MIT License]

## Acknowledgements

Yahoo Finance for providing financial data.

Qiskit for providing the quantum computing framework.

Inspirations from research in quantum portfolio optimization.

