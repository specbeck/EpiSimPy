from core import Epidemic
from cli import display_banner, show_parameters_table, get_simulation_parameters, prompt_and_run

"""Main function for the interactive CLI."""
display_banner()
    
# Get user inputs for parameters
population_size, beta, gamma, duration = get_simulation_parameters()
    
# Display the parameters back to the user
show_parameters_table(population_size, beta, gamma, duration)
    
# Confirm and run simulation
prompt_and_run(population_size, beta, gamma, duration)


