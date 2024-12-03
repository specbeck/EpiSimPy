import matplotlib.pyplot as plt

def plot_epidemic_curve(susceptible, infected, recovered, time):
    plt.figure(figsize=(10, 6))
    plt.plot(time, susceptible, label="Susceptible", color="blue")
    plt.plot(time, infected, label="Infected", color="red")
    plt.plot(time, recovered, label="Recovered", color="darkgreen")
    plt.legend()
    plt.xlabel("Days")
    plt.ylabel("Population")
    plt.title("Epidemic Curve")
    plt.show()


def plot_seird_curve(S, E, I, R, D, time_points):
    plt.figure(figsize=(10, 6))
    plt.plot(time_points, S, label="S (Susceptible)", color="blue", linewidth=2)
    plt.plot(time_points, E, label="E (Exposed)", color="orange", linewidth=2)
    plt.plot(time_points, I, label="I (Infected)", color="red", linewidth=2)
    plt.plot(time_points, R, label="R (Recovered)", color="darkgreen", linewidth=2)
    plt.plot(time_points, D, label="D (Deceased)", color="black", linewidth=2)

    plt.title("SEIRD Model Simulation")
    plt.xlabel("Time")
    plt.ylabel("Number of Individuals")
    plt.legend()
    plt.show()
