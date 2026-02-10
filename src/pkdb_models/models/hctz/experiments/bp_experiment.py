"""Reusable functionality for multiple simulation experiments."""

from typing import Dict

from sbmlsim.experiment import SimulationExperiment
from sbmlsim.model import AbstractModel
from sbmlsim.task import Task

from pkdb_models.models.hctz import MODEL_BASE_PATH


class BPSimulationExperiment(SimulationExperiment):
    """Base class for all SimulationExperiments."""

    font = {"weight": "bold", "size": 22}
    scan_font = {"weight": "bold", "size": 15}
    tick_font_size = 15
    legend_font_size = 13
    suptitle_font_size = 40

    units: Dict[str, str] = {
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
        "NACL_UPTAKE": "mmole/day",
        "NA_EXCRETION": "mmole/day",
        "CL_EXCRETION": "mmole/day",
        "vin_na": "g/day",
        "vin_cl": "g/day",
        "vout_na": "g/day",
        "vout_cl": "g/day",
    }
    labels: Dict[str, str] = {
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
        "NACL_UPTAKE": "NaCl uptake",
        "NA_EXCRETION": "Na excretion",
        "CL_EXCRETION": "Cl excretion",
        "vin_na": "Na uptake",
        "vin_cl": "Cl uptake",
        "vout_na": "Na excretion",
        "vout_cl": "Cl excretion",
    }

    def models(self) -> Dict[str, AbstractModel]:
        Q_ = self.Q_
        return {
            "model": AbstractModel(
                source=MODEL_BASE_PATH / "hctz_fluid.xml",
                language_type=AbstractModel.LanguageType.SBML,
                changes={},
            )
        }

    @staticmethod
    def _default_changes(Q_):
        """Default changes to simulations."""

        changes = {}

        return changes

    def default_changes(self: SimulationExperiment) -> Dict:
        """Default changes to simulations."""
        return BPSimulationExperiment._default_changes(Q_=self.Q_)

    def tasks(self) -> Dict[str, Task]:
        if self.simulations():
            return {
                f"task_{key}": Task(model="model", simulation=key)
                for key in self.simulations()
            }
        return {}

    def data(self) -> Dict:
        self.add_selections_data(
            selections=[
                "time",
                "vin_h2o",
                "ECF",
                "ECF_ref",
                "Vurine",
                "diuresis",
                "bp_systolic",
                "bp_diastolic",
                "[na]",
                "[cl]",
                "na_urine",
                "cl_urine",
                "NACL_UPTAKE",
                "NA_EXCRETION",
                "CL_EXCRETION",
                "vin_na",
                "vin_cl",
                "vout_na",
                "vout_cl",
            ]
        )
        return {}
