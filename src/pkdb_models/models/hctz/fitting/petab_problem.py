"""Write a HCTZ fit as a PEtab v2 problem and read it back.

The PEtab layer of `sbmlsim.fit.petab_v2` on the fit problems of the model: the
fit is written as a PEtab v2 problem, validated with `petab` itself and read
back into an optimization problem, and what the tables of PEtab cannot express
is reported before anything is written. The module is run as a script:

    python -m pkdb_models.models.hctz.fitting.petab_problem
    python -m pkdb_models.models.hctz.fitting.petab_problem --subset=PD --portable

The problem is written into `RESULTS_PATH_PETAB/<subset>` of the model, unless
`--output-dir` is given.

The round trip is checked (`round_trip`) and the command fails on a problem:
PEtab validates the problem without an error (the one warning allowed is that
PEtab cannot validate the `sbmlsim` extension); the read back problem has the
settings, the parameters (ids, units, bounds, start values) and the fit
mappings (by study and key, with their kinds) of the fit; and its residuals of
every mapping and its cost agree at the start values, the bounds and two random
points (`RTOL_RESIDUALS`, `RTOL`). With `--portable` the extension is not required: a tool which
does not read it compares a data point at the time of a change with the state
after the change (PEtab v2), the fit with the state before it (e.g. the end of
a urine collection), so the objective of another tool differs from the fit.

The module is not called `petab.py`: run as a script its directory is the first
entry of `sys.path`, so `import petab` would find this file instead of the
library and fail with "'petab' is not a package".
"""

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import petab.v2 as petab_v2
from rich import box
from rich.table import Table
from sbmlsim.console import console
from sbmlsim.fit import display
from sbmlsim.fit.optimization import OptimizationProblem
from sbmlsim.fit.petab_v2 import gaps_of_problem, gaps_table, to_petab
from sbmlsim.fit.petab_v2.extension import extension_of
from sbmlsim.fit.petab_v2.reader import from_petab

from pkdb_models.models.hctz import RESULTS_PATH_PETAB
from pkdb_models.models.hctz.fitting.fitting import FIT_DEFINITIONS

ICON_PETAB = ":package:"

#: the relative tolerance of the cost of the round trip
RTOL = 1e-5
#: the tolerance of the residuals of a mapping relative to its largest residual:
#: the IV infusions (Anderson1961) differ by up to 0.1 % after the round trip,
#: the oral doses by less than 1e-6
RTOL_RESIDUALS = 2e-3
#: the warning of PEtab which the round trip allows
EXTENSION_WARNING = "validation is not yet implemented: sbmlsim"


@dataclass
class RoundTrip:
    """The result of the round trip of a fit through PEtab v2.

    Attributes:
        yaml_file: the problem of PEtab.
        problems: what the round trip lost or changed, empty for a round trip
            without a problem.
        cost: the cost of the fit and of the problem read back at the start
            values.
    """

    yaml_file: Path
    problems: list[str] = field(default_factory=list)
    cost: tuple[float, float] = (np.nan, np.nan)


def _mapping_ids(problem: OptimizationProblem) -> list[tuple[str, str]]:
    """Get the study and the key of every fit mapping of a fit."""
    return list(zip(problem.experiment_keys, problem.mapping_keys, strict=True))


def _mapping_ids_read(
    problem: OptimizationProblem, ids: list[tuple[str, str]]
) -> list[tuple[str, str]]:
    """Get the study and the key of every fit mapping of a problem read back.

    The problem read back has the experiments of PEtab, it names a mapping
    `<study>__<key>` if two studies of the fit share its key, else by its key.

    Args:
        problem: the problem read back.
        ids: the studies and keys of the mappings of the fit.
    """
    studies = {study for study, _ in ids}
    known = {key: study for study, key in ids}
    read = []
    for key in problem.mapping_keys:
        study, _, rest = key.partition("__")
        if rest and study in studies and (study, rest) in ids:
            read.append((study, rest))
        else:
            read.append((known.get(key, "?"), key))
    return read


