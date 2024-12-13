from individual import Individual
from random import randint
from enums import Status

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
