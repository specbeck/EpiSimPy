from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt, IntPrompt
from core import Epidemic

# Create a console object for Rich
console = Console()

def display_banner():
    """Displays a banner for the application."""
    console.print("[bold blue]Welcome to Epidemic Simulator[/bold blue]", style="bold white on blue")
    console.print("[italic]Simulate epidemic dynamics using SIR models[/italic]", style="cyan")

def get_simulation_parameters():
    """Interactive prompts to get simulation parameters from the user."""
    console.print("\n[bold]Enter Simulation Parameters[/bold]", style="magenta")
    population_size = IntPrompt.ask("Population size (e.g., 500)", default=500)
    beta = FloatPrompt.ask("Infection rate β (e.g., 0.001)", default=0.001)
    gamma = FloatPrompt.ask("Recovery rate γ (e.g., 0.1)", default=0.1)
    duration = IntPrompt.ask("Simulation duration in days (e.g., 100)", default=100)
    return population_size, beta, gamma, duration

def show_parameters_table(population_size, beta, gamma, duration):
    """Displays the parameters in a table."""
    table = Table(title="Simulation Parameters", show_header=True, header_style="bold blue")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Population Size", str(population_size))
    table.add_row("Infection Rate (β)", str(beta))
    table.add_row("Recovery Rate (γ)", str(gamma))
    table.add_row("Duration (Days)", str(duration))
    console.print(table)

def prompt_and_run(population_size, beta, gamma, duration):
    if Prompt.ask("\n[bold yellow]Start the simulation?[/bold yellow] (y/n)", choices=["y", "n"]) == "y":
        console.print("\n[bold green]Running simulation...[/bold green]")
        
        # Run the epidemic simulation
        epidemic = Epidemic(population_size, beta, gamma, duration)
        epidemic.run()
        
        console.print("[bold green]Simulation complete![/bold green]")
    else:
        console.print("[bold red]Simulation aborted![/bold red]")