def _by_point(
    ids: list[tuple[str, str]], problem: OptimizationProblem, residuals: list
) -> dict[tuple[str, str], np.ndarray]:
    """Get the residuals of every mapping in the order of its data points."""
    ordered = {}
    for k, mapping_id in enumerate(ids):
        order = np.lexsort((problem.y_references[k], problem.x_references[k]))
        ordered[mapping_id] = np.asarray(residuals[k])[order]
    return ordered


def round_trip(subset: str, output_dir: Path, portable: bool = False) -> RoundTrip:
    """Write a fit as a PEtab v2 problem, validate it and read it back.

    Args:
        subset: the fit definition, a key of `FIT_DEFINITIONS`.
        output_dir: the directory the problem is written to (into `<subset>`).
        portable: write the `sbmlsim` extension as not required.

    Returns:
        The problem of PEtab and what the round trip lost, see the module.
    """
    definition = FIT_DEFINITIONS[subset]
    problem = definition.problem(opid=f"hctz_{subset}")
    problem.initialize(definition.settings)
    yaml_file = to_petab(
        problem, Path(output_dir) / subset, required_extension=not portable
    )
    result = RoundTrip(yaml_file=yaml_file)

    petab_problem = petab_v2.Problem.from_yaml(yaml_file)
    for issue in petab_problem.validate():
        if issue.level >= petab_v2.lint.ValidationIssueSeverity.ERROR or (
            EXTENSION_WARNING not in issue.message
        ):
            result.problems.append(f"PEtab: {issue.message}")

    read, settings = from_petab(yaml_file, opid=f"{subset}_petab")
    read.initialize(settings)
    if settings != definition.settings:
        result.problems.append("the settings are lost")
    for attribute in ["pid", "unit", "lower_bound", "upper_bound", "start_value"]:
        if [getattr(p, attribute) for p in read.parameters] != [
            getattr(p, attribute) for p in problem.parameters
        ]:
            result.problems.append(f"the {attribute} of the parameters are lost")

    ids = _mapping_ids(problem)
    ids_read = _mapping_ids_read(read, ids)
    kinds = dict(zip(ids, problem.mapping_kinds, strict=True))
    kinds_read = dict(zip(ids_read, read.mapping_kinds, strict=True))
    if sorted(ids) != sorted(ids_read) or len(set(ids)) != len(ids):
        result.problems.append("the fit mappings differ")
        return result
    if kinds != kinds_read:
        result.problems.append("the kinds of the fit mappings differ")

    # the residuals of every mapping and the cost at several parameters
    lower = np.array([p.lower_bound for p in problem.parameters], dtype=float)
    upper = np.array([p.upper_bound for p in problem.parameters], dtype=float)
    x0 = np.array(problem.x0, dtype=float)
    rng = np.random.default_rng(1)
    points = [x0, lower, upper] + [
        10 ** rng.uniform(np.log10(lower), np.log10(upper)) for _ in range(2)
    ]
    for k, x in enumerate(points):
        xlog = problem.to_scale(x)
        data = problem.residuals(xlog, complete_data=True)
        data_read = read.residuals(xlog, complete_data=True)
        if not isinstance(data, dict) or not isinstance(data_read, dict):
            raise TypeError("The complete data of the residuals is a dict.")
        # PEtab orders the measurements of a mapping by their time
        residuals = _by_point(ids, problem, data["residuals"])
        residuals_read = _by_point(ids_read, read, data_read["residuals"])
        for mapping_id, values in residuals.items():
            scale = max(float(np.max(np.abs(values), initial=0.0)), 1e-12)
            difference = float(
                np.max(np.abs(residuals_read[mapping_id] - values), initial=0.0)
            )
            if difference > RTOL_RESIDUALS * scale:
                result.problems.append(
                    f"the residuals of {mapping_id} differ at point {k}"
                )
        cost = problem.cost_least_square(xlog)
        cost_read = read.cost_least_square(xlog)
        if k == 0:
            result.cost = (cost, cost_read)
        if abs(cost - cost_read) > RTOL * max(abs(cost), np.finfo(float).tiny):
            result.problems.append(f"the cost differs at point {k}: {cost} {cost_read}")
    return result


