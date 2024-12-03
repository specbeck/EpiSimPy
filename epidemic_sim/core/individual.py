#from epidemic_sim.utils.enums import Status

class Individual:

    def __init__(self, age, status="susceptible"):
        """A single individual."""
        self.age = age
        self.status = status
        self.activity = self._define_activity()

    '''
    def status_change(self):
        if self.status == Status.SUSCEPTIBLE:
            self.status = Status.INFECTIOUS
        elif self.status == Status.INFECTIOUS:
            self.status = Status.RECOVERED

    '''

    def _define_activity(self):
        if self.age < 20 or self.age > 65:
            return "Less active"
        else:
            return "More active:"
