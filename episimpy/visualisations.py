import matplotlib.pyplot as plt
import plotext as plx
import time


class Plot:
    @staticmethod
    def window(values, model, time, delay=0.1, step=1):
        """
        Plot the epidemic curve namely the values of individuals over time on a seperate window
        """

        plt.figure(figsize=(10, 6))
        plt.ion()  # Interactive mode

        for t in range(0, len(time), step):
            plt.clf()  # Clear previous figure

            dt = time[: t + 1]

            if model == "SIR":
                susceptible, infected, recovered = values
            elif model == "SEIRD":
                susceptible, exposed, infected, recovered, dead = values
                plt.plot(dt, exposed[: t + 1], label="Exposed", color="orange")
                plt.plot(dt, dead[: t + 1], label="Dead", color="black")

            plt.plot(dt, susceptible[: t + 1], label="Susceptible", color="blue")
            plt.plot(dt, infected[: t + 1], label="Infected", color="red")
            plt.plot(dt, recovered[: t + 1], label="Recovered", color="darkgreen")

            plt.legend()
            plt.xlabel("Time (Days)")
            plt.ylabel("Population")
            plt.title("Epidemic Curve")
            plt.pause(delay)  # Pause with delay to simulate

        plt.ioff()
        plt.show()

    def terminal(values, model, time):
        """
        Plots the epidemic curve directly in the terminal with enhanced formatting.
        """
        # Clear the terminal plot
        plx.clf()

        # Dynamically set the plot size based on terminal size
        term_width, term_height = plx.terminal_size()
        plx.plotsize(term_width - 30, term_height - 15)

        # Set the title, labels, and styles
        plx.title("Epidemic Curve")
        plx.xlabel("Days")
        plx.ylabel("Population")
        plx.grid(True)
        plx.ticks_style("bold")

        # Markers for graph
        s, i, e, r, d = ["◆", "●", "▲", "◆", "■"]

        # Add curves based on the model type
        if model == "SIR":
            susceptible, infected, recovered = values
        elif model == "SEIRD":
            susceptible, exposed, infected, recovered, dead = values
            plx.plot(time, exposed, label="Exposed", color="orange", marker=e)
            plx.plot(time, dead, label="Dead", color="black", marker=d)

        plx.plot(time, susceptible, label="Susceptible", color="blue", marker=s)
        plx.plot(time, infected, label="Infected", color="red", marker=i)
        plx.plot(time, recovered, label="Recovered", color="darkgreen", marker=r)

        plx.canvas_color("lightgrey")
        plx.ticks_color("black")
        plx.show()
