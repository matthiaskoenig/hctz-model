"""Tool to run the hctz model factory and simulation experiments."""

import sys
import os
import subprocess
from enum import Enum
import optparse
from pathlib import Path
from pkdb_models.models.hctz import HCTZ_PATH
from pkdb_models.models.hctz.simulations import run_simulation_experiments, EXPERIMENTS
from sbmlutils.console import console

FACTORY_SCRIPT_PATH = HCTZ_PATH / "models" / "factory.py"

class Action(str, Enum):
    # simulations
    SIMULATE = "simulate"
    LIST_EXPERIMENTS = "list_experiments"
    # factory
    FACTORY = "factory"
    # run all
    ALL = "all"


def _setup_custom_results_paths(results_dir: str):
    """Override default results paths with custom directory for custom figure output directory."""
    import pkdb_models.models.hctz as hctz
    custom_path = Path(results_dir).resolve()
    custom_path.mkdir(parents=True, exist_ok=True)
    # Override the module paths
    hctz.RESULTS_PATH = custom_path
    hctz.RESULTS_PATH_SIMULATION = custom_path / "simulation"
    console.print(f"Figure output directory set to: [cyan]{custom_path}[/cyan]")
    return custom_path


def _get_current_results_path():
    """Get the current results path (default or custom)."""
    from pkdb_models.models.hctz import RESULTS_PATH
    return RESULTS_PATH


def _run_factory():
    """Executes the model factory script."""
    console.rule("[bold cyan]Running Model Factory[/bold cyan]", style="cyan")
    subprocess.run(
        [sys.executable, str(FACTORY_SCRIPT_PATH)],
        cwd=FACTORY_SCRIPT_PATH.parent,
        check=True,
    )
    console.print("[bold green]Factory finished.[/bold green]")
    console.rule(style="green")


def _list_available_experiments():
    """Display all available experiment groups and individual experiments."""
    console.rule("[bold cyan]Available Simulation Experiments[/bold cyan]", style="cyan")
    console.print("\n[bold]You can use these group names:[/bold]")
    console.print(f"  {', '.join([g for g in EXPERIMENTS.keys()])}")
    console.print("\n[bold]Or these individual experiment names:[/bold]")

    for group_name in ["studies", "misc", "scan"]:
        if group_name in EXPERIMENTS and EXPERIMENTS[group_name]:
            console.print(f"\n[yellow]{group_name}:[/yellow]")
            for exp in EXPERIMENTS[group_name]:
                console.print(f"  {exp.__name__}")

    console.print("\n[dim]Use '--experiments' with comma-separated names to run specific experiments.[/dim]")
    console.print('[dim]Example: run_hctz --action simulate --experiments "misc,Anderson1961"[/dim]')
    console.print('[dim]Or use "all" to run all experiments: run_hctz --action simulate --experiments all[/dim]\n')


def _resolve_experiment_names(experiment_names: list) -> tuple:
    """Resolve experiment names to experiment classes."""
    # Build dictionary of all available experiments by name
    all_available_exp = {}
    for category, exp_list in EXPERIMENTS.items():
        if category != "all":
            for exp in exp_list:
                all_available_exp[exp.__name__] = exp

    # Validate and collect requested experiments
    experiment_classes = []
    not_found = []

    for exp_name in experiment_names:
        # Check if it's a group name
        if exp_name in EXPERIMENTS:
            experiment_classes.extend(EXPERIMENTS[exp_name])
        # Check if it's an individual experiment
        elif exp_name in all_available_exp:
            experiment_classes.append(all_available_exp[exp_name])
        else:
            not_found.append(exp_name)

    return experiment_classes, not_found


def main() -> None:
    parser = optparse.OptionParser()
    parser.add_option(
        "-a", "--action",
        dest="action",
        help=f"The main action to perform. Choices: {[a.value for a in Action]} (required)",
    )
    parser.add_option(
        "-r", "--results-dir",
        dest="results_dir",
        help="Optional: Custom directory to save all results/figures (default: ./results)",
    )
    parser.add_option(
        "-e", "--experiments",
        dest="experiments",
        help="Comma-separated list of simulation experiments and/or groups (for '--action simulate'). "
             "Use '--action list_experiments' to see all available options.",
    )

    console.rule("[bold cyan]HCTZ PBPK/PD MODEL[/bold cyan]", style="cyan")

    options, args = parser.parse_args()

    def _parser_message(text: str) -> None:
        console.print(f"[bold red]Error: {text}[/bold red]")
        parser.print_help()
        console.rule(style="red")
        sys.exit(1)

    if not options.action:
        _parser_message("Required argument '--action' is missing.")

    try:
        action = Action(options.action.lower())
    except ValueError:
        _parser_message(f"Invalid action '{options.action}'. Please choose from {[a.value for a in Action]}.")

    # Setup custom results directory if provided
    if options.results_dir:
        _setup_custom_results_paths(options.results_dir)
    else:
        import pkdb_models.models.hctz as hctz
        default_path = _get_current_results_path()
        if options.action and options.action.lower() == "factory":
            console.print(f"[cyan]Factory will use model base path: {hctz.MODEL_BASE_PATH}[/cyan]")
        else:
            console.print(f"[cyan]Using figure results directory: {default_path}[/cyan]")

    # Handle different actions
    if action == Action.FACTORY:
        _run_factory()

    elif action == Action.LIST_EXPERIMENTS:
        _list_available_experiments()

    elif action == Action.SIMULATE:
        if not options.experiments:
            _parser_message("For '--action simulate', the '--experiments' argument is required.")

        # Parse experiment names
        exp_list = [e.strip() for e in options.experiments.split(",")]

        # Resolve names to experiment classes
        experiment_classes, not_found = _resolve_experiment_names(exp_list)

        # Report any experiments that weren't found
        if not_found:
            console.rule(style="red bold")
            console.print(f"[red]Warning: The following experiments were not found: {', '.join(not_found)}[/red]")
            console.rule(style="red bold")

        if not experiment_classes:
            console.rule(style="red bold")
            console.print("[red]Error: No valid experiments to run![/red]")
            console.rule(style="red bold")
            return

        # Run the experiments
        results_path = _get_current_results_path()
        console.rule("[bold cyan]Running Simulations[/bold cyan]", style="cyan")
        run_simulation_experiments(experiment_classes=experiment_classes)
        console.print("[bold green]Simulations finished.[/bold green]")
        console.print(f"[bold green]Results saved to: {results_path / 'simulation'}[/bold green]")

    elif action == Action.ALL:
        console.rule("[bold cyan]Running: Factory and all simulations.[/bold cyan]", style="cyan")
        _run_factory()
        run_simulation_experiments(selected="all")
        console.print("\n[bold green]All scripts completed successfully![/bold green]")

    console.rule(style="white")


if __name__ == "__main__":
    """
    This script is intended to be run from the command line as 'run_hctz'.

    -------------------------------------------------
    Usage Examples (to be run in your terminal):
    -------------------------------------------------

    1. Help:
       Shows all available options and actions.
       $ run_hctz --help

    2. Run the Model Factory:
       Generates all SBML model files.
       $ run_hctz --action factory

    3. Run Simulations:
       List available experiments:
       $ run_hctz --action list_experiments

       Run all experiments:
       $ run_hctz --action simulate --experiments all

    5. Run Everything:
       Runs factory and all simulations.
       $ run_hctz --action all
       
       With custom results directory for figures:
       $ run_hctz --action all --results-dir '/path/to/my/results'
    """
    main()