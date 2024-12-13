from scipy.integrate import solve_ivp  # To solve differential equations


class SIR:
    """
    The SIR Model.
    S: Susceptible individuals prone to the infection
    I: Infected individuals capable of spreading infection
    R: Recoverd/Removed individuals do not turn susceptible

    """

    @staticmethod
    def sir_model(
        t: list[float], x: list[int], params: dict[str, float]
    ) -> list[float]:
        """
        Differential equations encompassing the SIR model.
        """
        S, I, R = x
        beta = params["beta"]
        gamma = params["gamma"]

        dS = -beta * S * I  # Susceptible to infected
        dI = beta * S * I - gamma * I  # Infected to Recovered/Removed
        dR = gamma * I  # Infected to Recovered

        return [dS, dI, dR]

    @staticmethod
    def solve_sir(inits: list[int], params: dict[str, float], time_steps: list[float]):
        """
        Solves the SIR differential equations.
        """
        result = solve_ivp(
            fun=lambda t, y: SIR.sir_model(t, y, params),
            t_span=(time_steps[0], time_steps[-1]),
            y0=inits,
            t_eval=time_steps,
        )
        S, I, R = result.y
        return S, I, R, result.t


class SEIRD:
    @staticmethod
    def seird_model(t, x, params):
        """
        Differential equations for the SEIRD model.
        """
        S, E, I, R, D = x
        beta = params["beta"]
        sigma = params["sigma"]
        gamma = params["gamma"]
        mu = params["mu"]

        dS = -beta * S * I  # Susceptible to Exposed
        dE = beta * S * I - sigma * E  # Exposed to Infectious
        dI = sigma * E - gamma * I - mu * I  # Infectious to Recovered or Deceased
        dR = gamma * I  # Infectious to Recovered
        dD = mu * I  # Infectious to Deceased
        return [dS, dE, dI, dR, dD]

    @staticmethod
    def solve_seird(inits, params, time_steps):
        """
        Solves the SEIRD differential equations.
        """
        # Solve the equations using scipy's solve_ivp
        result = solve_ivp(
            fun=lambda t, y: SEIRD.seird_model(t, y, params),
            t_span=(time_steps[0], time_steps[-1]),
            y0=inits,
            t_eval=time_steps,
        )

        S, E, I, R, D = result.y
        return S, E, I, R, D, result.t
