import matplotlib.pyplot as plt
import numpy as np

class Plot:
    @staticmethod
    def window(values, model, time_steps, delay=0.1, step=1):
        """
        Dynamically plots the epidemic curve over time on a separate window.
        Optimized for dense time points and supports smooth animations.
        
        Parameters:
        - values: List of arrays for population groups (e.g., [S, I, R])
        - model: Model type ("SIR" or "SEIRD")
        - time_steps: Array of time points
        - delay: Pause duration between updates (default 0.01)
        - step: Step size for time points to skip frames and speed up animation
        """
        plt.figure(figsize=(10, 6))
        plt.ion()  # Turn on interactive mode

        for t in range(0, len(time_steps), step):  # Use step to skip frames for speed
            plt.clf()  # Clear the figure for each frame

            if model == "SIR":
                susceptible, infected, recovered = values
                plt.plot(time_steps[:t+1], susceptible[:t+1], label="Susceptible", color="blue")
                plt.plot(time_steps[:t+1], infected[:t+1], label="Infected", color="red")
                plt.plot(time_steps[:t+1], recovered[:t+1], label="Recovered", color="darkgreen")

            elif model == "SEIRD":
                susceptible, exposed, infected, recovered, dead = values
                plt.plot(time_steps[:t+1], susceptible[:t+1], label="Susceptible", color="blue")
                plt.plot(time_steps[:t+1], exposed[:t+1], label="Exposed", color="orange")
                plt.plot(time_steps[:t+1], infected[:t+1], label="Infected", color="red")
                plt.plot(time_steps[:t+1], recovered[:t+1], label="Recovered", color="darkgreen")
                plt.plot(time_steps[:t+1], dead[:t+1], label="Dead", color="black")

            plt.legend()
            plt.xlabel("Time (Days)")
            plt.ylabel("Population")
            plt.title("Epidemic Curve")
            plt.pause(delay)  # Pause to simulate animation

        plt.ioff()  # Turn off interactive mode
        plt.show()  # Display the final plot



from scipy.integrate import solve_ivp
import numpy as np

# Define SIR model differential equations
def sir_model(t, y, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

# Parameters
beta = 0.001
gamma = 0.1
S0, I0, R0 = 499, 1, 0  # Initial conditions
t_span = (0, 100)  # Time range
t_eval = np.arange(0, 100.1, 0.1)  # Dense time points

# Solve the differential equations
sol = solve_ivp(sir_model, t_span, [S0, I0, R0], args=(beta, gamma), t_eval=t_eval)

# Extract the results
time_steps = sol.t
susceptible, infected, recovered = sol.y

# Use the Plot.window function with frame skipping
Plot.window([susceptible, infected, recovered], "SIR", time_steps, delay=0.1, step=5)
