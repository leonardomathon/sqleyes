"""Utility functions w.r.t code complexity metrics"""
import math


def halstead_metrics(n1, n2, N1, N2):
    """
    Compute Halstead metrics for a given program.

    Parameters:
        n1 (int): Number of unique operators in the query.
        n2 (int): Number of unique operands in the query.
        N1 (int): Number of operators in the query.
        N2 (int): Number of operands in the query.

    Returns:
        N (int): Program length.
        n (int): Program vocabulary.
        V (float): Program volume.
        D (float): Program difficulty.
        E (float): Program effort.
    """
    # Program length
    N = N1 + N2

    # Program vocabulary
    n = n1 + n2

    # Volume
    V = N * math.log2(n)

    # Difficulty
    D = n1/2 * N2/n2

    # Effort
    E = D * V

    return (N, n, V, D, E)