"""Sensitivity analysis of the HCTZ model.

The outputs are the pharmacokinetic parameters of a single oral dose (the
non-compartmental analysis of `pkpdutils`) and the extremes of the
pharmacodynamics. The parameters are a list (`PARAMETER_IDS`): the
covariates and the impairments of the individual, the fitted parameters, the
activities of OAT1 and MRP4 and the reference physiology of the library,
with bounds of +-15 % around their value (a severity, 0 in the healthy
individual, from 0 to 15 % of its scale). A model of the library has
hundreds of parameters, most of them initial assignments of the covariates,
which an analysis of all constant parameters would vary as well. The
analyses are run as a script, the local analysis by default:

    python -m pkdb_models.models.hctz.sensitivity.sensitivity_analysis
    python -m pkdb_models.models.hctz.sensitivity.sensitivity_analysis local sampling

The analyses run on `sbmlsim.sensitivity.runner.SensitivityRunner`, which writes the
table of the parameters into `results/sensitivity` of the model and the tables
and figures of an analysis into `results/sensitivity/<analysis>`.
An analysis does not vary a parameter which one of its groups sets
(`pkpdsim.sensitivity.free_parameters`): `sampling`, over the four groups, leaves
out `f_renal_function`. The environment variable `PKPDSIM_SENSITIVITY_N`
replaces the numbers of samples of the global analyses for a quick run, see
`pkpdsim.sensitivity.sample_size`.

Every point of a design starts from the drug-free steady state of its
condition, the equilibration of the library which the simulation experiments
use as well (`pkpdsim.pbpk.Equilibration`, the `prepare` of every group; the
urine of the fluid PD, which grows without a steady state, is emptied at the
start, `HCTZSimulationExperiment.urine_reset`): in impaired renal function the
model without HCTZ is not stationary, the extracellular fluid and with it the
blood pressure rise to a new steady state ((ECF/ECF_ref)^10 =
1/f_renal_function; 120 to 141 mmHg in severe renal impairment), which an
analysis from the reference state would attribute to HCTZ, and a parameter
which moves the basal state (the renal function, a parameter of the PD) moves
it at every point. So the change of the pressure against its value at the
dose is the effect of HCTZ (`min_bp_systolic`, `min_bp_diastolic`). The dose
is given at the start (time 0) and followed for `END_HR` hours, long enough
for the non-compartmental analysis of severe renal impairment (0.04 % of the
maximal concentration at the end).
"""

from collections.abc import Callable, Mapping

import numpy as np
from pkpdsim.pbpk import Equilibration
from pkpdsim.sensitivity import NonzeroLocalAnalysis, library_parameters, max_after_dose
from pkpdutils import NCAOptions
from sbmlsim import Q
from sbmlsim.sensitivity.parameters import SensitivityParameter
from sbmlsim.sensitivity.runner import (
    FastAnalysis,
    SamplingAnalysis,
    SensitivityGroup,
    SensitivityOutput,
    SensitivityRunner,
    SobolAnalysis,
)
from sbmlsim.simulation import PK, Change, Custom, Formula, Simulation

from pkdb_models.models.hctz import MODEL, MODEL_PATH
from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)
from pkdb_models.models.hctz.fitting.parameters import parameters_all as fit_parameters

#: oral dose of the analysis [mg]
DOSE_HCTZ = 25
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
    "max_NA_EXCRETION": (max_after_dose, "FLUID__NA_EXCRETION", "mmole/min"),
    "max_CL_EXCRETION": (max_after_dose, "FLUID__CL_EXCRETION", "mmole/min"),
    "max_diuresis": (max_after_dose, "FLUID__diuresis", "l/min"),
    "min_bp_systolic": (change_after_dose, "FLUID__bp_systolic", "mmHg"),
    "min_bp_diastolic": (change_after_dose, "FLUID__bp_diastolic", "mmHg"),
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
        "Carm_hctz",
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


#: the output times [hr]: every 0.02 hr in the first day after the dose
#: (absorption and maximum), every 0.5 hr after it; a grid, since the
#: extremes and the non-compartmental analysis of every point of a design
#: read the same times
TIMES_HR: tuple[float, ...] = tuple(
    np.unique(
        np.concatenate(
            [
                np.linspace(0, 24, 1201),
                np.linspace(24, END_HR, 2 * (END_HR - 24) + 1),
            ]
        )
    ).tolist()
)

