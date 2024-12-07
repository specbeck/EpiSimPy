import matplotlib.pyplot as plt
import plotext as plx
import time


# Maybe make this as a class later on
class Plot:
    
    @staticmethod
    def window(values, model, time, delay=0.1, step=1):
        """
        Plot the epidemic curve namely the values of individuals over time on a seperate window
        """

        plt.figure(figsize=(10, 6))
        plt.ion() # Interactive mode

        for t in range(0, len(time), step):
            plt.clf() # Clear previous figure
            
            dt = time[:t+1]

            if model == "SIR":
                susceptible, infected, recovered = values
            elif model == "SEIRD":
                susceptible, exposed, infected, recovered, dead = values
                plt.plot(dt, exposed[:t+1], label="Exposed", color="orange")
                plt.plot(dt, dead[:t+1], label="Dead", color="black")

            plt.plot(dt, susceptible[:t+1], label="Susceptible", color="blue")
            plt.plot(dt, infected[:t+1], label="Infected", color="red")
            plt.plot(dt, recovered[:t+1], label="Recovered", color="darkgreen")
        

            plt.legend()
            plt.xlabel("Time (Days)")
            plt.ylabel("Population")
            plt.title("Epidemic Curve")
            plt.pause(delay) # Pause with delay to simulate
        
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
        plx.plotsize(term_width - 10, term_height - 5)

        # Set the title, labels, and styles
        plx.title("Epidemic Curve")
        plx.xlabel("Days")
        plx.ylabel("Population")
        plx.grid(True)
        plx.ticks_style("bold")
        
        # Markers for graph
        s, i, e, r, d = ["•", "●", "▲", "◆", "■"]

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



        # Customize canvas and ticks color
        plx.canvas_color("lightgrey")
        plx.ticks_color("black")

        # Show the plot with legend
        #plx.legend(loc="upper right")
        plx.show()

    @staticmethod
    def terminal_dynamic(values, model, time_steps, delay=0.1):
        """
        Dynamically plots the epidemic curve in the terminal.
        """
        for t in range(len(time_steps)):
            plx.clf()  # Clear the terminal plot for each frame

            # Dynamically set the plot size based on terminal size
            term_width, term_height = plx.terminal_size()
            plx.plotsize(term_width - 10, term_height - 5)

            # Set the title, labels, and styles
            plx.title("Epidemic Curve")
            plx.xlabel("Days")
            plx.ylabel("Population")
            plx.grid(True)
            plx.ticks_style("bold")

            if model == "SIR":
                susceptible, infected, recovered = values
                plx.plot(time_steps[:t+1], susceptible[:t+1], label="Susceptible", color="blue", marker="●")
                plx.plot(time_steps[:t+1], infected[:t+1], label="Infected", color="red", marker="●")
                plx.plot(time_steps[:t+1], recovered[:t+1], label="Recovered", color="darkgreen", marker="●")

            elif model == "SEIRD":
                susceptible, exposed, infected, recovered, dead = values
                plx.plot(time_steps[:t+1], susceptible[:t+1], label="Susceptible", color="blue", marker="●")
                plx.plot(time_steps[:t+1], exposed[:t+1], label="Exposed", color="orange", marker="●")
                plx.plot(time_steps[:t+1], infected[:t+1], label="Infected", color="red", marker="●")
                plx.plot(time_steps[:t+1], recovered[:t+1], label="Recovered", color="darkgreen", marker="●")
                plx.plot(time_steps[:t+1], dead[:t+1], label="Dead", color="black", marker="●")

            plx.canvas_color("lightgrey")
            plx.ticks_color("black")

            plx.show()
            time.sleep(delay)  # Pause to simulate animation

        '''
    def terminal(values, model, time):
        """
        Plots the epidemic curve directly in the terminal.
        """
        # Set up the plot
        plx.clf()
        plx.title("Epidemic Curve")
        plx.xlabel("Days")
        plx.ylabel("Population")
    
        plx.plotsize(100, 30)

        # Add data to the plot
        if model == "SIR":
            susceptible, infected, recovered = values
            plx.plot(time, susceptible, label="Susceptible", color="blue")
            plx.plot(time, infected, label="Infected", color="red")
            plx.plot(time, recovered, label="Recovered", color="darkgreen")
        
        elif model == "SEIRD":
            susceptible, exposed, infected, recovered, dead = values
            plx.plot(time, susceptible, label="Susceptible", color="blue")
            plx.plot(time, exposed, label="Exposed", color="orange")
            plx.plot(time, infected, label="Infected", color="red")
            plx.plot(time, recovered, label="Recovered", color="darkgreen")
            plx.plot(time, dead, label="Dead", color="black")
    
        # Customize the plot
        plx.ticks_style("bold")
        plx.canvas_color("skyblue")
        plx.ticks_color("red")
        #    plx.legend(["Susceptible", "Infected", "Recovered"])
        plx.show()'''
