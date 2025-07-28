import numpy as np
from qiskit_aer import Aer
from qiskit_algorithms import QAOA
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.problems import QuadraticProgram

def qubo_to_quadratic_program(Q):
    """
    Converts a QUBO matrix to a Quadratic Program.
    
    Parameters:
        Q (np.array): The QUBO matrix.
        
    Returns:
        QuadraticProgram: A Qiskit Quadratic Program object representing the QUBO.
    """
    n = Q.shape[0] 
    qp = QuadraticProgram() 
    
    # Create binary variables x_0, x_1, ..., x_(n-1)
    for i in range(n):
        qp.binary_var(name=f'x_{i}')
    
    # Add linear terms from the diagonal of Q
    linear = {f'x_{i}': Q[i, i] for i in range(n)}
    
    # Add quadratic terms from off-diagonals
    quadratic = {}
    for i in range(n):
        for j in range(i+1, n):
            if Q[i, j] != 0:
                quadratic[(f'x_{i}', f'x_{j}')] = Q[i, j]
    
    qp.minimize(linear=linear, quadratic=quadratic)
    return qp

def solve_qubo(Q, p=1):
    """
    Solves a QUBO problem using QAOA and returns the solution.
    
    Parameters:
        Q (np.array): The QUBO matrix.
        p (int): The depth of the QAOA circuit.
        
    Returns:
        dict: A dictionary with the solution variables and their values.
    """
    # Convert QUBO to QuadraticProgram
    qp = qubo_to_quadratic_program(Q)
    
    # Choose a backend simulator
    backend = Aer.get_backend('qasm_simulator')
    
    # Set up QAOA with a given number of repetitions (depth)
    qaoa = QAOA(quantum_instance=backend, reps=p)
    
    # Wrap QAOA in the MinimumEigenOptimizer
    optimizer = MinimumEigenOptimizer(qaoa)
    
    # Solve the problem
    result = optimizer.solve(qp)
    return result

if __name__ == "__main__":
    # For demonstration, we import the QUBO construction function
    from problem_formulation import construct_qubo
    
    # Dummy data for testing: (replace with your actual mu and Sigma later)
    mu_example = np.array([0.15, 0.12, 0.18, 0.14, 0.10])
    Sigma_example = np.array([
        [0.10, 0.02, 0.04, 0.01, 0.03],
        [0.02, 0.08, 0.01, 0.03, 0.02],
        [0.04, 0.01, 0.12, 0.02, 0.04],
        [0.01, 0.03, 0.02, 0.09, 0.01],
        [0.03, 0.02, 0.04, 0.01, 0.07]
    ])
    K_example = 2  # For example, select 2 stocks out of 5
    
    # Construct the QUBO matrix from the portfolio optimization formulation
    Q = construct_qubo(mu_example, Sigma_example, K_example, lambda_val=1.0, gamma=10.0)
    print("Constructed QUBO matrix:")
    print(Q)
    
    # Solve the QUBO using QAOA
    result = solve_qubo(Q, reps=1)
    print("\nOptimization Result:")
    print(result)