def SEIRD(t, x, parms):
    """
    Calculates the derivatives for the SEIRD model.

    Parameters:
    t: float
        Time.
    x: list or numpy array
        Current values of variables [S, E, I, R, D].
    parms: dict
        Dictionary of parameters {'beta': ..., 'sigma': ..., 'r': ..., 'mu': ...}.

    Returns:
    list
        Derivatives [dS/dt, dE/dt, dI/dt, dR/dt, dD/dt].
    """
    S, E, I, R, D = x
    beta = parms['beta']
    sigma = parms['sigma']
    r = parms['r']
    mu = parms['mu']

    dS = -beta * S * I          # Susceptible to Exposed
    dE = beta * S * I - sigma * E  # Exposed to Infectious
    dI = sigma * E - r * I - mu * I  # Infectious to Recovered or Deceased
    dR = r * I                   # Infectious to Recovered
    dD = mu * I                  # Infectious to Deceased

    return [dS, dE, dI, dR, dD]
