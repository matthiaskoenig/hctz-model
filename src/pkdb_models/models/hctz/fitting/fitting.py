"""HCTZ parameter fitting."""
import logging
from pathlib import Path

import itertools
from typing import List, Dict, Tuple

from pymetadata.console import console
from sbmlsim.fit import FitParameter, FitExperiment
from sbmlsim.fit.result import OptimizationResult
from sbmlsim.fit.optimization import OptimizationProblem
from sbmlsim.fit.analysis import OptimizationAnalysis
from sbmlsim.fit.runner import run_optimization
from sbmlsim.fit.options import *
from sbmlsim.fit.sampling import SamplingType

from pkdb_models.models.hctz.fitting.fit_experiments import (
    f_fitexp_pk,
    f_fitexp_pd,
    f_fitexp_pkiv,
)
from pkdb_models.models.hctz.fitting.parameters import (
    parameters_pk,
    parameters_pk_iv,
    parameters_pd,
)

from pkdb_models.models.hctz import (
    HCTZ_PATH,
    DATA_PATHS,
)

logger = logging.getLogger(__name__)

fit_kwargs = {
    # optimization settings
    "residual": ResidualType.NORMALIZED,
    "loss_function": LossFunctionType.LINEAR,
    "weighting_curves": [
        WeightingCurvesType.MAPPING,  # user defined weights # FIXME
        WeightingCurvesType.POINTS,  # number of points
    ],
    "weighting_points": WeightingPointsType.ERROR_WEIGHTING,  # no errors weighed with CV=0.5
    # additional integrator settings
    "variable_step_size": True,
    "relative_tolerance": 1e-6,
    "absolute_tolerance": 1e-6,
    # serial optimization
    # "serial": False,
}


def create_optimization_problem(
    fit_experiments: List[FitExperiment], opid: str, parameters: List[FitParameter]
) -> OptimizationProblem:
    op = OptimizationProblem(
        opid=opid,
        fit_experiments=fit_experiments,
        fit_parameters=parameters,
        base_path=HCTZ_PATH,
        data_path=DATA_PATHS,
    )
    return op


def fitlsq(op, seed: int, **kwargs) -> Tuple[OptimizationResult, OptimizationProblem]:
    """Local least square fitting."""
    opt_res = run_optimization(
        problem=op,
        seed=seed,
        algorithm=OptimizationAlgorithmType.LEAST_SQUARE,
        # parameters for least square optimization
        sampling=SamplingType.LOGUNIFORM_LHS,
        diff_step=0.05,
        # diff_step=0.05,
        # ftol=1e-10,
        # xtol=1e-10,
        # gtol=1e-10,
        **kwargs
    )
    return opt_res, op


def fitde(op, seed: int, **kwargs) -> Tuple[OptimizationResult, OptimizationProblem]:
    """Global differential evolution fitting."""
    opt_res = run_optimization(
        problem=op,
        seed=seed,
        algorithm=OptimizationAlgorithmType.DIFFERENTIAL_EVOLUTION,
        **kwargs
    )
    return opt_res, op


class OptimizationStrategy(str, Enum):
    """Strategy for fitting.

    Either fit all experiments together or individually.
    """

    ALL = "ALL",  # fit all experiments together, i.e, one parameter set
    SINGLE = "SINGLE",  # fit individual experiments, i.e. set of parameters for every experiment


class FitMethod(str, Enum):
    """Method for fitting."""

    LSQ = "LSQ",
    DE = "DE",


class FitExperimentSubset(str, Enum):
    """Subset of fit experiments for fitting."""

    PKIV = "PKIV",
    PK = "PK",
    PD = "PD",



