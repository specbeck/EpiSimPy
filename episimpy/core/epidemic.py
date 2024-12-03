from population import Population
import numpy as np
from models import SIR
from visualisations import plot_epidemic_curve

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
        plot_epidemic_curve(S, I, R, time_points)
