"""Sensitivity analysis."""
from __future__ import annotations

import numpy as np
import pandas as pd
import roadrunner
from pint import UnitRegistry
from sbmlutils.console import console

from pkdb_analysis.pk.pharmacokinetics import TimecoursePK

from sbmlsim.sensitivity.analysis import (
    SensitivitySimulation,
    SensitivityOutput,
    AnalysisGroup,
)
from sbmlsim.sensitivity.parameters import (
    SensitivityParameter,
    ParameterType,
)

from pkdb_models.models.hctz import MODEL_PATH
from pkdb_models.models.hctz.fitting.parameters import parameters_all as fit_parameters

# Dose for sensitivity analysis
dose_hctz = 25  # [mg]

# Subgroups to perform sensitivity analysis on
sensitivity_groups: list[AnalysisGroup] = [
    AnalysisGroup(
        uid="control",
        name="Control",
        changes={},
        color="dimgrey",
    ),
    AnalysisGroup(
        uid="mildRI",
        name="Mild renal impairment",
        changes={"f_renal_function": 0.69},
        color="#66c2a4",
    ),
    AnalysisGroup(
        uid="modRI",
        name="Moderate renal impairment",
        changes={"f_renal_function": 0.32},
        color="#2ca25f",
    ),
    AnalysisGroup(
        uid="sevRI",
        name="Severe renal impairment",
        changes={"f_renal_function": 0.19},
        color="#006d2c",
    ),
]


class HCTZSensitivitySimulation(SensitivitySimulation):
    """Simulation for sensitivity calculation."""
    tend = 5 * 24 * 60  # [min]
    steps = 10000

    def simulate(self, r: roadrunner.RoadRunner, changes: dict[str, float]) -> dict[str, float]:

        # apply changes and simulate
        all_changes = {
            **self.changes_simulation,  # model
            **changes  # sensitivity
        }
        self.apply_changes(r, all_changes, reset_all=True)
        # ensure tolerances
        r.integrator.setValue("absolute_tolerance", self.init_tolerances)
        s = r.simulate(start=0, end=self.tend, steps=self.steps)

        # pharmacokinetic parameters
        y: dict[str, float] = {}

        # pharmacokinetics
        ureg = UnitRegistry()
        Q_ = ureg.Quantity

        # losartan
        Mr_hctz = Q_(297.7, "g/mole")
        time = Q_(s["time"], "min")
        tcpk = TimecoursePK(
            time=time,
            concentration=Q_(s["[Cve_hctz]"], "mM"),
            substance="hctz",
            ureg=ureg,
            dose=Q_(dose_hctz, "mg")/Mr_hctz,
        )
        pk_dict = tcpk.pk.to_dict()
        # console.print(pk_dict)
        for pk_key in [
            "aucinf",
            "cmax",
            "thalf",
            "vd",
            "cl",
            "kel",
        ]:
            y[pk_key] = pk_dict[pk_key]

        # pharmacodynamics
        y["max_NA_EXCRETION"] = np.max(s["NA_EXCRETION"])
        y["max_CL_EXCRETION"] = np.max(s["CL_EXCRETION"])
        y["max_diuresis"] = np.max(s["diuresis"])
        y["min_bp_systolic"] = np.min(s["bp_systolic"])
        y["min_bp_diastolic"] = np.min(s["bp_diastolic"])

        return y


sensitivity_simulation = HCTZSensitivitySimulation(
    model_path=MODEL_PATH,
    selections=[
        "time",
        "[Cve_hctz]",
        "NA_EXCRETION",
        "CL_EXCRETION",
        "diuresis",
        "bp_systolic",
        "bp_diastolic",
    ],
    changes_simulation = {
        # ! make sure all the changes from base-experiment are injected here !
        "PODOSE_hctz": dose_hctz,  # [mg]
        # "f_cirrhosis": 0,  # [-]
        # "f_renal_function": 1.0,  # [-]
    },
    outputs=[
        # FIXME: auto-calculate units
        SensitivityOutput(uid='aucinf', name='HCTZ AUC∞', unit="mM*min"),
        SensitivityOutput(uid='cmax', name='HCTZ Cmax', unit="mM"),
        SensitivityOutput(uid='thalf', name='HCTZ Half-life', unit="min"),
        SensitivityOutput(uid='vd', name='HCTZ Vd', unit="l"),
        SensitivityOutput(uid='cl', name='HCTZ CL', unit="mole/min/mM"),
        SensitivityOutput(uid='kel', name='HCTZ kel', unit="1/min"),

        SensitivityOutput(uid='max_NA_EXCRETION', name='max Sodium excretion', unit="mmole/min"),
        SensitivityOutput(uid='max_CL_EXCRETION', name='max Chloride excretion', unit="mmole/min"),
        SensitivityOutput(uid='max_diuresis', name='max diuresis', unit="l/min"),
        SensitivityOutput(uid='min_bp_systolic', name='blood pressure systolic', unit="mmHg"),
        SensitivityOutput(uid='min_bp_diastolic', name='blood pressure diastolic', unit="mmHg"),
    ]
)


