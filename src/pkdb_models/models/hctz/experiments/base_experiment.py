"""Base class of the HCTZ simulation experiments."""

import math
from collections.abc import Iterable, Mapping, Sequence
from typing import Any, ClassVar, overload, override

import pandas as pd
from pkpdsim import impairment
from pkpdsim.pbpk import PBPKSimulationExperiment, ScaledRenalMap, molecular_weights
from sbmlsim import Q
from sbmlsim.result.scan import start_values
from sbmlsim.simulation import Scan, Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.hctz import MODEL
from pkdb_models.models.hctz.hctz_pk import (
    calculate_hctz_pd,
    calculate_hctz_pk,
)
from pkdb_models.models.hctz.models.definition import DEFINITION


class HCTZSimulationExperiment(PBPKSimulationExperiment):
    """Base class of the HCTZ simulation experiments."""

    pkpd_model = MODEL
    selections = (
        "time",
        # pharmacokinetics
        "IVDOSE_hctz",
        "PODOSE_hctz",
        "Carm_hctz",
        "Afeces_hctz",  # cumulative amount of hctz in feces
        "Rurine_hctz",  # urinary excretion rate
        "Aurine_hctz",  # cumulative amount of hctz in urine
        "FLUID__hctz_urine_excretion",  # concentration of hctz in the urine formed at the time
        # Urine volume & ion balance
        "FLUID__NA_EXCRETION",  # mmole/hr [mmole/min]
        "FLUID__CL_EXCRETION",  # mmole/hr [mmole/min]
        "FLUID__NA_FILTRATION",  # mmole/hr [mmole/min]
        "FLUID__CL_FILTRATION",  # mmole/hr [mmole/min]
        "FLUID__NA_REABSORPTION",  # mmole/hr [mmole/min]
        "FLUID__CL_REABSORPTION",  # mmole/hr [mmole/min]
        "FLUID__diuresis",  # ml/hr [l/min]
        "FLUID__Vurine",  # urine volume
        "FLUID__na_urine",  # sodium urine
        "FLUID__cl_urine",  # chloride urine
        "[FLUID__na]",  # sodium ECF
        "[FLUID__cl]",  # chloride ECF
        "FLUID__ECF",
        "FLUID__vin_na",
        "FLUID__vin_cl",
        "FLUID__NA_UPTAKE",
        "FLUID__CL_UPTAKE",
        "FLUID__vin_h2o",
        "FLUID__H2O_UPTAKE",
        "FLUID__h2o_reabsorption",
        "FLUID__bp_systolic",  # blood pressure systolic
        "FLUID__bp_diastolic",  # blood pressure diastolic
        "FLUID__bp_mean",  # mean arterial pressure
        # parameter scans
        "PODOSE_hctz",
        "f_renal_function",
        "CP_severity",
        "HF_severity",
    )

    font: ClassVar[dict[str, Any]] = {"weight": "bold", "size": 22}
    scan_font: ClassVar[dict[str, Any]] = {"weight": "bold", "size": 15}
    tick_font_size = 15
    legend_font_size = 13
    suptitle_font_size = 40

    unit_time = "hr"
    unit_hctz = "µM"
    unit_hctz_urine = "µmol"
    unit_hctz_feces = "µmol"
    unit_hctz_excretion_urine = "nmol/min"

    unit_urine_volume = "ml"
    unit_na = "mM"
    unit_cl = "mM"
    unit_na_urine = "mmole"
    unit_cl_urine = "mmole"

    units: ClassVar[Mapping[str, str]] = {
        "time": "hr",
        "Carm_hctz": unit_hctz,
        "Aurine_hctz": unit_hctz_urine,
        "Afeces_hctz": unit_hctz_feces,
        "Rurine_hctz": unit_hctz_excretion_urine,
        "FLUID__bp_systolic": "mmHg",
        "FLUID__bp_diastolic": "mmHg",
        "FLUID__bp_mean": "mmHg",
        "FLUID__Vurine": unit_urine_volume,
        "FLUID__NA_EXCRETION": "mmole/hr",
        "FLUID__CL_EXCRETION": "mmole/hr",
        "FLUID__vin_na": "mmole/hr",
        "FLUID__vin_cl": "mmole/hr",
        "FLUID__NA_UPTAKE": "mmole/hr",
        "FLUID__CL_UPTAKE": "mmole/hr",
        "FLUID__NA_FILTRATION": "mmole/hr",
        "FLUID__CL_FILTRATION": "mmole/hr",
        "FLUID__NA_REABSORPTION": "mmole/hr",
        "FLUID__CL_REABSORPTION": "mmole/hr",
        "FLUID__diuresis": "ml/hr",
        "FLUID__vin_h2o": "ml/hr",
        "FLUID__H2O_UPTAKE": "ml/hr",
        "FLUID__h2o_reabsorption": "ml/hr",
        "FLUID__ECF": "l",
        "[FLUID__na]": unit_na,
        "[FLUID__cl]": unit_cl,
        "FLUID__na_urine": unit_na_urine,
        "FLUID__cl_urine": unit_cl_urine,
    }

    label_time = "time"
    label_hctz = "HCTZ"
    label_hctz_urine = "HCTZ urine\n"
    label_hctz_feces = "HCTZ feces\n"
    label_hctz_excretion_urine = "HCTZ excretion\nurine"

    label_urine_volume = "Urine volume"
    label_na = "Sodium ECF"
    label_cl = "Chloride ECF"
    label_na_urine = "Sodium urine"
    label_cl_urine = "Chloride urine"

    labels: ClassVar[Mapping[str, str]] = {
        "time": label_time,
        "Carm_hctz": label_hctz,
        "Aurine_hctz": label_hctz_urine,
        "Afeces_hctz": label_hctz_feces,
        "Rurine_hctz": label_hctz_excretion_urine,
        "FLUID__bp_systolic": "blood pressure systolic\n",
        "FLUID__bp_diastolic": "blood pressure diastolic\n",
        "FLUID__bp_mean": "mean arterial pressure\n",
        "FLUID__Vurine": label_urine_volume,
        "FLUID__NA_EXCRETION": "Sodium excretion\n",
        "FLUID__CL_EXCRETION": "Chloride excretion\n",
        "FLUID__vin_na": "Na uptake baseline",
        "FLUID__vin_cl": "Cl uptake baseline",
        "FLUID__NA_UPTAKE": "Na uptake",
        "FLUID__CL_UPTAKE": "Cl uptake",
        "FLUID__NA_FILTRATION": "Na filtration",
        "FLUID__CL_FILTRATION": "Cl filtration",
        "FLUID__NA_REABSORPTION": "Na reabsorption",
        "FLUID__CL_REABSORPTION": "Cl reabsorption",
        "FLUID__vin_h2o": "H2O uptake baseline",
        "FLUID__H2O_UPTAKE": "H2O uptake",
        "FLUID__h2o_reabsorption": "H2O reabsorption",
        "FLUID__diuresis": "diuresis",
        "FLUID__ECF": "Extracellular fluid",
        "[FLUID__na]": label_na,
        "[FLUID__cl]": label_cl,
        "FLUID__na_urine": label_na_urine,
        "FLUID__cl_urine": label_cl_urine,
    }

    color_hctz = "black"
    color_hctz_urine = "black"

    #: the molecular weights of the conversion of the data, of the definition:
    #: hydrochlorothiazide (`Mr_hctz`) and renin (`Mr_ren`, Giudicelli1987)
    Mr: ClassVar[Mapping[str, Quantity]] = molecular_weights(DEFINITION)

    renal_colors: ClassVar[Mapping[str, str]] = {
        "Control": "black",
        "Normal renal function": "black",
        "Mild renal impairment": "#66c2a4",
        "Moderate renal impairment": "#2ca25f",
        "Severe renal impairment": "#006d2c",
    }

    @override
    def load_dataframe(
        self,
        fig_id: str,
        study: str | None = None,
        *,
        na_values: Sequence[str] | Mapping[str, Sequence[str]] | None = None,
    ) -> pd.DataFrame:
        """Load the digitized data of a figure or table, without the zero points.

        A point of value 0 at the time 0 (the dose, the start of a urine
        collection, a net change against the baseline) holds no information:
        the model starts there with 0 as well. In a fit it still counts in
        the number of points of its curve and lowers the mean of the curve,
        by which the residuals are normalized, and so raised the weight of
        the curve by n/(n - zeros). The points are left out.
        """
        df = super().load_dataframe(fig_id, study, na_values=na_values)
        return without_zero_start(df)

    def group_counts(self) -> dict[str, int]:
        """Get the number of subjects of every group of the study (TabGroups).

        The points of a scatter of pkdb_data have the count 1, also where a
        point is the mean of a group.
        """
        df = self.load_dataframe("TabGroups")
        return {
            str(k): int(v) for k, v in zip(df["name"], df["group_count"], strict=True)
        }

    #: the urine of a collection: what is emptied at its end, see
    #: `collected_amounts`
    urine_reset: ClassVar[dict[str, Quantity]] = {
        "Aurine_hctz": Q(0, "mmole"),
        "FLUID__Vurine": Q(1e-6, "l"),
        "FLUID__na_urine": Q(0, "mmole"),
        "FLUID__cl_urine": Q(0, "mmole"),
    }

    @overload
    def equilibrated_all(
        self, simulations: Mapping[str, Simulation]
    ) -> dict[str, Simulation]: ...

    @overload
    def equilibrated_all(self, simulations: Mapping[str, Scan]) -> dict[str, Scan]: ...

    @overload
    def equilibrated_all(
        self, simulations: Mapping[str, Simulation | Scan]
    ) -> dict[str, Simulation | Scan]: ...

    def equilibrated_all(
        self, simulations: Mapping[str, Simulation | Scan]
    ) -> dict[str, Simulation] | dict[str, Scan] | dict[str, Simulation | Scan]:
        """Get the simulations, each starting from the drug-free steady state of its condition.

        The start of the model is the steady state of the healthy reference
        individual without the fluid PD: without HCTZ the extracellular fluid,
        the electrolytes and the pressures drift (in renal impairment by days
        to a new steady state), which a study measures as the basal state of
        its subjects. Every simulation equilibrates its condition first
        (`equilibrated`, every point of a scan in its own), the urine of the
        fluid PD, which grows without a steady state, is emptied at the start
        (`urine_reset`).
        """
        equilibrated: dict[str, Simulation | Scan] = {}
        for key, simulation in simulations.items():
            equilibrated[key] = self.equilibrated(simulation, resets=self.urine_reset)
        return equilibrated

    @staticmethod
    def collected_amounts(
        df: pd.DataFrame, intervals: Sequence[tuple[float, float]]
    ) -> pd.DataFrame:
        """Get the amounts of urine collections from their excretion rates.

        A rate of a collection is its amount divided by its duration. The
        model has the instantaneous rate, which differs from the rate of a
        collection, so a fit compares the amount of every collection with the
        urine of a simulation which empties the urine at the end of every
        collection (`urine_reset`): a data point at the end of a collection
        is compared with the urine before the reset. The time of a collection
        is its end; a curve has no point of 0 at its start, which would hold
        no information (see `load_dataframe`).

        Args:
            df: the rates of one curve, a rate per hour or minute in `unit`,
                the time in hours; the rows without a value are left out.
            intervals: the start and the end of the collection of every row
                with a value, in the order of the times of the rows [hr].

        Returns:
            The amounts of the collections, with `tstart` and `tend`.
        """
        values = [c for c in ["mean", "value"] if c in df and df[c].notna().any()]
        if len(values) != 1:
            raise ValueError(f"A curve has one column of values, not {values}.")
        df = df[df[values[0]].notna()].sort_values("time").copy()
        if len(df) != len(intervals):
            raise ValueError(
                f"{len(df)} rates, but {len(intervals)} collection intervals."
            )
        unit = str(df["unit"].iloc[0])
        per_hour = {"/hr": 1.0, "/h": 1.0, "/min": 60.0}
        suffix = next((s for s in per_hour if unit.endswith(s)), None)
        if suffix is None or (df["unit"] != unit).any():
            raise ValueError(f"The rates of a curve are in one rate unit: {unit}.")
        df["tstart"] = [start for start, _ in intervals]
        df["tend"] = [end for _, end in intervals]
        factor = (df["tend"] - df["tstart"]) * per_hour[suffix]
        for column in [values[0], "sd", "se"]:
            if column in df:
                df[column] = df[column] * factor
        df["time"] = df["tend"]
        df["unit"] = unit.removesuffix(suffix)
        df["measurement_type"] = "amount of the collection"
        return df.reset_index(drop=True)

    #: the lower end of the supported renal function of the model: without
    #: filtration the excretion of sodium and chloride goes on without urine
    #: and the urinary concentration of HCTZ is not defined (anuria is not
    #: supported); the upper end is the validity of the kidney outflow of the
    #: library (`renal_function_limits`)
    renal_function_range: ClassVar[tuple[float, float] | None] = (0.05, math.inf)

    #: the classes of renal impairment by their GFR in ml/min (the midpoints of
    #: `impairment.RENAL_FUNCTION`), relative to the healthy GFR of the model
    renal_map: ClassVar[Mapping[str, float]] = ScaledRenalMap(impairment.RENAL_FUNCTION)
    #: the classes of heart failure of the studies as the severity
    #: `HF_severity`: mild, moderate and severe are the NYHA classes II to IV
    cardiac_map: ClassVar[Mapping[str, float]] = {
        "Normal cardiac function": 0,
        "Mild cardiac impairment": 2,
        "Moderate cardiac impairment": 3,
        "Severe cardiac impairment": 4,
    }
    cardiac_colors: ClassVar[Mapping[str, str]] = {
        "Normal cardiac function": impairment.HEART_FAILURE_COLORS[
            "Normal cardiac function"
        ],
        "Mild cardiac impairment": impairment.HEART_FAILURE_COLORS["NYHA II"],
        "Moderate cardiac impairment": impairment.HEART_FAILURE_COLORS["NYHA III"],
        "Severe cardiac impairment": impairment.HEART_FAILURE_COLORS["NYHA IV"],
    }

    # --- Pharmacokinetic parameters ---
    # keys are the parameters of the non-compartmental analysis of pkpdutils,
    # see `hctz_pk.pk_parameters`
    pk_labels: ClassVar[Mapping[str, str]] = {
        "auc_last": "AUCend",
        "auc_inf_obs": "AUC",
        "cl_f": "Apparent clearance",
        "cl_renal": "Renal clearance",
        "cl_sys": "Systemic clearance",
        "fe_urine": "Fraction of the dose in the urine",
        "fe_feces": "Fraction of the dose in the feces (not absorbed)",
        "f_remaining": "Fraction of the dose in the body",
        "cmax": "Cmax",
        "thalf": "Half-life",
        "lambda_z": "Elimination rate",
        "vz_f": "Apparent volume",
    }

    pk_units: ClassVar[Mapping[str, str]] = {
        "auc_last": "µmole/l*hr",
        "auc_inf_obs": "µmole/l*hr",
        "cl_f": "ml/min",
        "cl_renal": "ml/min",
        "cl_sys": "ml/min",
        "fe_urine": "dimensionless",
        "fe_feces": "dimensionless",
        "f_remaining": "dimensionless",
        "cmax": "µmole/l",
        "thalf": "hr",
        "lambda_z": "1/hr",
        "vz_f": "l",
    }

    def calculate_hctz_pk(
        self, scans: Iterable[str] | None = None
    ) -> dict[str, pd.DataFrame]:
        """Calculate the pharmacokinetic parameters of the scans.

        Args:
            scans: keys of the simulations, all simulations by default. A scan
                without a dose (the placebo) has no pharmacokinetics.

        Returns:
            The parameters of every scan by simulation key, per draw of the
            fitted parameters in a run over them (`uncertainty`).
        """
        keys = self._simulations if scans is None else scans
        across = self.across()
        return {
            key: calculate_hctz_pk(
                experiment=self, res=self.results[f"task_{key}"], across=across
            )
            for key in keys
            if float(start_values(self.results[f"task_{key}"], "PODOSE_hctz").max()) > 0
        }

    def calculate_hctz_pd(
        self, scans: Iterable[str] | None = None
    ) -> dict[str, dict[str, pd.DataFrame]]:
        """Calculate the pharmacodynamic parameters of the scans.

        Args:
            scans: keys of the simulations, all simulations by default.

        Returns:
            The parameters of every scan by simulation key, per draw of the
            fitted parameters in a run over them (`uncertainty`).
        """
        keys = self._simulations if scans is None else scans
        across = self.across()
        return {
            key: calculate_hctz_pd(res=self.results[f"task_{key}"], across=across)
            for key in keys
        }


