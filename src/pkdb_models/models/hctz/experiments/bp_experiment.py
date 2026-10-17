"""Base class of the simulation experiments of the fluid and blood pressure model."""

from collections.abc import Mapping
from pathlib import Path
from typing import Any, ClassVar, override

from pkpdsim.experiment import PKPDSimulationExperiment
from sbmlsim.model import AbstractModel
from sbmlsim.task import Task

from pkdb_models.models.hctz import MODEL, MODEL_BASE_PATH


class BPSimulationExperiment(PKPDSimulationExperiment):
    """Base class of the experiments with the fluid and blood pressure model.

    The experiments simulate the submodel `hctz_fluid` on its own, i.e., the
    sodium, chloride and water balance with the blood pressure.
    """

    pkpd_model = MODEL

    units: ClassVar[Mapping[str, str]] = {
        "time": "hr",
        "vin_h2o": "l/day",
        "ECF": "l",
        "ECF_ref": "l",
        "Vurine": "l",
        "diuresis": "l/day",
        "bp_systolic": "mmHg",
        "bp_diastolic": "mmHg",
        "[na]": "mmole/l",
        "[cl]": "mmole/l",
        "na_urine": "mmole",
        "cl_urine": "mmole",
        "NA_UPTAKE": "mmole/day",
        "CL_UPTAKE": "mmole/day",
        "NA_EXCRETION": "mmole/day",
        "CL_EXCRETION": "mmole/day",
        "vin_na": "mmole/day",
        "vin_cl": "mmole/day",
        "vout_na": "g/day",
        "vout_cl": "g/day",
    }
    labels: ClassVar[Mapping[str, str]] = {
        "time": "Time",
        "vin_h2o": "H2O uptake",
        "ECF": "Extracellular fluid",
        "ECF_ref": "Extracellular fluid reference",
        "Vurine": "Urine volume",
        "diuresis": "Diuresis",
        "bp_systolic": "Systolic blood pressure",
        "bp_diastolic": "Diastolic blood pressure",
        "[na]": "Na (ECF)",
        "[cl]": "Cl (ECF)",
        "na_urine": "Na (urine)",
        "cl_urine": "Cl (urine)",
        "NA_UPTAKE": "Na uptake",
        "CL_UPTAKE": "Cl uptake",
        "NA_EXCRETION": "Na excretion",
        "CL_EXCRETION": "Cl excretion",
        "vin_na": "Na uptake",
        "vin_cl": "Cl uptake",
        "vout_na": "Na excretion",
        "vout_cl": "Cl excretion",
    }

    @override
    def models(self) -> dict[str, AbstractModel | Path]:
        return {
            "model": AbstractModel(
                source=MODEL_BASE_PATH / "hctz_fluid.xml",
                language_type=AbstractModel.LanguageType.SBML,
                changes={},
            )
        }

    @override
    def tasks(self) -> dict[str, Task]:
        return {
            f"task_{key}": Task(model="model", simulation=key)
            for key in self.simulations()
        }

    @override
    def data(self) -> dict[str, Any]:
        # every quantity with a unit is plotted
        self.add_selections_data(selections=list(self.units))
        return {}
