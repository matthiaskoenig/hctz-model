from typing import List, Type, Union

from pkdb_models.models.hctz import (
    DATA_PATHS,
    MODEL_PATH,
    HCTZ_PATH,
    RESULTS_PATH_SIMULATION,
)
from sbmlsim.experiment import ExperimentRunner, SimulationExperiment
from sbmlsim.report.experiment_report import ExperimentReport, ReportResults

# from sbmlsim.simulator.simulation_ray import SimulatorParallel
from sbmlsim.simulator.simulation_serial import SimulatorSerial
from sbmlutils import log
from sbmlutils.console import console

from sbmlsim.plot import Figure

Figure.legend_fontsize = 10
logger = log.get_logger(__name__)


def run_experiments(
    experiment_classes: Union[
        Type[SimulationExperiment], List[Type[SimulationExperiment]]
    ],
    output_dir: str,
):
    """Execute given simulation experiment(s)."""
    output_path = RESULTS_PATH_SIMULATION / output_dir
    # simulator = SimulatorParallel(model=MODEL_PATH)
    simulator = SimulatorSerial(model=MODEL_PATH)

    if isinstance(experiment_classes, SimulationExperiment):
        experiment_classes = [experiment_classes]

    runner = ExperimentRunner(
        experiment_classes=experiment_classes,
        data_path=DATA_PATHS,
        base_path=HCTZ_PATH,
        simulator=simulator,
        absolute_tolerance=1e-10,
        relative_tolerance=1e-10,
    )
    results = runner.run_experiments(
        output_path=output_path,
        show_figures=True,
        save_results=False,
        figure_formats=["svg", "png"],
        reduced_selections=True,
    )

    report_results = ReportResults()
    for exp_result in results:
        report_results.add_experiment_result(exp_result=exp_result)

    # create HTML report
    report = ExperimentReport(report_results, metadata=None)
    report.create_report(output_path, report_type=ExperimentReport.ReportType.HTML)

    console.print("Successfully executed simulation experiments", style="success")
