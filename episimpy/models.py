from scipy.integrate import solve_ivp  # To solve differential equations


class SIR:
    @staticmethod
    def sir_model(t, x, params):
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
    def solve_sir(inits, params, time_steps):
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
        r = params["gamma"]
        mu = params["delta"]

        dS = -beta * S * I  # Susceptible to Exposed
        dE = beta * S * I - sigma * E  # Exposed to Infectious
        dI = sigma * E - r * I - mu * I  # Infectious to Recovered or Deceased
        dR = r * I  # Infectious to Recovered
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
