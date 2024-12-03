'''

import curses
import time
import numpy as np
from random import randint

# SIR model function
def SIR(t, x, parms):
    S, I, R = x
    beta = parms['beta']
    r = parms['r']
    dS = -beta * S * I
    dI = beta * S * I - r * I
    dR = r * I
    return [dS, dI, dR]

# Simulation parameters
parms = {'beta': 1e-3, 'r': 1e-1}  # Infection rate and recovery rate
inits = [499, 1, 0]  # Initial counts: S, I, R
time_points = np.arange(0, 100.1, 1)  # Time steps
result = np.zeros((len(time_points), 3))  # To store S, I, R counts

# Solve the SIR model using Euler's method
S, I, R = inits
for t_idx, t in enumerate(time_points):
    result[t_idx] = [S, I, R]
    dS, dI, dR = SIR(t, [S, I, R], parms)
    S += dS
    I += dI
    R += dR

# Visualization with curses
def animate(stdscr):
    curses.curs_set(0)  # Hide cursor
    height, width = stdscr.getmaxyx()
    num_individuals = 500
    individuals = []

    # Initialize individuals with random positions and states
    for _ in range(num_individuals):
        x, y = randint(0, width - 1), randint(0, height - 1)
        state = "S"  # Initially all are Susceptible
        individuals.append({"x": x, "y": y, "state": state})

    time_step = 0
    while time_step < len(time_points):
        stdscr.clear()
        # Update states based on SIR model
        S_count, I_count, R_count = result[time_step]
        total = int(S_count + I_count + R_count)
        infected_indices = np.random.choice(len(individuals), int(I_count), replace=False)
        recovered_indices = np.random.choice(len(individuals), int(R_count), replace=False)
        
        for idx, individual in enumerate(individuals):
            if idx in infected_indices:
                individual["state"] = "I"
            elif idx in recovered_indices:
                individual["state"] = "R"
            else:
                individual["state"] = "S"

            # Random movement
            individual["x"] = (individual["x"] + randint(-1, 1)) % width
            individual["y"] = (individual["y"] + randint(-1, 1)) % height

            # Display emoji based on state
            if individual["state"] == "S":
                stdscr.addstr(individual["y"], individual["x"], "🟦")
            elif individual["state"] == "I":
                stdscr.addstr(individual["y"], individual["x"], "🟥")
            elif individual["state"] == "R":
                stdscr.addstr(individual["y"], individual["x"], "🟩")

        # Display statistics
        stdscr.addstr(0, 0, f"Time: {time_points[time_step]:.1f}")
        stdscr.addstr(1, 0, f"Susceptible: {int(S_count)} 🟦")
        stdscr.addstr(2, 0, f"Infected: {int(I_count)} 🟥")
        stdscr.addstr(3, 0, f"Recovered: {int(R_count)} 🟩")

        stdscr.refresh()
        time.sleep(0.2)
        time_step += 1

curses.wrapper(animate)
'''


import curses
import time
from random import randint

# Visualization with curses
def animate(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    height, width = stdscr.getmaxyx()

    num_individuals = 100
    states = ["S"] * 95 + ["I"] * 5  # Initially 99 susceptible, 1 infected
    individuals = [{"x": randint(0, width - 2), "y": randint(0, height - 2), "state": state} for state in states]

    recovery_time = 20  # Time steps after which infected recover
    infected_timers = {i: recovery_time for i, ind in enumerate(individuals) if ind["state"] == "I"}

    while True:
        stdscr.clear()

        # Update individuals
        for i, ind in enumerate(individuals):
            # Random movement within bounds
            ind["x"] = (ind["x"] + randint(-1, 1)) % (width - 1)
            ind["y"] = (ind["y"] + randint(-1, 1)) % (height - 1)

            # Handle infection spread
            if ind["state"] == "S":
                for other in individuals:
                    if other["state"] == "I" and ind["x"] == other["x"] and ind["y"] == other["y"]:
                        ind["state"] = "I"
                        infected_timers[i] = recovery_time
                        break

            # Handle recovery
            if ind["state"] == "I":
                infected_timers[i] -= 1
                if infected_timers[i] <= 0:
                    ind["state"] = "R"

            # Display individual
            try:
                emoji = "🟦" if ind["state"] == "S" else "🟥" if ind["state"] == "I" else "🟩"
                stdscr.addstr(ind["y"], ind["x"], emoji)
            except curses.error:
                # Ignore errors caused by boundary issues
                pass

        # Display statistics
        s_count = sum(1 for ind in individuals if ind["state"] == "S")
        i_count = sum(1 for ind in individuals if ind["state"] == "I")
        r_count = sum(1 for ind in individuals if ind["state"] == "R")
        stats = f"Susceptible: {s_count} 🟦  Infected: {i_count} 🟥  Recovered: {r_count} 🟩"
        stdscr.addstr(0, 0, stats[:width - 1])  # Ensure stats fit within screen width

        stdscr.refresh()
        time.sleep(0.2)

curses.wrapper(animate)
