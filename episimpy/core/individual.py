from enums import Status


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
