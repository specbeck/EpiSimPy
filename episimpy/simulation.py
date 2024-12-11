from core import Epidemic, Status
from random import uniform
import math, time
import curses

class Simulation(Epidemic):
    """Simulates an Epidemic"""

    def __init__(self, population_size, params, duration, dims, model="SIR"):
        super().__init__(population_size, params, duration, model)

        # Simulation specific parameters
        self.positions = {}
        self.velocities = {}
        self.recovery_times = {}
        self.height, self.width = dims
        self.initialize_simulator()

    def initialize_simulator(self):
        """Initializes the simulation with velocities and postitions"""
        for i, individual in enumerate(self.population.individuals):
            self.positions[individual] = (
                uniform(0, self.width - 2),
                uniform(0, self.height - 1),
            )
            self.velocities[individual] = (
                uniform(-1, 1),
                uniform(-1, 1),
            )  # Replace with group velocities later
            if individual.status == Status.INFECTIOUS:
                self.recovery_times[individual] = (
                    int(1 / self.params["gamma"]) * 6
                )

    def movement(self):
        """Handles movement of the individuals."""
        for individual in self.population.individuals:
            x, y = self.positions[individual]
            vx, vy = self.velocities[individual]

            # Add the velocities to postitions
            new_x = x + vx
            new_y = y + vy

            # Bouncing off walls/bounds of the simulation
            if new_x <= 0 or new_x >= self.width:
                vx = -vx
            if new_y <= 0 or new_y >= self.height:
                vy = -vy

            # Update based on the bounce
            self.velocities[individual] = (vx, vy)
            self.positions[individual] = (new_x, new_y)

    def spread_infection(self, infection_radius):
        """Infection spreads based on the infection radius"""
        # For the SIR model
        for person in self.population.individuals:
            if person.status == Status.INFECTIOUS:
                for neighbour in self.population.individuals:
                    if (
                        neighbour.status == Status.SUSCEPTIBLE
                        and self._distance(person, neighbour) < infection_radius
                    ):
                        neighbour.infect()
                        self.recovery_times[neighbour] = (
                            int(1 / self.params["gamma"]) * 5
                        )

        # For the SEIRD model

    def recover_individual(self):
        """Recovers individual based on their recovery time"""
        for individual, time in list(self.recovery_times.items()):
            time -= 1
            if time <= 0:
                individual.recover()
                del self.recovery_times[individual]
            else:
                self.recovery_times[individual] = time

    def _distance(self, i1, i2):
        """Calculate the distance between two individuals."""
        x1, y1 = self.positions[i1]
        x2, y2 = self.positions[i2]

        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def run(self, infection_radius):
        """Run the simulation loop"""
        self.movement()
        self.spread_infection(infection_radius)
        self.recover_individual()
        # self.display_stats()

    def display_stats(self):
        """Displays the stats for the infection"""
        s_count, i_count, r_count, _, _ = self.population.get_counts()
        return f"Susceptible: {s_count} 🟦  Infected: {i_count} 🟥  Recovered: {r_count} 🟩"


def animate(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    scrdims = stdscr.getmaxyx()
    sim = Simulation(
        population_size=100,
        params={"beta": 0.2, "gamma": 0.1},
        duration=100,
        dims=scrdims,
    )
    infection_radius = 3

    while True:
        key = stdscr.getch()
        if key == ord("q"):  # Quit when 'q' is pressed
            break
        stdscr.clear()
        sim.run(infection_radius)

        # Display individuals
        for individual, (x, y) in sim.positions.items():
            emoji = (
                "🟦"
                if individual.status == Status.SUSCEPTIBLE
                else "🟥" if individual.status == Status.INFECTIOUS else "🟩"
            )
            try:
                stdscr.addstr(int(y), int(x), emoji)
            except curses.error:
                pass

        stdscr.addstr(0, 0, sim.display_stats())
        stdscr.refresh()
        time.sleep(0.1)


if __name__ == "__main__":
    curses.wrapper(animate)
