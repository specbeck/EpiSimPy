print("In module products __package__, __name__ ==", __package__, __name__)

from ..models.sir import solve_sir

class Epidemic:
    def __init__(self, population, model="SIR", params=None):
        self.population = population
        self.model = model
        self.params = params or {}

    def run_simulation(self, days):
        if self.model == "SIR":
            return sir_model([self.population - 1, 1, 0], **self.params, days=days)
        # Add other models here
