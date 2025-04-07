import numpy as np
import itertools

def solve_qubo_classically(Q):
    """
    Solves the QUBO problem by brute-force enumeration (suitable for small problems).
    
    Parameters:
        Q (np.array): The QUBO matrix.
        
    Returns:
        best_x (np.array): Binary vector (solution) that minimizes the QUBO objective.
        best_obj (float): The minimum objective value.
    """
    N = Q.shape[0]
    best_obj = float('inf')
    best_x = None
    
    # Enumerate all possible binary combinations of length N.
    for x_tuple in itertools.product([0, 1], repeat=N):
        x = np.array(x_tuple)
        obj = x.T @ Q @ x  # Compute the QUBO objective: x^T Q x
        if obj < best_obj:
            best_obj = obj
            best_x = x
            
    return best_x, best_obj

if __name__ == "__main__":
    # For testing purposes, import the QUBO construction function from problem_formulation.py
    from problem_formulation import construct_qubo

    # Example dummy data (replace these with your real mu and Sigma later)
    mu_example = np.array([0.15, 0.12, 0.18, 0.14, 0.10])  # Annual mean returns for 5 stocks
    Sigma_example = np.array([
        [0.10, 0.02, 0.04, 0.01, 0.03],
        [0.02, 0.08, 0.01, 0.03, 0.02],
        [0.04, 0.01, 0.12, 0.02, 0.04],
        [0.01, 0.03, 0.02, 0.09, 0.01],
        [0.03, 0.02, 0.04, 0.01, 0.07]
    ])
    K_example = 2  # For instance, select 2 stocks out of 5

    # Construct the QUBO matrix using the function from problem_formulation.py
    Q = construct_qubo(mu_example, Sigma_example, K_example, lambda_val=1.0, gamma=10.0)
    print("Constructed QUBO matrix:")
    print(Q)

    # Solve the QUBO problem using the classical solver
    best_solution, best_obj = solve_qubo_classically(Q)
    print("\nClassical Solver Result:")
    print("Best solution (binary vector):", best_solution)
    print("Objective value:", best_obj)