def without_zero_start(df: pd.DataFrame) -> pd.DataFrame:
    """Get the data without the points of value 0 at the time 0.

    A point counts as zero if its value (`mean` or `value`) is 0; points
    without a time (e.g. a scatter over another variable) are kept.
    """
    if "time" not in df:
        return df
    zero = pd.Series(False, index=df.index)
    for column in ["mean", "value"]:
        if column in df:
            zero |= pd.to_numeric(df[column], errors="coerce").eq(0)
    start = pd.to_numeric(df["time"], errors="coerce").eq(0)
    return df[~(zero & start)].reset_index(drop=True)


def ecf_expansion(f_renal_function: float) -> float:
    """Get the extracellular fluid of the steady state of a renal function.

    The steady state without HCTZ, relative to `ECF_ref`: the water uptake
    `vin_h2o * x^-g` equals the urine `(vin_h2o - vout_h2o) * f * x^g` and the
    water lost without urine `vout_h2o`, with `x = ECF/ECF_ref`, the renal
    function `f` and `g = counter_gamma` (5), at a plasma sodium of `na_ref`.

    Args:
        f_renal_function: the renal function, the GFR relative to the healthy.

    Returns:
        `ECF/ECF_ref` of the steady state.
    """
    from pkdb_models.models.hctz.models.model_fluid import vin_h2o, vout_h2o

    gamma = 5.0

    def balance(x: float) -> float:
        urine = (vin_h2o - vout_h2o) * f_renal_function * x**gamma
        return vin_h2o * x**-gamma - urine - vout_h2o

    # the balance falls with x, it is positive at 0.5 and negative at 3
    low, high = 0.5, 3.0
    for _ in range(100):
        mid = (low + high) / 2
        if balance(mid) > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2
