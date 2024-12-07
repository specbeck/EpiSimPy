import matplotlib.pyplot as mplt
import numpy as np

class Plot:
    @staticmethod
    def window(values, model, time_steps, delay=0.01, step=1):
        """
        Dynamically plots the epidemic curve over time on a separate window.
        Optimized for dense time points and supports smooth animations.
        
        Parameters:
        - values: List of arrays for population groups (e.g., [S, E, I, R, D] for SEIRD)
        - model: Model type ("SIR" or "SEIRD")
        - time_steps: Array of time points
        - delay: Pause duration between updates (default 0.01)
        - step: Step size for time points to skip frames and speed up animation
        """
        mplt.figure(figsize=(10, 6))
        mplt.ion()  # Turn on interactive mode

        for t in range(0, len(time_steps), step):  # Use step to skip frames for speed
            mplt.clf()  # Clear the figure for each frame

            if model == "SIR":
                susceptible, infected, recovered = values
                mplt.plot(time_steps[:t+1], susceptible[:t+1], label="Susceptible", color="blue")
                mplt.plot(time_steps[:t+1], infected[:t+1], label="Infected", color="red")
                mplt.plot(time_steps[:t+1], recovered[:t+1], label="Recovered", color="darkgreen")

            elif model == "SEIRD":
                susceptible, exposed, infected, recovered, dead = values
                mplt.plot(time_steps[:t+1], susceptible[:t+1], label="Susceptible", color="blue")
                mplt.plot(time_steps[:t+1], exposed[:t+1], label="Exposed", color="orange")
                mplt.plot(time_steps[:t+1], infected[:t+1], label="Infected", color="red")
                mplt.plot(time_steps[:t+1], recovered[:t+1], label="Recovered", color="darkgreen")
                mplt.plot(time_steps[:t+1], dead[:t+1], label="Dead", color="black")

            mplt.legend()
            mplt.xlabel("Time (Days)")
            mplt.ylabel("Population")
            mplt.title("Epidemic Curve")
            mplt.pause(delay)  # Pause to simulate animation

        mplt.ioff()  # Turn off interactive mode
        mplt.show()  # Display the final plot




from scipy.integrate import solve_ivp

def seird_model(t, y, beta, sigma, gamma, mu):
    """
    SEIRD model differential equations.
    
    Parameters:
    - beta: Transmission rate
    - sigma: Incubation rate (1/latent period)
    - gamma: Recovery rate
    - mu: Mortality rate
    """
    S, E, I, R, D = y
    dSdt = -beta * S * I
    dEdt = beta * S * I - sigma * E
    dIdt = sigma * E - (gamma + mu) * I
    dRdt = gamma * I
    dDdt = mu * I
    return [dSdt, dEdt, dIdt, dRdt, dDdt]

# Parameters
beta = 0.01  # Transmission rate
sigma = 0.2  # Incubation rate
gamma = 0.1  # Recovery rate
mu = 0.01   # Mortality rate

# Initial conditions
S0, E0, I0, R0, D0 = 500, 1, 0, 0, 0
t_span = (0, 100)  # Time range
t_eval = np.arange(0, 100.1, 0.1)  # Dense time points

# Solve the differential equations
sol = solve_ivp(seird_model, t_span, [S0, E0, I0, R0, D0], args=(beta, sigma, gamma, mu), t_eval=t_eval)

# Extract results
time_steps = sol.t
susceptible, exposed, infected, recovered, dead = sol.y
    
# Use the updated Plot.window function
Plot.window([susceptible, exposed, infected, recovered, dead], "SEIRD", time_steps, delay=0.01, step=5)
