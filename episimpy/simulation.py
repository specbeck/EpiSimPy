from core import Epidemic, Status
from random import uniform
import math, time
import curses

# Inherits the Epidemic class
class Simulation(Epidemic):
    """Simulates an Epidemic"""

    def __init__(self, population_size, params, duration, dims, simtype="normal", model="SIR"):
        super().__init__(population_size, params, duration, model)

        # Simulation specific parameters
        self.positions = {}
        self.velocities = {}
        self.recovery_times = {}
        self.height, self.width = dims
        self.simtype = simtype
        self.initialize_simulator()

    def initialize_simulator(self):
        """Initializes the simulation with velocities and postitions"""
        for i, individual in enumerate(self.population.individuals): # Fill the velocities and positions dictionaries
            self.positions[individual] = (
                uniform(0, self.width - 2),
                uniform(0, self.height - 1),
            )
            factor = 10
            velocity = (
                (
                    -individual.age_group.value[0] / factor,
                    individual.age_group.value[0] / factor,
                )
                if self.simtype == "real" # If simtype is real, customize velocities based on age group
                else (-1, 1)
            )
            self.velocities[individual] = (
                uniform(*velocity),
                uniform(*velocity),
            )
            if individual.status == Status.INFECTIOUS: # Set initialally infected individual's recovery time
                self.recovery_times[individual] = int(1 / self.params["gamma"]) * 6

    def movement(self):
        """Handles movement of the individuals."""
        for individual in self.population.individuals:
            x, y = self.positions[individual]
            vx, vy = self.velocities[individual]

            # Add the velocities to postitions to simulate movement
            new_x = x + vx
            new_y = y + vy

            # Bouncing off walls/bounds of the simulation
            if new_x <= 0 or new_x >= self.width:
                vx = -vx
            if new_y <= 0 or new_y >= self.height:
                vy = -vy

            # Update wrt to the bounce
            self.velocities[individual] = (vx, vy)
            self.positions[individual] = (new_x, new_y)

    def spread_infection(self):
        """Infection spreads based on the infection radius"""
        # For the SIR model
        for person in self.population.individuals:
            if person.status == Status.INFECTIOUS:
                for neighbour in self.population.individuals: # Infect if in the infection radius
                    if (
                        neighbour.status == Status.SUSCEPTIBLE
                        and self._distance(person, neighbour)
                        < self.get_infection_radius()
                    ):
                        neighbour.infect()
                        self.recovery_times[neighbour] = (
                            int(1 / self.params["gamma"]) * 5
                        )

        # For the SEIRD model

    def recover_individual(self):
        """Recovers individual based on their recovery time"""
        for individual, time in list(self.recovery_times.items()): # Count down recovery time for the infected people
            time -= 1
            if time <= 0:
                individual.recover()
                del self.recovery_times[individual]
            else:
                self.recovery_times[individual] = time

    def get_infection_radius(self):
        """Determines infection radius based on beta, the infection rate"""
        beta = self.params["beta"]  # Infectious rate
        if beta < 0.0005:
            return 1
        elif beta < 0.001:
            return 2
        elif beta < 0.005:
            return 3
        elif beta <= 0.01:
            return 4
        else:
            return 5

    def _distance(self, i1, i2):
        """Calculate the distance between two individuals."""
        x1, y1 = self.positions[i1]
        x2, y2 = self.positions[i2]

        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def run(self):
        """Run the simulation loop"""
        self.movement()
        self.spread_infection()
        self.recover_individual()
        # self.display_stats()

    def display_stats(self):
        """Displays the stats for the infection"""
        s_count, i_count, r_count, _, _ = self.population.get_counts()

        return (
            f"Susceptible: {s_count} 😊 Infected: {i_count} 🤢  Recovered: {r_count} 😷"
            if self.simtype == "real"
            else f"Susceptible: {s_count} 🟦  Infected: {i_count} 🟥  Recovered: {r_count} 🟩"
        )


def animate(stdscr, size, params, duration, simtype):
    """The main animation function that handles dynamic arguments given by the user"""

    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    scrdims = stdscr.getmaxyx()  # Get screen dimensions
    sim = Simulation(
        population_size=size,
        params=params,
        duration=duration,
        dims=scrdims,
        simtype=simtype,
    )

    while True:
        key = stdscr.getch()
        if key == ord("q"):  # Quit when 'q' is pressed
            break
        stdscr.clear()
        sim.run()

        # Display individuals
        for individual, (x, y) in sim.positions.items():
            emoji = (
                (
                    individual.age_group.value[1]
                    if individual.status == Status.SUSCEPTIBLE
                    else "🤢" if individual.status == Status.INFECTIOUS else "😷"
                )
                if simtype == "real"
                else (
                    "🟦"
                    if individual.status == Status.SUSCEPTIBLE
                    else "🟥" if individual.status == Status.INFECTIOUS else "🟩"
                )
            )
            try:
                stdscr.addstr(int(y), int(x), emoji)
            except curses.error:
                pass

        stdscr.addstr(0, 0, sim.display_stats())
        stdscr.refresh()
        time.sleep(0.1)


def run(n=100, p={"beta": 0.02, "gamma": 0.1}, t=100, simtype="normal"):
    """Runs the actual simulation with user defined parameters"""
    curses.wrapper(
        lambda stdscr: animate(stdscr, size=n, params=p, duration=t, simtype=simtype)
    )


if __name__ == "__main__":
    run(n=int(input("Enter individuals: ")), simtype=input("Enter simtype: "))
