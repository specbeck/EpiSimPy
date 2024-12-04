import curses
import time
import math
from random import uniform
from core import Status  # Import status enums from the main file

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
    num_particles = 100
    infection_radius = 3  # Spread radius for infection
    recovery_time = 100  # Recovery time in frames

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

