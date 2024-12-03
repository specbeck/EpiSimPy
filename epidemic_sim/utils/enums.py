from enum import Enum

class Status(Enum):
    SUSCEPTIBLE = "Breathing"
    INFECTIOUS = "Coughing"
    RECOVERED = "Relaxing"
    EXPOSED = "Moving"
    DEAD = "Lifeless"
