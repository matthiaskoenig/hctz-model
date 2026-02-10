"""Run HCTZ simulation experiments."""
import shutil
from pathlib import Path

from pkdb_models.models.hctz.helpers import run_experiments
from pkdb_models.models.hctz.experiments.studies import *
from pkdb_models.models.hctz.experiments.misc import *
import pkdb_models.models.hctz as hctz

from sbmlutils import log
from sbmlutils.console import console


logger = log.get_logger(__name__)


EXPERIMENTS = {
    "studies": [
        Anderson1961,
        Azumaya1990,
        Barbhaiya1982,
        Barbhaiya1982a,
        Beerman1976,
        Beermann1977a,
        Beermann1979,
        Devineni2014,
        Giudicelli1987,
        Heise2015,
        Howes1991,
        Hsiao2015,
        Hunninghake1986,
        # Januszewicz1959, # removed from analysis
        Jeon2012,
        Jordo1979,
        Koytchev2004,
        Niemeyer1983,
        Nilsen1989,
        Niopas2011,
        Patel1984,
        Ripley2000,
        Vaidyanathan2006,
        Weir1998,
        Williams1982,
    ],
    "renal_impairment": [
        Anderson1961,
        Niemeyer1983,
        Beermann1979,
    ],
    "cardiac_impairment": [
        Anderson1961,
        Niemeyer1983,
        Beermann1979,
    ],
    "hepatic_impairment": [
        Anderson1961,
    ],
    "pharmacodynamics": [
        Beermann1977a,
        Giudicelli1987,
        # Januszewicz1959, # removed from analysis
        Jeon2012,
        Nilsen1989,
        Ripley2000,
        Williams1982,
    ],
    "raas": [
        Giudicelli1987,
        Jeon2012,
    ],
    "misc": [DoseDependencyExperiment],
}
EXPERIMENTS["all"] = EXPERIMENTS["studies"] + EXPERIMENTS["misc"]


def run_simulation_experiments(
        selected: str = None,
        experiment_classes: list = None,
        output_dir: Path = None
) -> None:
    """Run hctz simulation experiments."""

    # Figure.fig_dpi = 600
    # Figure.legend_fontsize = 10

    # Determine which experiments to run
    if experiment_classes is not None:
        experiments_to_run = experiment_classes
        if output_dir is None:
            output_dir = hctz.RESULTS_PATH_SIMULATION / "custom_selection"
    elif selected:
        # Using the 'selected' parameter
        if selected not in EXPERIMENTS:
            console.rule(style="red bold")
            console.print(
                f"[red]Error: Unknown group '{selected}'. Valid groups: {', '.join(EXPERIMENTS.keys())}[/red]"
            )
            console.rule(style="red bold")
            return
        experiments_to_run = EXPERIMENTS[selected]
        if output_dir is None:
            output_dir = hctz.RESULTS_PATH_SIMULATION / selected
    else:
        console.print("\n[red bold]Error: No experiments specified![/red bold]")
        console.print("[yellow]Use selected='all' or selected='studies' or provide experiment_classes=[...][/yellow]\n")
        return

    # Run the experiments
    run_experiments(experiment_classes=experiments_to_run, output_dir=output_dir)

    # Collect figures into one folder
    figures_dir = output_dir / "_figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    for f in output_dir.glob("**/*.png"):
        if f.parent == figures_dir:
            continue
        try:
            shutil.copy2(f, figures_dir / f.name)
        except Exception as err:
            print(f"file {f.name} in {f.parent} fails, skipping. Error: {err}")
    console.print(f"Figures copied to: file://{figures_dir}", style="info")


if __name__ == "__main__":
    """
    # Run experiments

    # selected = "renal_impairment"
    # selected = "renal_impairment"
    # selected = "cardiac_impairment"
    # selected = "hepatic_impairment"
    # selected = "pharmacodynamics"
    # selected = "all"
    # selected = "scan"
    """

    run_simulation_experiments(selected="all")

    # typst
    # from pkdb_models.models.hydrochlorothiazide.thesis.supplementary_figures import create_supplement_typ
    # path_typ = RESULTS_PATH_SIMULATION / selected / "supplement.typ"
    # path_pdf = RESULTS_PATH_SIMULATION / selected / "supplement.pdf"
    # create_supplement_typ(path_typ=path_typ, figures_dir=figures_dir)

    # compilation to pdf
    # typst.compile(input=str(path_typ), output=str(path_pdf))
    # console.print(f"Report created: file://{path_pdf}", style="info")
    #

