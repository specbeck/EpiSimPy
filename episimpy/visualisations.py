import matplotlib.pyplot as mplt
import plotext as plt
#from core import Status

# Maybe make this as a class later on
class Plot:
    
    @staticmethod
    def window(values, model, time):
        """
        Plot the epidemic curve namely the values of individuals over time on a seperate window
        """

        mplt.figure(figsize=(10, 6))
        
        if model == "SIR":
            susceptible, infected, recovered = values
            mplt.plot(time, susceptible, label="Susceptible", color="blue")
            mplt.plot(time, infected, label="Infected", color="red")
            mplt.plot(time, recovered, label="Recovered", color="darkgreen")
        
        elif model == "SEIRD":
            susceptible, exposed, infected, recovered, dead = values
            mplt.plot(time, susceptible, label="Susceptible", color="blue")
            mplt.plot(time, exposed, label="Exposed", color="orange")
            mplt.plot(time, infected, label="Infected", color="red")
            mplt.plot(time, recovered, label="Recovered", color="darkgreen")
            mplt.plot(time, dead, label="Dead", color="black")

        mplt.legend()
        mplt.xlabel("Days")
        mplt.ylabel("Population")
        mplt.title("Epidemic Curve")
        mplt.show()

    
    def terminal(values, model, time):
        """
        Plots the epidemic curve directly in the terminal with enhanced formatting.
        """
        # Clear the terminal plot
        plt.clf()

        # Dynamically set the plot size based on terminal size
        term_width, term_height = plt.terminal_size()
        plt.plotsize(term_width - 10, term_height - 5)

        # Set the title, labels, and styles
        plt.title("Epidemic Curve")
        plt.xlabel("Days")
        plt.ylabel("Population")
        plt.grid(True)
        plt.ticks_style("bold")

        # Add curves based on the model type
        if model == "SIR":
            susceptible, infected, recovered = values
            plt.plot(time, susceptible, label="Susceptible", color="blue", marker="~")
            plt.plot(time, infected, label="Infected", color="red", marker="*")
            plt.plot(time, recovered, label="Recovered", color="darkgreen", marker="^")

        elif model == "SEIRD":
            susceptible, exposed, infected, recovered, dead = values
            plt.plot(time, susceptible, label="Susceptible", color="blue", marker="~")
            plt.plot(time, exposed, label="Exposed", color="orange", marker="+")
            plt.plot(time, infected, label="Infected", color="red", marker="*")
            plt.plot(time, recovered, label="Recovered", color="darkgreen", marker="-")
            plt.plot(time, dead, label="Dead", color="black", marker="^")

        # Customize canvas and ticks color
        plt.canvas_color("lightgrey")
        plt.ticks_color("black")

        # Show the plot with legend
        #plt.legend(loc="upper right")
        plt.show()
    

        '''
    def terminal(values, model, time):
        """
        Plots the epidemic curve directly in the terminal.
        """
        # Set up the plot
        plt.clf()
        plt.title("Epidemic Curve")
        plt.xlabel("Days")
        plt.ylabel("Population")
    
        plt.plotsize(100, 30)

        # Add data to the plot
        if model == "SIR":
            susceptible, infected, recovered = values
            plt.plot(time, susceptible, label="Susceptible", color="blue")
            plt.plot(time, infected, label="Infected", color="red")
            plt.plot(time, recovered, label="Recovered", color="darkgreen")
        
        elif model == "SEIRD":
            susceptible, exposed, infected, recovered, dead = values
            plt.plot(time, susceptible, label="Susceptible", color="blue")
            plt.plot(time, exposed, label="Exposed", color="orange")
            plt.plot(time, infected, label="Infected", color="red")
            plt.plot(time, recovered, label="Recovered", color="darkgreen")
            plt.plot(time, dead, label="Dead", color="black")
    
        # Customize the plot
        plt.ticks_style("bold")
        plt.canvas_color("skyblue")
        plt.ticks_color("red")
        #    plt.legend(["Susceptible", "Infected", "Recovered"])
        plt.show()'''