#: the equilibration of every point of a design: the drug-free steady state of
#: its condition, the urine of the fluid PD emptied at the start
EQUILIBRATION = Equilibration(resets=HCTZSimulationExperiment.urine_reset)


def sensitivity_simulation(changes: Mapping[str, float]) -> Simulation:
    """Get the simulation of a group: a single oral dose of HCTZ at time 0.

    The simulation starts at the dose; its group equilibrates it
    (`EQUILIBRATION`), see the module.
    """
    return Simulation(
        start=0,
        end=END_HR,
        times=TIMES_HR,
        time_unit="hr",
        preinit_changes={**changes},
        changes=[Change(0, {"PODOSE_hctz": Q(DOSE_HCTZ, "mg")})],
    )


#: the groups the analyses are run for: the control and the stages of renal
#: impairment of the simulation experiments
SENSITIVITY_GROUPS: list[SensitivityGroup] = [
    SensitivityGroup(
        "control",
        "Control",
        sensitivity_simulation({}),
        "dimgrey",
        prepare=EQUILIBRATION,
    ),
    *(
        SensitivityGroup(
            uid,
            name,
            sensitivity_simulation(
                {"f_renal_function": HCTZSimulationExperiment.renal_map[name]}
            ),
            HCTZSimulationExperiment.renal_colors[name],
            prepare=EQUILIBRATION,
        )
        for uid, name in [
            ("mildRI", "Mild renal impairment"),
            ("modRI", "Moderate renal impairment"),
            ("sevRI", "Severe renal impairment"),
        ]
    ),
]


#: the parameters of the analyses: the covariates and the impairments of the
#: individual, the fitted parameters, the activities of OAT1 and MRP4 (the
#: tubular secretion) and the reference physiology of the library
PARAMETER_IDS: tuple[str, ...] = (
    "BW",
    "HEIGHT",
    "f_renal_function",
    "CP_severity",
    "HF_severity",
    "f_cardiac_function",
    *(fp.pid for fp in fit_parameters),
    "KI__f_slc22a6",
    "KI__f_abcc4",
    "HCT_ref",
    "CO_ref",
    "GFR_ref",
)

#: the source of the classes of the renal function (the stages of chronic
#: kidney disease by the GFR), in the form of the sources of the library
STEVENS2024 = (
    "Stevens PE, Ahmed SB, Carrero JJ, et al. (KDIGO CKD Work Group). KDIGO "
    "2024 Clinical Practice Guideline for the Evaluation and Management of "
    "Chronic Kidney Disease. Kidney Int 105(4S), S117-S314, 2024. "
    "doi:10.1016/j.kint.2023.10.018"
)

#: the factors of the organ functions and of the activities of the proteins, 1
#: in the healthy individual
SCALING_IDS: tuple[str, ...] = (
    "f_cardiac_function",
    "f_renal_function",
    "KI__f_slc22a6",
    "KI__f_abcc4",
)


def sensitivity_parameters() -> list[SensitivityParameter]:
    """Get the parameters of the analyses with their bounds and references.

    The parameters of `PARAMETER_IDS` (`pkpdsim.sensitivity.library_parameters`):
    the fitted parameters, the scaling factors (`SCALING_IDS`) and the
    severities with their bounds, the references of their notes and the
    guideline of the classes of the renal function, whose notes give no source.
    """
    return library_parameters(
        MODEL_PATH,
        PARAMETER_IDS,
        fit_ids=[fp.pid for fp in fit_parameters],
        scaling_ids=SCALING_IDS,
        references={"f_renal_function": STEVENS2024},
        relative=BOUNDS_FRACTION,
    )


#: the analyses of the script, with their groups and numbers of samples
SENSITIVITY = SensitivityRunner(
    project=MODEL,
    out=MODEL.results_dir / "sensitivity",
    parameters=sensitivity_parameters,
    outputs=OUTPUTS,
    observables=OBSERVABLES,
    analyses={
        "local": NonzeroLocalAnalysis(groups=SENSITIVITY_GROUPS[:1], delta=0.01),
        "sampling": SamplingAnalysis(groups=SENSITIVITY_GROUPS, n=1000),
        "fast": FastAnalysis(groups=SENSITIVITY_GROUPS[:1], n=1000),
        "sobol": SobolAnalysis(groups=SENSITIVITY_GROUPS[:1], n=4096),
    },
    default=("local",),
)


if __name__ == "__main__":
    SENSITIVITY.main()
