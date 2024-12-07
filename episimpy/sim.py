import curses # Adds strings to the terminal dynamically!!
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

    def move(self, max_width, max_height): # Nice logic!
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
    # Parameters
    num_particles = 100# int(input("Enter the number of individuals to simualte: "))
    infection_radius = 3# int(input("Enter infection spread radius: "))  # Spread radius for infection
    recovery_time = 60 # int(input("How fast will infected recover? "))  # Recovery time in frames

    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    height, width = stdscr.getmaxyx()

    # Initialize particles with random positions and velocities (Doesn't display yet)
    particles = [ # Could use the velocities coded in the enum when inheriting
        Particle(
            x=uniform(0, width - 1),
            y=uniform(0, height - 1),
            vx=uniform(-0.5, 0.5),
            vy=uniform(-0.5, 0.5),
            state=Status.SUSCEPTIBLE if i > 0 else Status.INFECTIOUS # This is taken care of in Epidemic class
        )
        for i in range(num_particles)
    ]

    while True: # Game loop basically
        stdscr.clear()
        # Introduce clock for duration of spread!
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
                particle.timer -= 1 # Varied recovery time!
                if particle.timer <= 0:
                    particle.recover()

            # Draw particle
            emoji = "🟦" if particle.state == Status.SUSCEPTIBLE else "🟥" if particle.state == Status.INFECTIOUS else "🟩"
            try:
                stdscr.addstr(int(particle.y), int(particle.x), emoji)
            except curses.error:
                pass
            #raise Exception("Something happened while rendering the icons.")

        # Display statistics could be used from epidemic class
        s_count = sum(1 for p in particles if p.state == Status.SUSCEPTIBLE)
        i_count = sum(1 for p in particles if p.state == Status.INFECTIOUS)
        r_count = sum(1 for p in particles if p.state == Status.RECOVERED)
        stats = f"Susceptible: {s_count} 🟦  Infected: {i_count} 🟥  Recovered: {r_count} 🟩"
        stdscr.addstr(0, 0, stats[:width - 1])
        # Adds the str to the top updating every second
        stdscr.refresh()
        time.sleep(0.09)

if __name__ == "__main__":
    curses.wrapper(animate)

