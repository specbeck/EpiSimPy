from individual import Individual
from random import randint

class Population:
    def __init__(self, size, r=0.01, m=0.005):
        self.individuals = [Individual(age=random.randint(1, 90)) for _ in range(size)]
        self.growth_rate = r
        self.mortality_rate = m
        # self.density = "crowdiness" if time permits!


    def mortality(self):
        new_individuals = int(len(self.individuals) * self.growth_rate)
        self.individuals.extend([Individual(age=random.randint(1, 90)) for _ in range(new_individuals)])

    def mortality(self):
        death_count = int(len(self.individuals) * self.mortality_rate)
        self.individuals = self.individuals[:-death_count]  # Remove last few individuals

    def simulate_day(self):
        for individual in self.individuals:
            individual.status_change()
            individual.age += 1

  
