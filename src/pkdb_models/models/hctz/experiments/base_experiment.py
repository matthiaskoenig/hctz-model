"""Base class of the HCTZ simulation experiments."""

from collections.abc import Iterable, Mapping, Sequence
from typing import Any, ClassVar, NamedTuple, override

import pandas as pd
from pkpdsim.experiment import PKPDSimulationExperiment
from sbmlsim import Q
from sbmlsim.units import Quantity

from pkdb_models.models.hctz import MODEL
from pkdb_models.models.hctz.hctz_pk import (
    calculate_hctz_pd,
    calculate_hctz_pk,
)


class MolecularWeights(NamedTuple):
    """Molecular weights for the conversion of the data."""

    hctz: Quantity
    ren: Quantity


class HCTZSimulationExperiment(PKPDSimulationExperiment):
    """Base class of the HCTZ simulation experiments."""

    pkpd_model = MODEL
    selections = (
        "time",
        # pharmacokinetics
        "IVDOSE_hctz",
        "PODOSE_hctz",
        "[Cve_hctz]",
        "Afeces_hctz",  # cumulative amount of hctz in feces
        "KI__HCTZEX",  # urinary excretion rate
        "Aurine_hctz",  # cumulative amount of hctz in urine
        "hctz_urine_excretion",  # concentration of hctz in the urine formed at the time
        # Urine volume & ion balance
        "NA_EXCRETION",  # mmole/hr [mmole/min]
        "CL_EXCRETION",  # mmole/hr [mmole/min]
        "NA_FILTRATION",  # mmole/hr [mmole/min]
        "CL_FILTRATION",  # mmole/hr [mmole/min]
        "NA_REABSORPTION",  # mmole/hr [mmole/min]
        "CL_REABSORPTION",  # mmole/hr [mmole/min]
        "diuresis",  # ml/hr [l/min]
        "Vurine",  # urine volume
        "na_urine",  # sodium urine
        "cl_urine",  # chloride urine
        "[na]",  # sodium ECF
        "[cl]",  # chloride ECF
        "ECF",
        "vin_na",
        "vin_cl",
        "NA_UPTAKE",
        "CL_UPTAKE",
        "vin_h2o",
        "H2O_UPTAKE",
        "h2o_reabsorption",
        "bp_systolic",  # blood pressure systolic
        "bp_diastolic",  # blood pressure diastolic
        "bp_mean",  # mean arterial pressure
        # parameter scans
        "PODOSE_hctz",
        "f_renal_function",
        "f_cirrhosis",
        "f_cardiac_function",
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
        "[Cve_hctz]": unit_hctz,
        "Aurine_hctz": unit_hctz_urine,
        "Afeces_hctz": unit_hctz_feces,
        "KI__HCTZEX": unit_hctz_excretion_urine,
        "bp_systolic": "mmHg",
        "bp_diastolic": "mmHg",
        "bp_mean": "mmHg",
        "Vurine": unit_urine_volume,
        "NA_EXCRETION": "mmole/hr",
        "CL_EXCRETION": "mmole/hr",
        "vin_na": "mmole/hr",
        "vin_cl": "mmole/hr",
        "NA_UPTAKE": "mmole/hr",
        "CL_UPTAKE": "mmole/hr",
        "NA_FILTRATION": "mmole/hr",
        "CL_FILTRATION": "mmole/hr",
        "NA_REABSORPTION": "mmole/hr",
        "CL_REABSORPTION": "mmole/hr",
        "diuresis": "ml/hr",
        "vin_h2o": "ml/hr",
        "H2O_UPTAKE": "ml/hr",
        "h2o_reabsorption": "ml/hr",
        "ECF": "l",
        "[na]": unit_na,
        "[cl]": unit_cl,
        "na_urine": unit_na_urine,
        "cl_urine": unit_cl_urine,
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
        "[Cve_hctz]": label_hctz,
        "Aurine_hctz": label_hctz_urine,
        "Afeces_hctz": label_hctz_feces,
        "KI__HCTZEX": label_hctz_excretion_urine,
        "bp_systolic": "blood pressure systolic\n",
        "bp_diastolic": "blood pressure diastolic\n",
        "bp_mean": "mean arterial pressure\n",
        "Vurine": label_urine_volume,
        "NA_EXCRETION": "Sodium excretion\n",
        "CL_EXCRETION": "Chloride excretion\n",
        "vin_na": "Na uptake baseline",
        "vin_cl": "Cl uptake baseline",
        "NA_UPTAKE": "Na uptake",
        "CL_UPTAKE": "Cl uptake",
        "NA_FILTRATION": "Na filtration",
        "CL_FILTRATION": "Cl filtration",
        "NA_REABSORPTION": "Na reabsorption",
        "CL_REABSORPTION": "Cl reabsorption",
        "vin_h2o": "H2O uptake baseline",
        "H2O_UPTAKE": "H2O uptake",
        "h2o_reabsorption": "H2O reabsorption",
        "diuresis": "diuresis",
        "ECF": "Extracellular fluid",
        "[na]": label_na,
        "[cl]": label_cl,
        "na_urine": label_na_urine,
        "cl_urine": label_cl_urine,
    }

    color_hctz = "black"
    color_hctz_urine = "black"

    # molecular weights of hydrochlorothiazide and renin (Giudicelli1987)
    Mr: ClassVar[MolecularWeights] = MolecularWeights(
        hctz=Q(297.7, "g/mole"),
        ren=Q(45057, "g/mole"),
    )

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

    #: the urine of a collection: what is emptied at its end, see
    #: `collected_amounts`
    urine_reset: ClassVar[dict[str, Quantity]] = {
        "Aurine_hctz": Q(0, "mmole"),
        "Vurine": Q(1e-6, "l"),
        "na_urine": Q(0, "mmole"),
        "cl_urine": Q(0, "mmole"),
    }

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

    #: the healthy glomerular filtration rate of the model at 75 kg [ml/min],
    #: `GFR_base`, the normal rate of the classes of renal impairment
    gfr_healthy: ClassVar[float] = 101.0

    #: the supported renal function of the model: up to 2 the filtration
    #: stays a physiological fraction of the renal plasma flow (0.28 at a
    #: hematocrit of 0.45, 0.14 at renal function 1), and without filtration
    #: the excretion of sodium and chloride goes on without urine and the
    #: urinary concentration of HCTZ is not defined (anuria is not supported)
    renal_function_range: ClassVar[tuple[float, float]] = (0.05, 2.0)

    @classmethod
    def renal_function(
        cls, clearance: float, f_cardiac_function: float = 1.0
    ) -> Quantity:
        """Get the renal function of a measured clearance.

        The glomerular filtration rate of the model is `f_renal_function *
        GFR_base`, and `GFR_base` is proportional to the renal blood flow and
        so to the cardiac function. A measured clearance includes the effect
        of an impaired cardiac function, the renal function is the clearance
        relative to the healthy rate of that cardiac function, so that the
        simulated rate is the measured one.

        Args:
            clearance: measured clearance (creatinine clearance or GFR) [ml/min],
                not indexed to the body surface area.
            f_cardiac_function: cardiac function of the simulation.

        Returns:
            The renal function `f_renal_function`.

        Raises:
            ValueError: for a renal function outside of `renal_function_range`.
        """
        value = clearance / (cls.gfr_healthy * f_cardiac_function)
        low, high = cls.renal_function_range
        if not low <= value <= high:
            raise ValueError(
                f"The renal function {value:.3g} of a clearance of {clearance} "
                f"ml/min is outside of the supported range {low} to {high}."
            )
        return Q(value, "dimensionless")

    cardiac_colors: ClassVar[Mapping[str, str]] = {
        "Normal cardiac function": "black",
        "Mild cardiac impairment": "#FFB233",
        "Moderate cardiac impairment": "#FF8333",
        "Severe cardiac impairment": "tab:red",
        "Cardiac failure": "darkred",
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
        across = None if self.uncertainty is None else self.uncertainty.id
        return {
            key: calculate_hctz_pk(
                experiment=self, res=self.results[f"task_{key}"], across=across
            )
            for key in keys
            if float(self.results[f"task_{key}"]["PODOSE_hctz"].isel(time=0).max()) > 0
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
        across = None if self.uncertainty is None else self.uncertainty.id
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
