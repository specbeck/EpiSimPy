from scipy.integrate import solve_ivp


class SIR:
    @staticmethod
    def sir_model(t, x, beta, gamma):
        """
        Differential equations for the SIR model.
        """
        S, I, R = x
        dS = -beta * S * I
        dI = beta * S * I - gamma * I
        dR = gamma * I
        return [dS, dI, dR]

    @staticmethod
    def solve_sir(inits, beta, gamma, time_points):
        """
        Solves the SIR differential equations.
        """
        # Solve the equations using scipy's solve_ivp
        result = solve_ivp(
            fun=lambda t, y: SIR.sir_model(t, y, beta, gamma),
            t_span=(time_points[0], time_points[-1]),
            y0=inits,
            t_eval=time_points
        )

        S, I, R = result.y
        return S, I, R



class SEIRD:
    ...
