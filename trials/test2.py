from enum import Enum
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Enums: Status for individuals
class Status(Enum):
    SUSCEPTIBLE = "blue"
    INFECTIOUS = "red"
    RECOVERED = "darkgreen"

# SIR Model Functions
def sir_model(t, x, beta, gamma):
    S, I, R = x
    dS = -beta * S * I
    dI = beta * S * I - gamma * I
    dR = gamma * I
    return [dS, dI, dR]

def solve_sir(inits, beta, gamma, time_points):
    result = solve_ivp(
        fun=lambda t, y: sir_model(t, y, beta, gamma),
        t_span=(time_points[0], time_points[-1]),
        y0=inits,
        t_eval=time_points
    )
    return result.y  # Returns S, I, R arrays

# Animation Function
def animate_epidemic_with_dot(inits, time_points, beta_values, gamma_values):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, time_points[-1])
    ax.set_ylim(0, max(inits) * 1.1)

    # Create lines for S, I, R
    line_s, = ax.plot([], [], label="Susceptible", color="blue")
    line_i, = ax.plot([], [], label="Infected", color="red")
    line_r, = ax.plot([], [], label="Recovered", color="darkgreen")

    # Create a dot to track the values
    dot_s, = ax.plot([], [], 'bo')  # Blue dot for Susceptible
    dot_i, = ax.plot([], [], 'ro')  # Red dot for Infected
    dot_r, = ax.plot([], [], 'go')  # Green dot for Recovered

    ax.set_title("Epidemic Simulation with Moving Dot")
    ax.set_xlabel("Days")
    ax.set_ylabel("Population")
    ax.legend()

    # Update function for animation
    def update(frame):
        beta = beta_values[frame]
        gamma = gamma_values[frame]
        R_0 = beta * sum(inits) / gamma

        # Solve the SIR model for current beta, gamma
        S, I, R = solve_sir(inits, beta, gamma, time_points)

        # Update the lines (curves)
        line_s.set_data(time_points, S)
        line_i.set_data(time_points, I)
        line_r.set_data(time_points, R)

        # Calculate current time step for the dot (moving marker)
        current_time = time_points[frame]
        current_s = S[frame]
        current_i = I[frame]
        current_r = R[frame]

        # Update the dots to track the current values of S, I, R
        dot_s.set_data(current_time, current_s)
        dot_i.set_data(current_time, current_i)
        dot_r.set_data(current_time, current_r)

        return line_s, line_i, line_r, dot_s, dot_i, dot_r

    # Create the animation
    ani = FuncAnimation(fig, update, frames=len(beta_values), interval=200, blit=True)
    plt.show()

# Main Epidemic Simulation Class
class EpidemicWithMovingDot:
    def __init__(self, population_size, beta_values, gamma_values, duration):
        self.inits = [population_size - 1, 1, 0]  # S, I, R
        self.beta_values = beta_values
        self.gamma_values = gamma_values
        self.duration = duration
        self.time_points = np.arange(0, self.duration + 0.1, 0.1)

    def run(self):
        animate_epidemic_with_dot(self.inits, self.time_points, self.beta_values, self.gamma_values)

# Run the Simulation
if __name__ == "__main__":
    POPULATION_SIZE = 500
    DURATION = 100

    # Define beta and gamma values for varying R_0
    beta_values = np.linspace(1e-4, 3e-3, 30)  # Infection rate (varied)
    gamma_values = np.linspace(0.05, 0.2, 30)  # Recovery rate (varied)

    # Create and run the epidemic simulation
    epidemic = EpidemicWithMovingDot(
        population_size=POPULATION_SIZE,
        beta_values=beta_values,
        gamma_values=gamma_values,
        duration=DURATION
    )
    epidemic.run()
