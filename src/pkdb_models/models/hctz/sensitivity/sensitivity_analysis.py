"""Sensitivity analysis of the HCTZ model.

The outputs are the pharmacokinetic parameters of a single oral dose (the
non-compartmental analysis of `pkpdutils`) and the extremes of the
pharmacodynamics. The parameters are the parameters of the model with bounds
of +-15 % around their value. The analyses are run as a script, the local
analysis by default:

    python -m pkdb_models.models.hctz.sensitivity.sensitivity_analysis
    python -m pkdb_models.models.hctz.sensitivity.sensitivity_analysis local sampling

The analyses run on `pkpdsim.sensitivity.SensitivityRunner`, which writes the
table of the parameters into `results/sensitivity` of the model and the tables
and figures of an analysis into `results/sensitivity/<analysis>`.
An analysis does not vary a parameter which one of its groups sets
(`pkpdsim.sensitivity.free_parameters`): `sampling`, over the four groups, leaves
out `f_renal_function`. The environment variable `PKPDSIM_SENSITIVITY_N`
replaces the numbers of samples of the global analyses for a quick run, see
`pkpdsim.sensitivity.sample_size`.

The simulation of a group starts `EQUILIBRATION_DAYS` before the dose without
HCTZ: in impaired renal function the model without HCTZ is not stationary, the
extracellular fluid and with it the blood pressure rise to a new steady state
((ECF/ECF_ref)^10 = 1/f_renal_function; 120 to 141 mmHg in severe renal
impairment), which an analysis from the reference state would attribute to
HCTZ. After the equilibration the pressure without HCTZ changes by less than
0.05 mmHg in the following 720 hr, so that the change of the pressure against
its value at the dose is the effect of HCTZ (`min_bp_systolic`,
`min_bp_diastolic`), and the extremes are taken after the dose. The dose is
followed for `END_HR` hours, long enough for the non-compartmental analysis of
severe renal impairment (0.04 % of the maximal concentration at the end).
"""

from collections.abc import Callable, Mapping

import numpy as np
from pkpdsim.sensitivity import (
    FastAnalysis,
    LocalAnalysis,
    ParameterType,
    SamplingAnalysis,
    SensitivityGroup,
    SensitivityOutput,
    SensitivityParameter,
    SensitivityRunner,
    SobolAnalysis,
    parameters_from_sbml,
    set_bounds,
    set_relative_bounds,
)
from pkpdutils import NCAOptions
from sbmlsim import Q
from sbmlsim.simulation import PK, Change, Custom, Formula, Simulation

from pkdb_models.models.hctz import MODEL, MODEL_PATH
from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)
from pkdb_models.models.hctz.fitting.parameters import parameters_all as fit_parameters

#: oral dose of the analysis [mg]
DOSE_HCTZ = 25
#: the days without HCTZ before the dose, the equilibration of the fluid
EQUILIBRATION_DAYS = 14
#: the hours after the dose
END_HR = 720
#: the limit of quantification of the non-compartmental analysis [mM], 1e-6 of
#: the maximal concentration of the control (4.5e-4 mM) as in the scans
#: (`hctz_pk.LLOQ_FRACTION`), so that the noise of the integrator is not the
#: terminal phase
LLOQ = 4.5e-10
#: fraction of the bounds of a parameter relative to its value
BOUNDS_FRACTION = 0.15

#: outputs of the non-compartmental analysis of pkpdutils -> unit of the output
PK_OUTPUTS: dict[str, str] = {
    "auc_inf_obs": "mM*min",
    "cmax": "mM",
    "thalf": "min",
    "vz_f": "l",
    "cl_f": "ml/min",
    "lambda_z": "1/min",
}
#: the non-compartmental analysis of the concentration; the id `hctz` is a
#: species of the model, which an observable must not share
PK_ID = "pk_hctz"
#: the outputs whose unit has the amount of the dose: the dose is a mass
#: (`PODOSE_hctz` in mg), so they are divided by the molecular weight (its value
#: at the start, a value per simulation like the parameter of the analysis)
PK_PER_DOSE_MASS: frozenset[str] = frozenset({"vz_f", "cl_f"})


def max_after_dose(time: np.ndarray, values: dict[str, np.ndarray]) -> float:
    """Get the maximum of a timecourse after the dose (time 0)."""
    (x,) = values.values()
    return float(np.max(x[time >= 0]))


def change_after_dose(time: np.ndarray, values: dict[str, np.ndarray]) -> float:
    """Get the largest decrease after the dose (time 0) against the value at the dose."""
    (x,) = values.values()
    after = time >= 0
    return float(np.min(x[after]) - x[after][0])


#: the extremes of the pharmacodynamics after the dose: id -> function,
#: selection, unit
EXTREMES: dict[
    str, tuple[Callable[[np.ndarray, dict[str, np.ndarray]], float], str, str]
] = {
    "max_NA_EXCRETION": (max_after_dose, "NA_EXCRETION", "mmole/min"),
    "max_CL_EXCRETION": (max_after_dose, "CL_EXCRETION", "mmole/min"),
    "max_diuresis": (max_after_dose, "diuresis", "l/min"),
    "min_bp_systolic": (change_after_dose, "bp_systolic", "mmHg"),
    "min_bp_diastolic": (change_after_dose, "bp_diastolic", "mmHg"),
}