def fit_hctz(
    optimization_strategy: OptimizationStrategy,
    fit_method: FitMethod,
    fit_experiments: List[FitExperiment],
    parameters: List[FitParameter],
    n_cores: int,
    n_optimizations: int,
    seed: int,
) -> Dict[str, Tuple[OptimizationResult, OptimizationProblem]]:

    if not isinstance(optimization_strategy, OptimizationStrategy):
        raise ValueError
    if not isinstance(fit_method, FitMethod):
        raise ValueError

    def fit_op(
        op: OptimizationProblem,
    ) -> Tuple[OptimizationResult, OptimizationProblem]:
        """Wrapper for optimization function."""

        # run optimization
        opt_result: OptimizationResult
        op: OptimizationProblem
        if fit_method == FitMethod.LSQ:
            opt_result, op = fitlsq(op, seed=seed, size=n_optimizations, n_cores=n_cores, **fit_kwargs)
        elif fit_method == FitMethod.DE:
            opt_result, op = fitde(op, seed=seed, size=n_optimizations, n_cores=n_cores, **fit_kwargs)

        return opt_result, op

    # store optimization results
    results = {}

    if optimization_strategy == OptimizationStrategy.SINGLE:
        # fit all experiments individually
        for fit_exp in fit_experiments:
            opid = fit_exp.experiment_class.__name__

            op = create_optimization_problem(
                fit_experiments=[fit_exp], opid=opid, parameters=parameters
            )
            results[opid] = fit_op(op=op)

    elif optimization_strategy == OptimizationStrategy.ALL:
        # fit all experiments together
        opid = "all"
        op = create_optimization_problem(
            fit_experiments=fit_experiments, opid=opid, parameters=parameters
        )
        results[opid] = fit_op(op)

    return results


def get_fit_experiments(fit_subset: FitExperimentSubset, study_ids: List[str] = None):
    """Creates a subset of fit experiments from given information."""
    if not isinstance(fit_subset, FitExperimentSubset):
        raise ValueError
    if fit_subset == FitExperimentSubset.PKIV:
        fitexp_dict = f_fitexp_pkiv()
    elif fit_subset == FitExperimentSubset.PK:
        fitexp_dict = f_fitexp_pk()
    elif fit_subset == FitExperimentSubset.PD:
        fitexp_dict = f_fitexp_pd()

    if study_ids:
        fit_experiments = [fitexp_dict[sid] for sid in study_ids]
    else:
        fit_experiments = [exp for exp in fitexp_dict.values()]

    # reduce list of lists
    fit_experiments = list(itertools.chain(*fit_experiments))
    return fit_experiments


def get_fit_parameters(fit_subset: FitExperimentSubset) -> List[FitParameter]:
    """Creates a subset of fit experiments from given information."""
    if not isinstance(fit_subset, FitExperimentSubset):
        raise ValueError
    if fit_subset == FitExperimentSubset.PKIV:
        parameters = parameters_pk_iv
    elif fit_subset == FitExperimentSubset.PK:
        parameters = parameters_pk
    elif fit_subset == FitExperimentSubset.PD:
        parameters = parameters_pd

    return parameters


