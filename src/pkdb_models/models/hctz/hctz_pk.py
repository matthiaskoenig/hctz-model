"""Pharmacokinetic and pharmacodynamic parameters of the HCTZ scans.

The pharmacokinetic parameters are the non-compartmental analysis of
`pkpdutils`, named like the variables of its `NCAResult` (e.g. `auc_last`,
`auc_inf_obs`, `cmax`, `thalf`, `lambda_z`, `cl_f`, `vz_f`), with the unit of
every parameter in `<name>_unit`. The quality of the analysis is part of the
parameters: the terminal phase (`lambda_z_r2_adj`, `lambda_z_n_points`,
`lambda_z_span`), the extrapolated fraction of the AUC (`auc_extrap_fraction`)
and the flags of the analysis (`nca_flags`, e.g. `EXTRAPOLATION_HIGH` above
`EXTRAPOLATION_WARNING`). The simulations decay to the numerical noise of the
integrator, the concentrations below `LLOQ_FRACTION` of the maximum are below
the limit of quantification. The pharmacodynamic parameters are the minimum
and the maximum of the effects.

A scan has one dimension, the scanned parameter; a run over the draws of the
fitted parameters (`run_simulation pkdb_models.models.hctz --uncertainty`) adds
the dimension of the draws. The parameters are calculated for every point of
every dimension, a row per point with its position along each dimension (the
columns `point` and, with draws, `draw`), see `summarize`.
"""

from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from pkpdsim.scan import point_timecourse, scan_dimensions, single_dimension
from pkpdutils import Dose, NCAOptions, Route, Timecourse, nca_single, ureg
from sbmlsim import Q
from sbmlsim.result import ScanResult

if TYPE_CHECKING:
    from pkdb_models.models.hctz.experiments.base_experiment import (
        HCTZSimulationExperiment,
    )

#: concentration of hydrochlorothiazide in plasma
CONCENTRATION = "[Cve_hctz]"
#: oral dose of the scans
DOSE = "PODOSE_hctz"
#: the cumulative amount of hydrochlorothiazide in the urine
URINE = "Aurine_hctz"
#: the cumulative amount of hydrochlorothiazide in the feces, the oral dose
#: which is not absorbed: the model has no systemic elimination into the feces
FECES = "Afeces_hctz"
#: the limit of quantification of the analysis relative to the maximal concentration
LLOQ_FRACTION = 1e-6
#: the extrapolated fraction of the AUC above which the analysis is flagged
EXTRAPOLATION_WARNING = 0.1
#: the effects whose minimum and maximum are the pharmacodynamic parameters
EFFECTS: list[str] = [
    "NA_EXCRETION",
    "CL_EXCRETION",
    "diuresis",
    "bp_systolic",
    "bp_diastolic",
]


def _points(res: ScanResult, across: str | None) -> list[dict[str, int]]:
    """Get the positions of every point of a scan along its dimensions.

    The scan has one dimension besides the draws `across`; the positions are
    those of the dimension of the scan and of the draws.
    """
    dims = scan_dimensions(res, across)
    if len(dims) != 1:
        raise ValueError(
            f"A scan of one dimension is required, not of {dims} (draws: {across})."
        )
    names = [dims[0], *([across] if across is not None else [])]
    return [
        dict(zip(names, position, strict=True))
        for position in itertools.product(*(range(res.ds.sizes[n]) for n in names))
    ]


def _columns(point: dict[str, int], across: str | None) -> dict[str, int]:
    """Get the columns of the position of a point, `point` and `draw`."""
    columns = {"point": next(v for k, v in point.items() if k != across)}
    if across is not None:
        columns["draw"] = point[across]
    return columns


