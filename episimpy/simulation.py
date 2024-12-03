"""import curses
import time
import math
from random import uniform
from enums import Status  # Import status enums from the main file

# Billiards-inspired particle movement
class Particle:
    def __init__(self, x, y, vx, vy, state):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.state = state
        self.timer = 10 # Recovery timer for infected individuals

    def move(self, max_width, max_height):
        """Update position with wall collision logic."""
        self.x += self.vx
        self.y += self.vy

        # Bounce off walls
        if self.x <= 0 or self.x >= max_width - 1:
            self.vx = -self.vx
        if self.y <= 0 or self.y >= max_height - 1:
            self.vy = -self.vy

    def infect(self, recovery_time):
        """Change state to infected and set a recovery timer."""
        self.state = Status.INFECTIOUS
        self.timer = recovery_time

    def recover(self):
        """Change state to recovered."""
        self.state = Status.RECOVERED
        self.timer = None

def distance(p1, p2):
    """Calculate Euclidean distance between two particles."""
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def animate(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    height, width = stdscr.getmaxyx()

    # Parameters
    num_particles = 1000
    infection_radius = 1  # Spread radius for infection
    recovery_time = 50  # Recovery time in frames

    # Initialize particles with random positions and velocities
    particles = [
        Particle(
            x=uniform(0, width - 1),
            y=uniform(0, height - 1),
            vx=uniform(-1, 1),
            vy=uniform(-1, 1),
            state=Status.SUSCEPTIBLE if i > 0 else Status.INFECTIOUS
        )
        for i in range(num_particles)
    ]

    while True:
        stdscr.clear()

        # Update and draw particles
        for particle in particles:
            particle.move(width, height)

            # Infection spread
            if particle.state == Status.INFECTIOUS:
                for other in particles:
                    if other.state == Status.SUSCEPTIBLE and distance(particle, other) < infection_radius:
                        other.infect(recovery_time)

            # Recovery
            if particle.state == Status.INFECTIOUS:
                particle.timer -= 1
                if particle.timer <= 0:
                    particle.recover()

            # Draw particle
            emoji = "🟦" if particle.state == Status.SUSCEPTIBLE else "🟥" if particle.state == Status.INFECTIOUS else "🟩"
            try:
                stdscr.addstr(int(particle.y), int(particle.x), emoji)
            except curses.error:
                pass

        # Display statistics
        s_count = sum(1 for p in particles if p.state == Status.SUSCEPTIBLE)
        i_count = sum(1 for p in particles if p.state == Status.INFECTIOUS)
        r_count = sum(1 for p in particles if p.state == Status.RECOVERED)
        stats = f"Susceptible: {s_count} 🟦  Infected: {i_count} 🟥  Recovered: {r_count} 🟩"
        stdscr.addstr(0, 0, stats[:width - 1])

        stdscr.refresh()
        time.sleep(0.1)

if __name__ == "__main__":
    curses.wrapper(animate)

"""


import curses
import time
import math
from random import uniform
from core import Individual, Population, Epidemic, Status  # Import existing classes

def distance(ind1, ind2):
    """Calculate Euclidean distance between two individuals."""
    return math.sqrt((ind1.x - ind2.x) ** 2 + (ind1.y - ind2.y) ** 2)

def animate(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    height, width = stdscr.getmaxyx()

    # Initialize epidemic parameters
    num_individuals = 100
    infection_radius = 2  # Spread radius for infection
    recovery_time = 50  # Recovery time in frames

    # Create a population
    population = Population(num_individuals, width, height)

    # Assign random velocities to individuals
    for individual in population.individuals:
        individual.vx = uniform(-1, 1)
        individual.vy = uniform(-1, 1)

    # Initialize the epidemic with one infected individual
    epidemic = Epidemic(population)
    epidemic.individuals[0].state = Status.INFECTIOUS
    epidemic.infected_timers[epidemic.individuals[0]] = recovery_time

    while True:
        stdscr.clear()

        # Update population movement
        for individual in epidemic.individuals:
            # Update position with velocity
            individual.x += individual.vx
            individual.y += individual.vy

            # Bounce off walls
            if individual.x <= 0 or individual.x >= width - 1:
                individual.vx = -individual.vx
            if individual.y <= 0 or individual.y >= height - 1:
                individual.vy = -individual.vy

        # Update epidemic states
        for i, ind in enumerate(epidemic.individuals):
            if ind.state == Status.INFECTIOUS:
                # Spread infection
                for other in epidemic.individuals:
                    if other.state == Status.SUSCEPTIBLE and distance(ind, other) < infection_radius:
                        epidemic.infect(other)

                # Handle recovery
                epidemic.infected_timers[ind] -= 1
                if epidemic.infected_timers[ind] <= 0:
                    epidemic.recover(ind)

        # Draw individuals
        for ind in epidemic.individuals:
            emoji = "🟦" if ind.state == Status.SUSCEPTIBLE else "🟥" if ind.state == Status.INFECTIOUS else "🟩"
            try:
                stdscr.addstr(int(ind.y), int(ind.x), emoji)
            except curses.error:
                pass

        # Display statistics
        s_count = epidemic.susceptible_count()
        i_count = epidemic.infected_count()
        r_count = epidemic.recovered_count()
        stats = f"Susceptible: {s_count} 🟦  Infected: {i_count} 🟥  Recovered: {r_count} 🟩"
        stdscr.addstr(0, 0, stats[:width - 1])

        stdscr.refresh()
        time.sleep(0.1)

if __name__ == "__main__":
    curses.wrapper(animate)