def main() -> None:
    """Entry point which runs parameter fitting script.

    The script is registered as `fit_hctz` command.
    """

    import optparse
    import sys

    parser = optparse.OptionParser()
    parser.add_option(
        "-c",
        "--cores",
        action="store",
        dest="cores",
        help="Number of cores to use for optimization",
    )
    parser.add_option(
        "-r",
        "--runs",
        action="store",
        dest="runs",
        help="Number of optimization runs",
    )
    parser.add_option(
        "-s",
        "--seed",
        action="store",
        dest="seed",
        help="Seed for optimization (ensures reproducibility)",
    )
    parser.add_option(
        "-t",
        "--strategy",
        action="store",
        dest="strategy",
        help="Optimization strategy [ALL, SINGLE]",
    )
    parser.add_option(
        "-n",
        "--name",
        action="store",
        dest="name",
        help="Name for optimization",
    )
    parser.add_option(
        "-m",
        "--method",
        action="store",
        dest="method",
        help="Method for optimization [LSQ, DE]",
    )
    parser.add_option(
        "-x",
        "--subset",
        action="store",
        dest="subset",
        help="Subset for optimization",
    )
    parser.add_option(
        "-o",
        "--output_dir",
        action="store",
        dest="output_dir",
        help="Path to output folder with optimization results (optional)",
    )

    console.rule(style="white")
    console.print(":wrench: FIT HCTZ :wrench:")
    console.rule(style="white")

    options, args = parser.parse_args()

    def _parser_message(text: str) -> None:
        console.print(text)
        parser.print_help()
        console.rule(style="white")
        sys.exit(1)

    if not options.cores:
        _parser_message("Required argument '--cores' missing.")
    if not options.runs:
        _parser_message("Required argument '--runs' missing.")
    if not options.seed:
        _parser_message("Required argument '--seed' missing.")
    if not options.method:
        _parser_message("Required argument '--method' missing.")
    if not options.strategy:
        _parser_message("Required argument '--strategy' missing.")
    if not options.subset:
        _parser_message("Required argument '--subset' missing.")

    output_dir: Path
    if not options.output_dir:
        from pkdb_models.models.hctz import RESULTS_PATH_FIT
        output_dir = RESULTS_PATH_FIT
    else:
        output_dir = Path(options.output_dir)

    if not output_dir.exists():
        console.log(f"Create output directory: {output_dir}")
        output_dir.mkdir(parents=True)

    n_cores: int = int(options.cores)
    n_optimizations: int = int(options.runs)
    seed: int = int(options.seed)
    name: str = str(options.name)
    method: str = str(options.method)
    subset: str = str(options.subset)
    strategy: str = str(options.strategy)

    fit_method = FitMethod(method)
    fit_subset = FitExperimentSubset(subset)
    optimization_strategy = OptimizationStrategy(strategy)

    console.print(f"{'cores':<20}: {n_cores}")
    console.print(f"{'runs':<20}: {n_optimizations}")
    console.print(f"{'seed':<20}: {seed}")
    console.print(f"{'name':<20}: {name}")
    console.print(f"{'method':<20}: {fit_method}")
    console.print(f"{'subset':<20}: {fit_subset}")
    console.print(f"{'strategy':<20}: {optimization_strategy}")
    console.rule(style="white")

    console.rule("Parameters", align="left", style="white")
    parameters = get_fit_parameters(fit_subset=fit_subset)
    console.print(FitParameter.parameters_to_df(parameters))

    # Run optimization
    fit_experiments = get_fit_experiments(fit_subset=fit_subset)

    # FIXME: this must store the results
    results: Dict[str, Tuple[OptimizationResult, OptimizationProblem]] = fit_hctz(
        fit_experiments=fit_experiments,
        parameters=parameters,
        optimization_strategy=optimization_strategy,
        fit_method=fit_method,
        n_cores=n_cores,
        n_optimizations=n_optimizations,
        seed=seed,
    )
    # TODO: serialization

    console.rule(style="white")
    # Create report
    # FIXME: this creates the analysis;
    # TODO: separate in different command

    # parameters for plots
    mpl_parameters = {
        # 'axes.labelsize': 12,
        # 'axes.labelweight': "bold",
    }
    for key, (opt_result, op) in results.items():
        # create figures and outputs
        opt_analysis = OptimizationAnalysis(
            opt_result=opt_result,
            op=op,
            output_name=name,
            output_dir=output_dir,
            show_plots=False,
            show_titles=False,
            **fit_kwargs
        )
        opt_analysis.run(mpl_parameters=mpl_parameters)


if __name__ == "__main__":
    """
    Parameter fitting should be executed from the terminal:
    
    # ensure latest codes and commands
        
    cd ~/git/sbmlsim
    git pull
    cd ~/git/pkdb_data
    git pull
    cd ~/git/pkdb_models
    git pull
    workon pkdb_models
    pip install -e . --upgrade
        
    # run parameter fitting via terminal, e.g. default output directory (10 optimizations on 10 cores)
    fit_hctz
    fit_hctz --cores=10 --runs=10 --seed=1234 --method=LSQ --strategy=ALL --subset=PKIV --name=PKIV_LSQ_ALL
    fit_hctz --cores=10 --runs=10 --seed=1234 --method=LSQ --strategy=ALL --subset=PK --name=PK_LSQ_ALL
    fit_hctz --cores=10 --runs=10 --seed=1234 --method=LSQ --strategy=ALL --subset=PD --name=PD_LSQ_ALL
    """
    main()