def pk_parameters(
    experiment: HCTZSimulationExperiment,
    res: ScanResult,
    index: int | dict[str, int],
) -> dict[str, float | str]:
    """Calculate the pharmacokinetic parameters of a simulation of a scan.

    The fractions of the dose in the urine (`fe_urine`) and in the feces
    (`fe_feces`, the oral dose which is not absorbed) at the end of the
    simulation, and the rest in the body (`f_remaining`). The renal clearance
    `cl_renal` is the amount in the urine over `auc_last`; the systemic
    clearance `cl_sys` is the absorbed dose (the dose minus the feces) over
    `auc_inf_obs`, and `cl_f` (of the NCA) is the apparent oral clearance,
    the dose over `auc_inf_obs`. HCTZ is eliminated only by the kidneys, so
    `cl_sys` is `cl_renal` when the simulation is long enough.

    Args:
        experiment: experiment of the scan, for the molecular weight.
        res: result of the scan.
        index: index of the simulation in a scan of one dimension, or the
            position of the point along every dimension of the scan.

    Returns:
        The parameters and their units (`<name>_unit`).
    """
    units = res.units
    point = index if isinstance(index, dict) else {single_dimension(res): index}

    # the dose in the substance unit of the concentration, which `cl_f` and
    # `vz_f` require
    dose_mass = Q(res[DOSE].isel({**point, "time": 0}).item(), units[DOSE])
    dose = (dose_mass / experiment.Mr.hctz).to("mmole")
    time, values = point_timecourse(res, CONCENTRATION, **point)
    cmax = float(values.max())
    timecourse = Timecourse(
        time=time,
        value=values,
        time_unit=str(units["time"]),
        unit=str(units[CONCENTRATION]),
        lloq=LLOQ_FRACTION * cmax if cmax > 0 else None,
        dose=Dose(amount=dose.magnitude, unit="mmol", route=Route.ORAL),
        substance="hctz",
    )
    result = nca_single(
        timecourse, options=NCAOptions(extrapolation_warning=EXTRAPOLATION_WARNING)
    )
    pk = result.to_quantities()

    urine, feces = (
        ureg.Quantity(res[sid].isel({**point, "time": -1}).item(), str(units[sid]))
        for sid in [URINE, FECES]
    )
    dose_amount = ureg.Quantity(dose.magnitude, "mmol")
    excretion = {
        "fe_urine": (urine / dose_amount).to("dimensionless"),
        "fe_feces": (feces / dose_amount).to("dimensionless"),
        "f_remaining": (1 - (urine + feces) / dose_amount).to("dimensionless"),
        "cl_renal": (urine / pk["auc_last"]).to("ml/min"),
        "cl_sys": ((dose_amount - feces) / pk["auc_inf_obs"]).to("ml/min"),
    }

    parameters: dict[str, float | str] = {
        "substance": "hctz",
        "nca_flags": ", ".join(result.flags()),
    }
    for key, value in {**pk, **excretion}.items():
        parameters[key] = value.magnitude
        parameters[f"{key}_unit"] = str(value.units)
    return parameters


def calculate_hctz_pk(
    experiment: HCTZSimulationExperiment, res: ScanResult, across: str | None = None
) -> pd.DataFrame:
    """Calculate the pharmacokinetic parameters of every simulation of a scan.

    Args:
        experiment: experiment of the scan.
        res: result of the scan.
        across: the dimension of the draws of the fitted parameters, `None`
            for a scan without draws.

    Returns:
        One row per simulation of the scan, with its position (`point`, and
        `draw` with draws).
    """
    return pd.DataFrame(
        [
            {**_columns(point, across), **pk_parameters(experiment, res, point)}
            for point in _points(res, across)
        ]
    )


def calculate_hctz_pd(
    res: ScanResult, across: str | None = None
) -> dict[str, pd.DataFrame]:
    """Calculate the pharmacodynamic parameters of every simulation of a scan.

    Args:
        res: result of the scan.
        across: the dimension of the draws of the fitted parameters, `None`
            for a scan without draws.

    Returns:
        By effect, one row per simulation with its position (`point`, and
        `draw` with draws), the minimum and the maximum.
    """
    units = res.units
    points = _points(res, across)
    frames: dict[str, pd.DataFrame] = {}
    for sid in EFFECTS:
        rows = []
        for point in points:
            _, values = point_timecourse(res, sid, **point)
            rows.append(
                {
                    **_columns(point, across),
                    "sid": sid,
                    "min": values.min(),
                    "max": values.max(),
                    "unit": str(units[sid]),
                }
            )
        frames[sid] = pd.DataFrame(rows)
    return frames


def summarize(
    df: pd.DataFrame, key: str, quantiles: tuple[float, float]
) -> pd.DataFrame:
    """Get the median and the quantiles of a parameter over the draws of every point.

    Args:
        df: the parameters with the columns `point` and `draw`.
        key: the parameter.
        quantiles: the lower and the upper quantile.

    Returns:
        One row per point (the index), the columns `lower`, `median`, `upper`.
    """
    low, high = quantiles
    grouped = df.groupby("point")[key]
    return pd.DataFrame(
        {
            "lower": grouped.quantile(low),
            "median": grouped.median(),
            "upper": grouped.quantile(high),
        }
    ).astype(np.float64)
