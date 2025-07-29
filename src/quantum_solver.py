import numpy as np
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.problems import QuadraticProgram
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler

def qubo_to_quadratic_program(Q):
    """
    Converts a QUBO matrix to a Qiskit QuadraticProgram.

    Parameters:
        Q (np.array): The QUBO matrix.

    Returns:
        QuadraticProgram: A Qiskit Quadratic Program object representing the QUBO.
    """
    n = Q.shape[0]
    qp = QuadraticProgram()
    for i in range(n):
        qp.binary_var(name=f'x_{i}')
    linear = {f'x_{i}': float(Q[i, i]) for i in range(n)}
    quadratic = {}
    for i in range(n):
        for j in range(i + 1, n):
            if Q[i, j] != 0:
                quadratic[(f'x_{i}', f'x_{j}')] = float(Q[i, j])
    qp.minimize(linear=linear, quadratic=quadratic)
    return qp

def solve_qubo(Q, reps=1):
    """
    Solves a QUBO problem using QAOA and returns the Qiskit optimization result.

    Parameters:
        Q (np.array): The QUBO matrix.
        reps (int): The depth of the QAOA circuit.

    Returns:
        OptimizationResult: Qiskit optimization result object, e.g., result.x for solution.
    """
    qp = qubo_to_quadratic_program(Q)
    sampler = Sampler()
    optimizer = COBYLA()
    qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=reps)
    optimizer_wrapper = MinimumEigenOptimizer(qaoa)
    result = optimizer_wrapper.solve(qp)
    return result

if __name__ == "__main__":
    from problem_formulation import construct_qubo

    mu_example = np.array([0.15, 0.12, 0.18, 0.14, 0.10])
    Sigma_example = np.array([
        [0.10, 0.02, 0.04, 0.01, 0.03],
        [0.02, 0.08, 0.01, 0.03, 0.02],
        [0.04, 0.01, 0.12, 0.02, 0.04],
        [0.01, 0.03, 0.02, 0.09, 0.01],
        [0.03, 0.02, 0.04, 0.01, 0.07]
    ])
    K_example = 2

    Q = construct_qubo(mu_example, Sigma_example, K_example, lambda_val=1.0, gamma=10.0)
    print("Constructed QUBO matrix:")
    print(Q)

    result = solve_qubo(Q, reps=1)
    print("\nOptimization Result:")
    print(result)
    if hasattr(result, "x"):
        print("Best solution (bitstring):", result.x)
        print("Objective value:", result.fval)
