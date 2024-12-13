# Importing necessary functions for the cli
from cli import (
    display_banner,
    show_parameters_table,
    get_simulation_parameters,
    prompt_and_run,
)

# Displays the banner for the program
display_banner()

# Get user inputs for parameters
model, population_size, params, duration = get_simulation_parameters()

# Confirm and run simulation
prompt_and_run(model, population_size, params, duration)

# Display the parameters back to the user
show_parameters_table(model, population_size, params, duration)


