# Quantum Portfolio Optimizer

[![Streamlit App](https://img.shields.io/badge/Live-App-blue)](https://quantumportfoliooptimizer.streamlit.app/)

---

## Overview

**Quantum Portfolio Optimizer** is a portfolio optimization project combining real financial data with advanced optimization techniques, including a classical brute-force solver and a quantum solver prototype using QAOA (Qiskit).  
The project fetches historical stock prices, computes returns and risk, formulates a QUBO model, and finds an optimal stock mix balancing return and risk.

> **Note:** The quantum solver is currently **paused** due to compatibility issues with Python 3.12+. Only the classical solver works on the deployed website.

---

## Features

- Real historical stock data retrieval using Yahoo Finance
- Data cleaning and calculation of annualized returns and covariance
- QUBO problem formulation for portfolio optimization with constraints
- Classical brute-force solver for exact optimization
- Quantum solver prototype with QAOA (requires Python 3.10 environment)
- Interactive Streamlit web app for easy portfolio analysis and visualization

---

## Live Demo

Try it out on [Streamlit Cloud](https://quantumportfoliooptimizer.streamlit.app/) — classical solver only.

---

## Installation & Setup (for Development)

1. Clone the repo:

   ```bash
   git clone https://github.com/Towaiji/quantum-portfolio-optimizer.git
   cd quantum-portfolio-optimizer
   ```
2. Create and activate a Python 3.10 virtual environment (required for quantum solver):

macOS/Linux:
```bash
python3.10 -m venv .venv
source .venv/bin/activate
```
Windows:
```powershell
python3.10 -m venv .venv
.\.venv\Scripts\activate
```
Install dependencies:
```bash
Copy
pip install -r requirements.txt
```

## Running
Classical Solver (Works in any Python 3.10+ environment)
```bash
python src/main.py
```
Quantum Solver (Requires Python 3.10 environment due to Qiskit compatibility)

-Activate your Python 3.10 virtual environment (see above).

-Run the same main.py script; quantum solver is toggled inside the code.

-Note: Quantum solver module is currently paused by default due to dependency conflicts.

## Usage
Input stock tickers, date ranges, and optimization parameters in the Streamlit app.

See recommended portfolio selections with risk/return visualizations.

Download results as CSV.

## Troubleshooting & Notes
The quantum solver depends on specific Qiskit versions compatible only with Python 3.10.x.

Streamlit Cloud currently uses Python 3.13, which conflicts with Qiskit dependencies; that’s why only the classical solver is deployed live.

Use runtime.txt with Python 3.10.x if deploying quantum solver in an environment supporting older Python versions.

## License
MIT License

## Acknowledgements
Yahoo Finance for stock data

Qiskit for quantum computing framework

Streamlit for web app framework
