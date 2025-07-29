import numpy as np

def construct_qubo(mu, Sigma, K, lambda_val=1.0, gamma=10.0):
    """
    Constructs the QUBO matrix for portfolio optimization.
    
    The objective is to maximize returns (represented by mu) and minimize risk (captured by Sigma).
    We model this as minimizing the following function:
    
        Objective = - sum(mu_i * x_i) + lambda_val * (x^T Sigma x)
        
    To enforce that exactly K stocks are selected, we add a constraint penalty:
    
        Constraint = gamma * (sum(x_i) - K)^2
    
    This function returns a QUBO matrix Q, such that minimizing x^T Q x over binary variables x 
    (where x_i = 1 if the asset is selected and 0 otherwise) solves our portfolio optimization problem.
    
    Parameters:
        mu (np.array): 1D array of annual mean returns for each asset.
        Sigma (np.array): 2D array representing the annual covariance matrix.
        K (int): Desired number of stocks to include in the portfolio.
        lambda_val (float): Weighting factor for the risk term.
        gamma (float): Penalty coefficient for the constraint.
        
    Returns:
        Q (np.array): The QUBO matrix.
    """
    N = len(mu)
    Q = np.zeros((N, N))
    
    # Objective: -mu_i * x_i  + lambda_val * (Sigma_ij * x_i * x_j)
    for i in range(N):
        # Linear part: -mu_i
        Q[i, i] += -mu.iloc[i]
        for j in range(i, N):
            # Quadratic risk term from covariance matrix
            Q[i, j] += lambda_val * Sigma.iloc[i, j]
            if i != j:
                Q[j, i] = Q[i, j]
    
    # Constraint: gamma * (sum_i x_i - K)^2
    # Expand the square: sum_i x_i^2 + 2*sum_{i<j} x_i * x_j - 2*K * sum_i x_i + K^2
    # Since x_i is binary, x_i^2 = x_i. We ignore the constant term (K^2) as it doesn't affect optimization.
    for i in range(N):
        # Add the x_i term from the constraint
        Q[i, i] += gamma
        for j in range(i+1, N):
            Q[i, j] += 2 * gamma
            Q[j, i] = Q[i, j]
    # Subtract 2 * gamma * K from the diagonal to complete the linear part of the constraint
    for i in range(N):
        Q[i, i] -= 2 * gamma * K
    
    return Q

# Example usage for testing the function
if __name__ == "__main__":
    import pandas as pd

    # Dummy example data
    mu_example = pd.Series([0.15, 0.12, 0.18, 0.14, 0.10])

    Sigma_example = pd.DataFrame([
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