def _sensitivity_parameters() -> list[SensitivityParameter]:
    """Definition of parameters and bounds for sensitivity analysis."""
    console.rule("Parameters", style="white")
    parameters: list[SensitivityParameter] = SensitivityParameter.parameters_from_sbml(
        sbml_path=MODEL_PATH,
        exclude_ids={
            # conversion factors
            "conversion_min_per_day",
            # "KI__cf_mg_per_g",
            # "KI__cf_ml_per_l",

            # molecular weights
            "Mr_hctz",
            "Mr_na",
            "Mr_cl",
            "Mr_nacl"

            # unchangable values
            "FQlu",
            "FVhv",
            "FVpo",
            "GFR_healthy",

            # dosing parameters
            "PODOSE_hctz",
            "ti_hctz",

            # unused volumes
            "Vurine",
            "KI__urine_volume",
            "Vfeces",
            "Vplasma",
            "Vstomach",
        },
        exclude_na=True,
        exclude_zero=True,
    )
    bounds_fraction = 0.15  # fraction of bounds relative to value

    # bounds from fitted parameters
    fit_bounds = [
        # (fp.pid, fp.lower_bound, fp.upper_bound, ParameterType.FIT) for fp in fit_parameters
        (fp.pid, np.nan, np.nan, ParameterType.FIT) for fp in fit_parameters
    ]
    SensitivityParameter.parameters_set_bounds(parameters, bounds=fit_bounds)

    # bounds from scaled parameters
    uids_scaling = [
        "f_cardiac_function",
        "f_renal_function",
    ]
    scaling_bounds = [
        (uid, 1 - bounds_fraction, 1 + bounds_fraction, ParameterType.SCALING) for uid in uids_scaling
    ]
    SensitivityParameter.parameters_set_bounds(parameters, bounds=scaling_bounds)

    # references for values
    reference_data={
        "HCT": r"\cite{Mondal2025, Fiseha2023}",
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
        # "LI__f_cyp2c9": r"\cite{Kusama2009, Wang2014, Maekawa2009}",
    }
    p_dict = {p.uid: p for p in parameters}
    for pid, reference in reference_data.items():
        p = p_dict[pid]
        p.reference = reference
        if p.type == ParameterType.NA:
            p.type = ParameterType.DATA

    # setting missing bounds;
    for p in parameters:
        if np.isnan(p.lower_bound) and np.isnan(p.upper_bound):
            p.lower_bound = p.value * (1 - bounds_fraction)
            p.upper_bound = p.value * (1 + bounds_fraction)

    # print parameters
    pd.options.display.float_format = "{:.5g}".format
    df_parameters = SensitivityParameter.parameters_to_df(parameters)
    console.print(df_parameters)

    return parameters

sensitivity_parameters = _sensitivity_parameters()


if __name__ == "__main__":
    import multiprocessing
    from sbmlsim.sensitivity import (
        LocalSensitivityAnalysis,
        SamplingSensitivityAnalysis,
        FASTSensitivityAnalysis,
        SobolSensitivityAnalysis,
    )
    from pkdb_models.models.hctz import RESULTS_PATH

    sensitivity_path = RESULTS_PATH / "sensitivity"
    sensitivity_path.mkdir(parents=True, exist_ok=True)
    df_parameters = SensitivityParameter.parameters_to_df(sensitivity_parameters)
    df_parameters.to_csv(sensitivity_path / "parameters.tsv", sep="\t", index=False)
    console.print(df_parameters)
    SensitivityParameter.parameter_to_latex(
        tex_path=sensitivity_path / "parameters.tex",
        parameters=sensitivity_parameters,
    )

    settings = {
        "cache_results": False,
        "n_cores": int(round(0.9 * multiprocessing.cpu_count())),
        "seed": 1234
    }

    sa_local = LocalSensitivityAnalysis(
        sensitivity_simulation=sensitivity_simulation,
        parameters=sensitivity_parameters,
        groups=[sensitivity_groups[0]],
        results_path=sensitivity_path / "local",
        difference=0.01,
        **settings,
    )
    sa_sampling = SamplingSensitivityAnalysis(
        sensitivity_simulation=sensitivity_simulation,
        parameters=sensitivity_parameters,
        groups=sensitivity_groups,
        results_path=sensitivity_path / "sampling",
        N=1000,
        **settings,
    )
    # sa_fast = FASTSensitivityAnalysis(
    #     sensitivity_simulation=sensitivity_simulation,
    #     parameters=sensitivity_parameters,
    #     groups=[sensitivity_groups[0]],
    #     results_path=sensitivity_path / "fast",
    #     N=1000,
    #     **settings,
    # )
    # sa_sobol = SobolSensitivityAnalysis(
    #     sensitivity_simulation=sensitivity_simulation,
    #     parameters=sensitivity_parameters,
    #     groups=[sensitivity_groups[0]],
    #     results_path=sensitivity_path / "sobol",
    #     N=4096,
    #     **settings,
    # )
    for sa in [
        sa_local,
        # sa_sampling,
        # sa_fast,
        # sa_sobol,
    ]:
        sa.execute()
        sa.plot()
