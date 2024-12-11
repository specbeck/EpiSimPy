from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt, IntPrompt
from core import Epidemic
from simulation import animate
import curses

# Create a console object for Rich
console = Console()


def display_banner():
    """Displays a banner for the application."""
    console.print(
        "[bold blue]Welcome to Epidemic Simulator[/bold blue]",
        style="bold white on blue",
    )
    console.print(
        "[italic]Simulate epidemic dynamics using SIR or SEIRD models[/italic]",
        style="cyan",
    )


def get_simulation_parameters():
    """Interactive prompts to get simulation parameters from the user."""
    console.print("\n[bold]Enter Simulation Parameters[/bold]", style="magenta")
    model = Prompt.ask(
        "Choose the epidemic model", choices=["SIR", "SEIRD"], default="SIR"
    )
    population_size = IntPrompt.ask("Population size (e.g., 500)", default=500)
    duration = IntPrompt.ask("Simulation duration in days (e.g., 100)", default=100)

    # Common parameters
    params = {
        "beta": FloatPrompt.ask("Infection rate β (e.g., 0.001)", default=0.001),
        "gamma": FloatPrompt.ask("Recovery rate γ (e.g., 0.1)", default=0.1),
    }

    # Additional parameters for SEIRD model
    if model == "SEIRD":
        params["sigma"] = FloatPrompt.ask("Incubation rate σ (e.g., 0.2)", default=0.2)
        params["delta"] = FloatPrompt.ask("Mortality rate δ (e.g., 0.01)", default=0.01)

    return model, population_size, params, duration


def show_parameters_table(model, population_size, params, duration):
    """Displays the parameters in a table."""
    table = Table(
        title="Simulation Parameters", show_header=True, header_style="bold blue"
    )
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Model", model)
    table.add_row("Population Size", str(population_size))
    table.add_row("Infection Rate (β)", str(params["beta"]))
    table.add_row("Recovery Rate (γ)", str(params["gamma"]))

    if model == "SEIRD":
        table.add_row("Incubation Rate (σ)", str(params["sigma"]))
        table.add_row("Mortality Rate (δ)", str(params["delta"]))

    table.add_row("Duration (Days)", str(duration))
    console.print(table)


def prompt_and_run(model, population_size, params, duration):
    """Prompts the user and runs the main program."""
    if (
        Prompt.ask(
            "\n[bold yellow]Start the simulation?[/bold yellow] (y/n)",
            choices=["y", "n"],
        )
        == "y"
    ):
        console.print("\n[bold green]Running simulation...[/bold green]")

        # Run the epidemic simulation
        epidemic = Epidemic(population_size, params, duration, model)
        epidemic.run()
        
        curses.wrapper(animate)

        console.print("[bold green]Simulation complete![/bold green]")
    else:
        console.print("[bold red]Simulation aborted![/bold red]")
