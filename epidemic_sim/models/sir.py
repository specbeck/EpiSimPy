import numpy as np
from scipy.integrate import solve_ivp


def sir_model(t, x, beta, gamma):
    """
    Calculates the derivatives for the SIR model.

    Parameters:
    t: float
        Time (not explicitly used here as there's no time dependence in equations).
    x: list or numpy array
        Current values of variables [S, I, R].
    beta: float
        Infectivity
    gamma: float
        Rate of recovery

    Returns:
    list
        Derivatives [dS/dt, dI/dt, dR/dt].
    """
    S, I, R = x

    dS = -beta * S * I
    dI = beta * S * I - gamma * I
    dR = gamma * I

    return [dS, dI, dR]


def solve_sir(inits=[499, 1, 0], beta, gamma, time_points=np.arange(0, 100.1, 0.1)):
    # Calculate and print R_0
    N = sum(inits)
    R_0 = beta * N / gamma
    print(f"R_0 = {R_0:.2f}")


    # Solve the differential equations using solve_ivp
    result = solve_ivp(
        fun=lambda t, y: sir_model(t, y, parms), # use of lambda functions
        t_span=(time_points[0], time_points[-1]),
        y0=inits,
        t_eval=time_points,
        vectorized=False
    )

    # Extract the solution
    S, I, R = result.y
    return [S, I, R]
