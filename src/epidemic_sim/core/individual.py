from 

class Individual:

    def __init__(self, age, status: Status, activity):
        """A single individual."""

        self.age = age
        self.status = status

    def status_change(self):
        if self.status == Status.SUSCEPTIBLE:
            self.status = Status.INFECTIOUS
        elif self.status == Status.INFECTIOUS:
            self.status = Status.RECOVERED
