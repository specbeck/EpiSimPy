from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt, IntPrompt
from core import Epidemic
from simulation import run

# Create a console object for Rich
console = Console()


def display_banner() -> None:
    """Displays a banner for the application."""
    console.print(
        "EpiSimPy",
        style="bold white on blue",
    )
    console.print(
        "[italic]Compartmental models in epidemiology[/italic]",
        style="cyan",
    )


def get_simulation_parameters() -> tuple[str, int, dict[str, float], int]:
    """Interactive prompts to get simulation parameters from the user."""

    console.print("\n[bold]Enter Simulation Parameters[/bold]", style="magenta")
    model = Prompt.ask(
        "Choose the epidemic model", choices=["SIR", "SEIRD"], default="SIR"
    )
    population_size = IntPrompt.ask("Population size", default=500)
    duration = IntPrompt.ask("Epidemic duration (in days)", default=100)

    # Common parameters
    params = {
        "beta": FloatPrompt.ask("Infection rate β (e.g., 0.001)", default=0.001),
        "gamma": FloatPrompt.ask("Recovery rate γ (e.g., 0.1)", default=0.1),
    }

    # Additional parameters for SEIRD model
    if model == "SEIRD":
        params["sigma"] = FloatPrompt.ask("Incubation rate σ (e.g., 0.2)", default=0.2)
        params["mu"] = FloatPrompt.ask("Mortality rate μ (e.g., 0.01)", default=0.01)

    return model, population_size, params, duration


def show_parameters_table(
    model: str, population_size: int, params: dict[str, float], duration: int
) -> None:
    """Displays the parameters in a table."""
    table = Table(
        title="Simulation Parameters", show_header=True, header_style="bold white"
    )
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Model", model)
    table.add_row("Population Size", str(population_size))
    table.add_row("Infection Rate (β)", str(params["beta"]))
    table.add_row("Recovery Rate (γ)", str(params["gamma"]))

    if model == "SEIRD":
        table.add_row("Incubation Rate (σ)", str(params["sigma"]))
        table.add_row("Mortality Rate (μ)", str(params["mu"]))

    table.add_row("Duration (Days)", str(duration))
    console.print(table)


def prompt_and_run(
    model: str, population_size: int, params: dict[str, float], duration: int
) -> None:
    """Prompts the user and runs the main program."""
    if (
        Prompt.ask(
            "\n[bold yellow]Start the program?[/bold yellow] (y/n)",
            choices=["y", "n"],
        )
        == "y".casefold()
    ):
        console.print("\n[bold green]Running simulation...[/bold green]")

        # Run the epidemic simulation
        epidemic = Epidemic(population_size, params, duration, model)
        epidemic.run()

        simtype = Prompt.ask(
            "What simulation style would you prefer",
            choices=["normal", "real"],
            default="normal",
        )

        if (
            Prompt.ask(
                "\n[bold yellow]Run the stochastic simulation with same parameters?[/bold yellow]",
                choices=["y", "n"],
                default="n",
            )
            == "y".casefold()
        ):
            run(population_size, params, duration, simtype)
        else:
            run(simtype=simtype)

        console.print("[bold green]Simulation complete![/bold green]")
    else:
        console.print("[bold red]Simulation aborted![/bold red]")