def main() -> None:
    """Write a HCTZ fit as PEtab v2 and read it back."""
    parser = argparse.ArgumentParser(
        prog="petab_hctz", description=__doc__.split("\n")[0]
    )
    parser.add_argument(
        "--subset",
        default="PK",
        choices=sorted(FIT_DEFINITIONS),
        help="fit problem to write, the pharmacokinetics by default",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=RESULTS_PATH_PETAB,
        help="directory the problem is written to",
    )
    parser.add_argument(
        "--portable",
        action="store_true",
        help="write the `sbmlsim` extension as not required, i.e. a problem "
        "other tools fit with the objective of PEtab",
    )
    args = parser.parse_args()
    result = round_trip(args.subset, args.output_dir, portable=args.portable)

    definition = FIT_DEFINITIONS[args.subset]
    problem = definition.problem(opid=f"hctz_{args.subset}")
    problem.initialize(definition.settings)

    display.section(f"PEtab v2: {args.subset}", icon=ICON_PETAB)
    display.key_values(
        {
            "collections": len(problem.mapping_collections),
            "fit mappings": len(problem.mapping_keys),
            "parameters": len(problem.parameters),
            "data points": sum(len(y) for y in problem.y_references),
        }
    )

    # what PEtab v2 cannot express about this fit, before it is written
    display.section("Gaps", icon=":triangular_flag:")
    console.print(gaps_table(gaps_of_problem(problem)))

    # --- WRITE ---
    output_dir = Path(args.output_dir) / args.subset
    yaml_file = result.yaml_file

    display.section("Problem", icon=":open_file_folder:")
    for path in sorted(output_dir.iterdir()):
        if path.is_file():
            display.key_values({path.name: f"{path.stat().st_size / 1024:.1f} kB"})
    display.link("problem", yaml_file)

    # --- VALIDATE WITH PETAB ---
    petab_problem = petab_v2.Problem.from_yaml(yaml_file)
    extension = extension_of(petab_problem.config)
    issues = list(petab_problem.validate())
    display.section("PEtab", icon=":white_check_mark:")
    display.key_values(
        {
            "models": len(petab_problem.models),
            "experiments": len(petab_problem.experiments),
            "conditions": len(petab_problem.conditions),
            "observables": len(petab_problem.observables),
            "measurements": len(petab_problem.measurements),
            "parameters": len(petab_problem.parameters),
            "extension": f"required={extension.required}" if extension else "-",
            "issues": len(issues),
        }
    )
    for issue in issues:
        console.print(f"  {issue}")

    # every experiment of PEtab comes from a collection of fit mappings
    table = Table(box=box.SIMPLE_HEAD, header_style="bold", show_edge=False)
    for column in ["experiment", "collection", "periods", "observables"]:
        table.add_column(column)
    for experiment in petab_problem.experiments:
        info = extension.experiments.get(experiment.id, {}) if extension else {}
        observables = {
            m.observable_id
            for m in petab_problem.measurements
            if m.experiment_id == experiment.id
        }
        table.add_row(
            experiment.id,
            str(info.get("collection", "-")),
            str(len(experiment.periods)),
            str(len(observables)),
        )
    console.print(table)

    # --- READ BACK ---
    display.section("Read back", icon=":arrows_counterclockwise:")
    cost, cost_petab = result.cost
    display.key_values(
        {
            "cost": f"{cost:.6f} -> {cost_petab:.6f}",
            "problems": len(result.problems),
        }
    )
    for message in result.problems:
        console.print(f"  [red]{message}[/red]")
    if result.problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
