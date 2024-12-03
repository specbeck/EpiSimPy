import matplotlib.pyplot as plt
import plotext as plt

# Maybe make this as a class later on
def plot_epidemic_curve(susceptible, infected, recovered, time):
    """
    Plots the epidemic curve for SIR dynamics.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(time, susceptible, label="Susceptible", color="blue")
    plt.plot(time, infected, label="Infected", color="red")
    plt.plot(time, recovered, label="Recovered", color="darkgreen")
    plt.legend()
    plt.xlabel("Days")
    plt.ylabel("Population")
    plt.title("Epidemic Curve")
    plt.show()



def plot_epidemic_curve_terminal(susceptible, infected, recovered, time):
    """
    Plots the epidemic curve for SIR dynamics directly in the terminal.
    """
    # Set up the plot
    plt.clf()
    plt.title("Epidemic Curve")
    plt.xlabel("Days")
    plt.ylabel("Population")
    
    plt.plotsize(100, 30)

    # Add data to the plot
    plt.plot(time, susceptible, label="Susceptible", color="blue")
    plt.plot(time, infected, label="Infected", color="red")
    plt.plot(time, recovered, label="Recovered", color="green")
    
    #xticks = [i* 10 for i in range(1,101,20)]

    #xlabels = [i* 10 for i in range(1,101,20)]
    #plt.xticks(xticks, xlabels) 
    #plt.yfrequency(5)
    # Customize the plot
    plt.canvas_color("skyblue")
    plt.ticks_color("red")
    #    plt.legend(["Susceptible", "Infected", "Recovered"])
    plt.show()
