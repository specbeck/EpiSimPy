from enum import Enum
from random import randint
import numpy as np
from models import SIR
from visualisations import plot_epidemic_curve_terminal


# Custom enums for classes
class Status(Enum):
    SUSCEPTIBLE = "blue"
    INFECTIOUS = "red"
    RECOVERED = "darkgreen"

class Individual:
    """A single individual."""
    def __init__(self, x, y, status=Status.SUSCEPTIBLE):
        self.x = x
        self.y = y
        self.status = status

    def infect(self):
        """Changes the status of the individual to infected."""
        self.status = Status.INFECTIOUS

    def recover(self):
        """Changes the status of the individual to recovered."""
        self.status = Status.RECOVERED

class Population:
    """A collection of individuals."""
    def __init__(self, size):
        self.size = size
        self.individuals = [
            Individual(randint(0, 100), randint(0, 100)) for _ in range(size)
        ]
        # Initially, one individual is infectious
        self.individuals[0].infect()

    def get_counts(self):
        """Get the count of individuals in each state."""
        s_count = sum(1 for i in self.individuals if i.status == Status.SUSCEPTIBLE)
        i_count = sum(1 for i in self.individuals if i.status == Status.INFECTIOUS)
        r_count = sum(1 for i in self.individuals if i.status == Status.RECOVERED)
        return s_count, i_count, r_count

class Epidemic:
    """
    Simulates an epidemic using the SIR model.
    """
    def __init__(self, population_size, beta, gamma, duration):
        self.population = Population(population_size)
        self.beta = beta
        self.gamma = gamma
        self.duration = duration

    def run(self):
        """
        Run the epidemic simulation.
        """
        # Initial counts for S, I, R
        s_count, i_count, r_count = self.population.get_counts()
        inits = [s_count, i_count, r_count]
        time_points = np.arange(0, self.duration + 0.1, 0.1)

        # Solve the SIR model
        S, I, R = SIR.solve_sir(inits, self.beta, self.gamma, time_points)

        # Plot the epidemic curve
        plot_epidemic_curve_terminal(S, I, R, time_points)
