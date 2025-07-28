import unittest
import numpy as np
import os

from data_collection import calculate_returns_and_risk
from problem_formulation import construct_qubo
from quantum_solver import solve_qubo

class TestQuantumSolverIntegration(unittest.TestCase):
    def test_quantum_solver_on_real_data(self):
        # 1. Load data and calculate returns/risk
        data_path = os.path.join("data", "stock_data.csv")
        mean_returns, cov_matrix = calculate_returns_and_risk(data_path)

        # 2. Construct QUBO (fill with any additional required args)
        # Adjust these params as needed
        budget = 3  # number of assets to select (example)
        risk_aversion = 0.1
        Q = construct_qubo(mean_returns, cov_matrix, budget, risk_aversion)

        # 3. Run quantum solver
        result = solve_qubo(Q)

        # 4. Assertions: type/shape checks
        self.assertIsInstance(result, dict)
        self.assertIn("solution", result)
        self.assertIsInstance(result["solution"], np.ndarray)

        # 5. Optionally, check that the selected assets matches the budget constraint
        self.assertEqual(result["solution"].sum(), budget)

if __name__ == "__main__":
    unittest.main()
