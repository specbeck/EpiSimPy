"""
from enum import Enum
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from random import randint

# Enums: Status for individuals
class Status(Enum):
    SUSCEPTIBLE = "blue"
    INFECTIOUS = "red"
    RECOVERED = "darkgreen"

# Individual Class
class Individual:
    def __init__(self, x, y, status=Status.SUSCEPTIBLE):
        self.x = x
        self.y = y
        self.status = status

    def infect(self):
        self.status = Status.INFECTIOUS

    def recover(self):
        self.status = Status.RECOVERED

# Population Class
class Population:
    def __init__(self, size):
        self.size = size
        self.individuals = [
            Individual(randint(0, 100), randint(0, 100)) for _ in range(size)
        ]
        self.individuals[0].infect()  # Initially, one individual is infectious

    def get_counts(self):
        s_count = sum(1 for ind in self.individuals if ind.status == Status.SUSCEPTIBLE)
        i_count = sum(1 for ind in self.individuals if ind.status == Status.INFECTIOUS)
        r_count = sum(1 for ind in self.individuals if ind.status == Status.RECOVERED)
        return s_count, i_count, r_count

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
def animate_epidemic(S, I, R, time_points):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, time_points[-1])
    ax.set_ylim(0, max(max(S), max(I), max(R)) * 1.1)

    # Create empty lines for S, I, R
    line_s, = ax.plot([], [], label="Susceptible", color="blue")
    line_i, = ax.plot([], [], label="Infected", color="red")
    line_r, = ax.plot([], [], label="Recovered", color="darkgreen")

    ax.set_title("Epidemic Simulation Over Time")
    ax.set_xlabel("Days")
    ax.set_ylabel("Population")
    ax.legend()

    def update(frame):
        # Update the lines with data up to the current frame
        line_s.set_data(time_points[:frame], S[:frame])
        line_i.set_data(time_points[:frame], I[:frame])
        line_r.set_data(time_points[:frame], R[:frame])
        return line_s, line_i, line_r

    # Create the animation
    ani = FuncAnimation(fig, update, frames=len(time_points), interval=50, blit=True)
    plt.show()

# Main Epidemic Simulation Class
class Epidemic:
    def __init__(self, population_size, beta, gamma, duration):
        self.population = Population(population_size)
        self.beta = beta
        self.gamma = gamma
        self.duration = duration

    def run(self):
        s_count, i_count, r_count = self.population.get_counts()
        inits = [s_count, i_count, r_count]
        time_points = np.arange(0, self.duration + 0.1, 0.1)

        # Solve the SIR model
        S, I, R = solve_sir(inits, self.beta, self.gamma, time_points)

        # Animate the epidemic curve
        animate_epidemic(S, I, R, time_points)

# Run the Simulation
if __name__ == "__main__":
    POPULATION_SIZE = 500
    BETA = 1e-3
    GAMMA = 0.1
    DURATION = 100

    epidemic = Epidemic(population_size=POPULATION_SIZE, beta=BETA, gamma=GAMMA, duration=DURATION)
    epidemic.run() """

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
def animate_epidemic_with_r0(inits, time_points, beta_values, gamma_values):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, time_points[-1])
    ax.set_ylim(0, max(inits) * 1.1)

    # Create empty lines for S, I, R
    line_s, = ax.plot([], [], label="Susceptible", color="blue")
    line_i, = ax.plot([], [], label="Infected", color="red")
    line_r, = ax.plot([], [], label="Recovered", color="darkgreen")
    text_r0 = ax.text(0.02, 0.95, "", transform=ax.transAxes, fontsize=12, verticalalignment="top")

    ax.set_title("Epidemic Simulation with Varying $R_0$")
    ax.set_xlabel("Days")
    ax.set_ylabel("Population")
    ax.legend()

    def update(frame):
        beta = beta_values[frame]
        gamma = gamma_values[frame]
        R_0 = beta * sum(inits) / gamma

        # Solve the SIR model for current beta, gamma
        S, I, R = solve_sir(inits, beta, gamma, time_points)

        # Update the lines and text
        line_s.set_data(time_points, S)
        line_i.set_data(time_points, I)
        line_r.set_data(time_points, R)
        text_r0.set_text(f"$R_0$: {R_0:.2f} (β={beta:.3f}, γ={gamma:.3f})")
        return line_s, line_i, line_r, text_r0

    # Create the animation
    ani = FuncAnimation(fig, update, frames=len(beta_values), interval=1000, blit=True)
    plt.show()

# Main Epidemic Simulation Class
class EpidemicWithR0:
    def __init__(self, population_size, beta_values, gamma_values, duration):
        self.inits = [population_size - 1, 1, 0]  # S, I, R
        self.beta_values = beta_values
        self.gamma_values = gamma_values
        self.duration = duration
        self.time_points = np.arange(0, self.duration + 0.1, 0.1)

    def run(self):
        animate_epidemic_with_r0(self.inits, self.time_points, self.beta_values, self.gamma_values)

# Run the Simulation
if __name__ == "__main__":
    POPULATION_SIZE = 500
    DURATION = 100

    # Define beta and gamma values for varying R_0
    beta_values = np.linspace(1e-4, 3e-3, 30)  # Infection rate (varied)
    gamma_values = np.linspace(0.05, 0.2, 30)  # Recovery rate (varied)

    # Create and run the epidemic simulation
    epidemic = EpidemicWithR0(
        population_size=POPULATION_SIZE,
        beta_values=beta_values,
        gamma_values=gamma_values,
        duration=DURATION
    )
    epidemic.run()
