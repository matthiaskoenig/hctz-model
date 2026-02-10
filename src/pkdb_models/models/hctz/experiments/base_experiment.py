"""Reusable functionality for multiple simulation experiments."""
import pandas as pd

from collections import namedtuple
from typing import Dict

from sbmlsim.experiment import SimulationExperiment
from sbmlsim.model import AbstractModel
from sbmlsim.task import Task

from pkdb_models.models.hctz import MODEL_PATH
from pkdb_models.models.hctz.hctz_pk import (
    calculate_hydrochlorothiazide_pk,
    calculate_hydrochlorothiazide_pd,
)

MolecularWeights = namedtuple("MolecularWeights", "hctz ren ang1 ald")


class HCTZSimulationExperiment(SimulationExperiment):
    """Base class for all SimulationExperiments."""

    font = {"weight": "bold", "size": 22}
    scan_font = {"weight": "bold", "size": 15}
    tick_font_size = 15
    legend_font_size = 13
    suptitle_font_size = 40

    unit_time = "hr"
    unit_hctz = "µM"
    unit_hctz_urine = "µmol"
    unit_hctz_feces = "µmol"
    unit_hctz_excretion_urine = "nmol/min"

    unit_urine_volume = "ml"
    unit_na_urine = "mmole"
    unit_cl_urine = "mmole"

    units: Dict[str, str] = {
        "time": "hr",
        "[Cve_hctz]": unit_hctz,
        "Aurine_hctz": unit_hctz_urine,
        "Afeces_hctz": unit_hctz_feces,
        "KI__HCTZEX": unit_hctz_excretion_urine,

        "[Cve_ang1]": "nM",
        "[Cve_ald]": "nM",
        "HR": "1/min",
        "bp_systolic": "mmHg",
        "bp_diastolic": "mmHg",
        "renin_activity": "pmole/min/l",
        "Vurine": unit_urine_volume,
        "NA_EXCRETION": "mmole/hr",
        "CL_EXCRETION":  "mmole/hr",
        "diuresis":  "ml/hr",
        "ECF": "l",

        "na_urine": unit_na_urine,
        "cl_urine": unit_cl_urine,

        # RAAS system
        "[anggen]": "pM",  # angiotensinogen in Vplasma
        "[ang1]": "pM",  # angiotensin I in Vplasma
        "ang1_change": "pM",
        "ang1_ratio": "dimensionless",
        "[ang2]": "pM",  # angiotensin II in Vplasma
        "ang2_change": "pM",
        "ang2_ratio": "dimensionless",

        "[ren]": "pM",  # renin in Vplasma
        "ren_change": "pM",
        "ren_ratio": "dimensionless",
        "[ald]": "nM",  # aldosterone in Vplasma
        "ald_change": "nM",
        "ald_ratio": "dimensionless",

        "ANGGEN2ANG1": "pmol/min",  # angiotensinogen to angiotensin I (renin)
        "ANG1ANG2": "pmol/min",  # angiotensin I to angiotensin II (ACE)
        "ANG2DEG": "pmol/min",  # angiotensin II degradation (ANG2DEG)

        "RENSEC": "pmol/min",  # renin secretion (RENSEC)
        "RENDEG": "pmol/min",  # renin degradation (RENDEG)
        "ALDSEC": "pmol/min",  # aldosterone secretion (ALDSEC)
        "ALDDEG": "pmol/min",  # aldosterone degradation (ALDDEG)
    }

    label_time = "time"
    label_hctz = "HCTZ"
    label_hctz_urine = "HCTZ urine\n"
    label_hctz_feces = "HCTZ feces\n"
    label_hctz_excretion_urine = "HCTZ excretion\nurine"

    label_urine_volume = "Urine volume"
    label_na_urine = "Sodium urine"
    label_cl_urine = "Chloride urine"

    labels: Dict[str, str] = {
        "[Cve_hctz]": label_hctz,
        "Aurine_hctz": label_hctz_urine,
        "Afeces_hctz": label_hctz_feces,
        "KI__HCTZEX": label_hctz_excretion_urine,

        "HR": "heart rate",

        "bp_systolic": "blood pressure systolic\n",
        "bp_diastolic": "blood pressure diastolic\n",
        "renin_activity": "renin activity\n",
        "Vurine": label_urine_volume,
        "NA_EXCRETION": "Sodium excretion\n",
        "CL_EXCRETION": "Chloride excretion\n",
        "diuresis": "diuresis",
        "na_urine": label_na_urine,
        "cl_urine": label_cl_urine,
        "ECF": "Extracellular fluid",

        # RAAS system
        "[anggen]": "angiotensinogen",  # angiotensinogen in Vplasma
        "[ang1]": "angiotensin I",  # angiotensin I in Vplasma
        "ang1_change": "angiotensin I change\n",
        "ang1_ratio": "angiotensin I ratio\n",
        "[ang2]": "angiotensin II",  # angiotensin II in Vplasma
        "ang2_change": "angiotensin II change\n",
        "ang2_ratio": "angiotensin II ratio\n",
        "[ren]": "renin",  # renin in Vplasma
        "ren_change": "renin change\n",
        "ren_ratio": "renin ratio\n",
        "[ald]": "aldosterone",  # aldosterone in Vplasma
        "ald_change": "aldosterone change\n",
        "ald_ratio": "aldosterone ratio\n",

        "ANGGEN2ANG1": "ANGGEN2ANG1",  # angiotensinogen to angiotensin I (renin)
        "ANG1ANG2": "ANG1ANG2",  # angiotensin I to angiotensin II (ANG1ANG2)
        "ANG2DEG": "ANG2DEG",  # angiotensin II degradation (ANG2DEG)
        "RENSEC": "renin secretion\n(RENSEC)",  # renin secretion (RENSEC)
        "RENDEG": "renin degradation\n(RENDEG)",  # renin degradation (RENDEG)
        "ALDSEC": "aldosterone secretion\n(ALDSEC)",  # aldosterone secretion (ALDSEC)
        "ALDDEG": "aldosterone degradation\n(ALDDEG)",  # aldosterone degradation (ALDDEG)
    }

    color_hctz = "black"
    color_hctz_urine = "black"

    def models(self) -> Dict[str, AbstractModel]:
        Q_ = self.Q_  # FIXME:
        return {
            "model": AbstractModel(
                source=MODEL_PATH,
                language_type=AbstractModel.LanguageType.SBML,
                changes={},
            )
        }

    @staticmethod
    def _default_changes(Q_):
        """Default changes to simulations."""

        changes = {

            # switch to Km urine model
            # >>> !Optimal parameter 'Kp_hctz' within 5% of upper bound! <<<
            'ftissue_hctz': Q_(0.1268945619898461, 'l/min'),  # [0.01 - 10]
            'Kp_hctz': Q_(0.9863278014342243, 'dimensionless'),  # [0.25 - 1.0]
            'Ka_dis_hctz': Q_(3.3911589867541108, '1/hr'),  # [0.0001 - 10]
            'GU__HCTZABS_k': Q_(0.00240363011285685, '1/min'),  # [0.0001 - 10]
            'KI__HCTZEX_Vmax': Q_(0.002521976126922892, 'mmole/min/l'),  # [0.0001 - 10]
            'KI__HCTZEX_Km': Q_(0.0028843086768038048, 'mM'),  # [1e-06 - 0.01]

            # PD
            # 20251216_190427__9ea46
            'vin_nacl': Q_(0.09218491502645276, 'mmole/min'),  # [0.01 - 0.2]
            'E50_hctz_na': Q_(0.0006884061501025768, 'mM'),  # [1e-06 - 0.01]
            'E50_hctz_cl': Q_(0.0005363664092606548, 'mM'),  # [1e-06 - 0.01]
            'E50_hctz_h2o': Q_(0.0006236904646602116, 'mM'),  # [1e-06 - 0.01]
        }

        return changes

    def default_changes(self: SimulationExperiment) -> Dict:
        """Default changes to simulations."""
        return HCTZSimulationExperiment._default_changes(Q_=self.Q_)

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

                # pharmacokinetics
                "IVDOSE_hctz",
                "PODOSE_hctz",
                "[Cve_hctz]",
                
                "Afeces_hctz",  # cumulative amount of hctz in feces

                "KI__HCTZEX",  # urinary excretion rate
                "Aurine_hctz",  # cumulative amount of hctz in urine
                "hctz_urine_excretion",  # amount of hctz in urine based on collected volume

                "HR",

                # Urine volume & ion balance
                "NA_EXCRETION",  # mmole/hr [mmole/min]
                "CL_EXCRETION",  # mmole/hr [mmole/min]
                "diuresis",  # ml/hr [l/min]
                "Vurine",  # urine volume
                "na_urine", # sodium urine
                "cl_urine", # chloride urine
                "ECF",

                "bp_systolic",  # blood pressure systolic
                "bp_diastolic",  # blood pressure diastolic


                # RAAS system
                "[anggen]",
                "[ang1]",
                "ang1_change",
                "ang1_ratio",
                "[ang2]",
                "ang2_change",
                "ang2_ratio",
                "[ren]",
                "ren_change",
                "ren_ratio",
                "[ald]",
                "ald_change",
                "ald_ratio",

                "ANGGEN2ANG1",
                "ANG1ANG2",
                "ANG2DEG",
                "RENSEC",
                "RENDEG",
                "ALDSEC",
                "ALDDEG",

                # parameter scans
                "PODOSE_hctz",
                "KI__f_renal_function",
                "f_cirrhosis",
                "f_cardiac_function",
            ]
        )
        return {}

    @property
    def Mr(self):
        return MolecularWeights(
            hctz=self.Q_(297.7, "g/mole"),
            ren=self.Q_(45057, "g/mole"),
            ang1=self.Q_(1296.499, "g/mole"),
            ald=self.Q_(360.444, "g/mole"),
        )

    renal_colors = {
        "Control": "black",
        "Normal renal function": "black",
        "Mild renal impairment": "#66c2a4",
        "Moderate renal impairment": "#2ca25f",
        "Severe renal impairment": "#006d2c",
    }
    renal_map = {
        "Normal renal function": 101.0 / 101.0,  # 1.0,
        "Mild renal impairment": 69.5 / 101.0,  # 0.69
        "Moderate renal impairment": 32.5 / 101.0,  # 0.32
        "Severe renal impairment": 19.5 / 101.0,  # 0.19
    }

    cardiac_colors = {
        "Normal cardiac function": "black",
        "Mild cardiac impairment": "#FFB233",
        "Moderate cardiac impairment": "#FF8333",
        "Severe cardiac impairment": "tab:red",
        "Cardiac failure": "darkred",
    }

    # Normal CO: ~4.5 to 6 L/min
    # Mild impairment: Slight reduction or maintained near normal (e.g., 4-5.5 L/min)
    # Moderate impairment: Reduced CO possibly around 3-4 L/min
    # Severe impairment and failure: Marked reduction, often below 3 L/min, sometimes much lower depending on severity and heart failure stage.
    cardiac_map = {
        "Normal cardiac function": 1.0,
        "Mild cardiac impairment": 4.75 / 5.25,  # 0.90,
        "Moderate cardiac impairment": 3.5 / 5.25,  # 0.67,
        "Severe cardiac impairment": 3 / 5.25,  # 0.57,
        "Cardiac failure": 0.5
    }

    # ----------- Cirrhosis map --------------
    cirrhosis_map = {
        "Control": 0,
        "Mild cirrhosis": 0.3994897959183674,  # CPT A
        "Moderate cirrhosis": 0.6979591836734694,  # CPT B
        "Severe cirrhosis": 0.8127551020408164,  # CPT C
    }
    cirrhosis_colors = {
        "Control": "black",
        "Mild cirrhosis": "#74a9cf",  # CPT A
        "Moderate cirrhosis": "#2b8cbe",  # CPT B
        "Severe cirrhosis": "#045a8d",  # CPT C
    }

    # --- Pharmacokinetic parameters ---
    pk_labels = {
        "auc": "AUCend",
        "aucinf": "AUC",
        "cl": "Total clearance",
        "cl_renal": "Renal clearance",
        "cl_hepatic": "Hepatic clearance",
        "cmax": "Cmax",
        "thalf": "Half-life",
        "kel": "kel",
        "vd": "vd",
    }

    pk_units = {
        "auc": "µmole/l*hr",
        "aucinf": "µmole/l*hr",
        "cl": "ml/min",
        "cl_renal": "ml/min",
        "cl_hepatic": "ml/min",
        "cmax": "µmole/l",
        "thalf": "hr",
        "kel": "1/hr",
        "vd": "l",
    }

    def calculate_hydrochlorothiazide_pk(self, scans: list = []) -> Dict[str, pd.DataFrame]:
       """Calculate pk parameters for simulations (scans)"""
       pk_dfs = {}
       if scans:
           for sim_key in scans:
               xres = self.results[f"task_{sim_key}"]
               df = calculate_hydrochlorothiazide_pk(experiment=self, xres=xres)
               pk_dfs[sim_key] = df
       else:
           for sim_key in self._simulations.keys():
               xres = self.results[f"task_{sim_key}"]
               df = calculate_hydrochlorothiazide_pk(experiment=self, xres=xres)
               pk_dfs[sim_key] = df
       return pk_dfs

    def calculate_hydrochlorothiazide_pd(self, scans: list = []) -> Dict[str, pd.DataFrame]:
       """Calculate pd parameters for simulations (scans)"""
       pd_dfs = {}
       if scans:
           for sim_key in scans:
               xres = self.results[f"task_{sim_key}"]
               df = calculate_hydrochlorothiazide_pd(experiment=self, xres=xres)
               pd_dfs[sim_key] = df
       else:
           for sim_key in self._simulations.keys():
               xres = self.results[f"task_{sim_key}"]
               df = calculate_hydrochlorothiazide_pd(experiment=self, xres=xres)
               pd_dfs[sim_key] = df
       return pd_dfs

