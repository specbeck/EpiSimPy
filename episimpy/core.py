from enum import Enum
from random import randint
import numpy as np
from models import SIR, SEIRD
from visualisations import Plot

# Custom enums for classes
class Status(Enum):
    """
    Defines custom statuses of individuals wrt the pandemic
    """
    SUSCEPTIBLE = "blue"
    EXPOSED = "yellow"
    INFECTIOUS = "red"
    RECOVERED = "darkgreen"
    DEAD = "black"


class Groups(Enum):
    """
    Defines age groups for population segregation, with values representing mobility
    """
    INFANTS = 0
    TEENS = 10
    ADULTS = 15
    MIDDLE = 20
    OLD = 5
    

class Individual:
    """A single individual."""
    def __init__(self, age, status=Status.SUSCEPTIBLE): # Initially every individual is susceptible
        self.age = age
        self.age_group = self.age_group()
        self.status = status

    def expose(self):
        """Individual is exposed."""
        self.status = Status.EXPOSED

    def infect(self):
        """Individual gets infected."""
        self.status = Status.INFECTIOUS

    def recover(self):
        """Individual recovers from the infection."""
        self.status = Status.RECOVERED
    
    def die(self):
        """Individual dies."""
        self.status = Status.DEAD

    # Helper functions
    def age_group(self):
        """Segregates individuals into age groups based on their age."""
        if self.age > 64:
            return Groups.OLD
        elif self.age > 24:
            return Groups.MIDDLE
        elif self.age > 14:
            return Groups.ADULTS
        elif self.age > 5:
            return Groups.TEENS
        else:
            return Groups.INFANTS



class Population:
    """A collection of individuals."""
    def __init__(self, size):
        self.size = size
        self.individuals = self.segregate_population()
    
    def segregate_population(self):
        """
        Segregates population based on the different age groups
        Assumes the average approximate population segregation percentages as follows:
        INFANTS: 7.5% ~ 8%, TEENS: 19%, ADULTS: 17.5% ~ 18%, MIDDLE-AGED: 45%, OLD-AGED: 11%
        """
        percent_to_counts = (int((p / 100) * self.size) for p in [7.5, 19, 17.5, 45, 11])
        limits = ([1, 5], [6, 14], [15, 24], [25, 65], [66, 90])

        population = []
        
        for count, limit in zip(percent_to_counts, limits):
            group = [ Individual(randint(*limit)) for _ in range(count) ]
            population.extend(group)
        
        return population
    

    def get_counts(self):
        """Get the count of individuals in each state at any point."""
        s_count = sum(1 for i in self.individuals if i.status == Status.SUSCEPTIBLE)
        i_count = sum(1 for i in self.individuals if i.status == Status.INFECTIOUS)
        r_count = sum(1 for i in self.individuals if i.status == Status.RECOVERED)
        e_count = sum(1 for i in self.individuals if i.status == Status.EXPOSED)
        d_count = sum(1 for i in self.individuals if i.status == Status.DEAD)


        return s_count, i_count, r_count, e_count, d_count



class Epidemic:
    """
    Simulates an epidemic.
    """
    def __init__(self, population_size, params, duration, model="SIR"):
        self.population = Population(population_size)
        self.params = params
        self.duration = duration
        self.simulation_set = None
        self.model = model 
        # Initially, one individual is infectious
        self.population.individuals[randint(0, self.population.size)].infect()
    

    def run(self):
        """
        Run the epidemic simulation.
        """

        s_count, i_count, r_count, e_count, d_count = self.population.get_counts()
        inits = [s_count, i_count, r_count]
        
        if self.model == "SEIRD":
            inits = [s_count, e_count, i_count, r_count, d_count]

        # Take varying time points
        time_points = np.arange(0, self.duration + 0.1, 0.1)

        # Solve the SIR model
        if self.model == "SIR":
            S, I, R, time_steps = SIR.solve_sir(inits, self.params, time_points)
            # Plot the epidemic curve
            Plot.window([S, I, R], self.model, time_steps)
            Plot.terminal([S, I, R], self.model, time_steps)
        elif self.model == "SEIRD":
            S, E, I, R, D, time_steps = SEIRD.solve_seird(inits, self.params, time_points)
            
            Plot.window([S, E, I, R, D], self.model, time_steps)
            Plot.terminal([S, E, I, R, D], self.model, time_steps)
            
        self.simulation_set = zip(time_steps, S, I, R)