#: the outputs with their ids and names
OUTPUTS: list[SensitivityOutput] = [
    SensitivityOutput("auc_inf_obs", "HCTZ AUC∞"),
    SensitivityOutput("cmax", "HCTZ Cmax"),
    SensitivityOutput("thalf", "HCTZ Half-life"),
    SensitivityOutput("vz_f", "HCTZ Vz/F"),
    SensitivityOutput("cl_f", "HCTZ CL/F"),
    SensitivityOutput("lambda_z", "HCTZ λz"),
    SensitivityOutput("max_NA_EXCRETION", "max Sodium excretion"),
    SensitivityOutput("max_CL_EXCRETION", "max Chloride excretion"),
    SensitivityOutput("max_diuresis", "max diuresis"),
    SensitivityOutput("min_bp_systolic", "change blood pressure systolic"),
    SensitivityOutput("min_bp_diastolic", "change blood pressure diastolic"),
]

#: the observables of a simulation, the outputs with their units
OBSERVABLES = [
    PK(
        PK_ID,
        "[Cve_hctz]",
        dose="PODOSE_hctz",
        route="oral",
        options=NCAOptions(lloq=LLOQ),
        parameters=list(PK_OUTPUTS),
    ),
    *(
        Formula(
            key,
            f"{PK_ID}.{key} / at(Mr_hctz, 0)"
            if key in PK_PER_DOSE_MASS
            else f"{PK_ID}.{key}",
            unit=unit,
        )
        for key, unit in PK_OUTPUTS.items()
    ),
    *(
        Custom(key, function, unit, symbols=[selection])
        for key, (function, selection, unit) in EXTREMES.items()
    ),
]


#: the output times [hr]: every hour of the equilibration, every 0.02 hr in
#: the first day after the dose (absorption and maximum), every 0.5 hr after it
TIMES_HR: tuple[float, ...] = tuple(
    np.unique(
        np.concatenate(
            [
                np.arange(-24 * EQUILIBRATION_DAYS, 0, 1.0),
                np.linspace(0, 24, 1201),
                np.linspace(24, END_HR, 2 * (END_HR - 24) + 1),
            ]
        )
    ).tolist()
)


def sensitivity_simulation(changes: Mapping[str, float]) -> Simulation:
    """Get the simulation of a group: a single oral dose of HCTZ at time 0.

    The simulation starts `EQUILIBRATION_DAYS` before the dose without HCTZ,
    see the module.
    """
    return Simulation(
        start=-24 * EQUILIBRATION_DAYS,
        end=END_HR,
        times=TIMES_HR,
        time_unit="hr",
        preinit_changes={**changes},
        changes=[Change(0, {"PODOSE_hctz": Q(DOSE_HCTZ, "mg")})],
    )


#: the groups the analyses are run for: the control and the stages of renal
#: impairment of the simulation experiments
SENSITIVITY_GROUPS: list[SensitivityGroup] = [
    SensitivityGroup("control", "Control", sensitivity_simulation({}), "dimgrey"),
    *(
        SensitivityGroup(
            uid,
            name,
            sensitivity_simulation(
                {"f_renal_function": HCTZSimulationExperiment.renal_map[name]}
            ),
            HCTZSimulationExperiment.renal_colors[name],
        )
        for uid, name in [
            ("mildRI", "Mild renal impairment"),
            ("modRI", "Moderate renal impairment"),
            ("sevRI", "Severe renal impairment"),
        ]
    ),
]


def sensitivity_parameters() -> list[SensitivityParameter]:
    """Get the parameters of the analyses with their bounds and references."""
    parameters = parameters_from_sbml(
        MODEL_PATH,
        exclude_ids={
            # conversion factors
            "conversion_min_per_day",
            # molecular weights
            "Mr_hctz",
            "Mr_na",
            "Mr_cl",
            "Mr_nacl",
            # reference values
            "BW_ref",
            # unchangeable values
            "FQlu",
            "FVhv",
            "FVpo",
            # dosing parameters
            "PODOSE_hctz",
            "ti_hctz",
            # unused volumes
            "Vurine",
            "Vfeces",
        },
        exclude_na=True,
        exclude_zero=True,
    )

    # the fitted parameters, their bounds are set relative to the value below
    set_bounds(
        parameters,
        [(fp.pid, np.nan, np.nan, ParameterType.FIT) for fp in fit_parameters],
    )
    # the scaling factors of the organ functions
    set_bounds(
        parameters,
        [
            (uid, 1 - BOUNDS_FRACTION, 1 + BOUNDS_FRACTION, ParameterType.SCALING)
            for uid in ["f_cardiac_function", "f_renal_function"]
        ],
    )

    # the references of the values from the literature
    references = {
        "BW": r"\cite{Ogden2004, Jones2013, Thompson2009, Brown1997}",
        "FQgu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FQh": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
        "FQki": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVar": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVgu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVki": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVli": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
        "FVlu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVve": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "COBW": r"\cite{Cattermole2017, Patel2021, Collis2001}",
        "f_renal_function": r"\cite{Stevens2024}",
    }
    by_uid = {p.uid: p for p in parameters}
    for uid, reference in references.items():
        p = by_uid[uid]
        p.reference = reference
        if p.type == ParameterType.NA:
            p.type = ParameterType.DATA

    # every parameter without bounds varies around its value
    set_relative_bounds(parameters, BOUNDS_FRACTION)
    return parameters


#: the analyses of the script, with their groups and numbers of samples
SENSITIVITY = SensitivityRunner(
    model=MODEL,
    parameters=sensitivity_parameters,
    outputs=OUTPUTS,
    observables=OBSERVABLES,
    analyses={
        "local": LocalAnalysis(groups=SENSITIVITY_GROUPS[:1], delta=0.01),
        "sampling": SamplingAnalysis(groups=SENSITIVITY_GROUPS, n=1000),
        "fast": FastAnalysis(groups=SENSITIVITY_GROUPS[:1], n=1000),
        "sobol": SobolAnalysis(groups=SENSITIVITY_GROUPS[:1], n=4096),
    },
    default=("local",),
)


if __name__ == "__main__":
    SENSITIVITY.main()
