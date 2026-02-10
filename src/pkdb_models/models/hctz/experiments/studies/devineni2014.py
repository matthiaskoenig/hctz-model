from copy import deepcopy
from typing import Dict

import pandas as pd
from sbmlsim.data import DataSet, load_pkdb_dataframe
from sbmlsim.fit import FitMapping, FitData

from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Timecourse, TimecourseSim

from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)
from pkdb_models.models.hctz.experiments.metadata import (
    Health, Tissue, ApplicationForm,
    Dosing, Route, Fasting, Coadministration,
    HCTZMappingMetaData,
)
from pkdb_models.models.hctz.helpers import run_experiments


class Devineni2014(HCTZSimulationExperiment):
    """Simulation experiment of Devineni2014.

    Multiple oral dosing of 25mg HCTZ alone or with Canagliflozin 300mg per day
    """
    groups = ["HCTZ25", "CAN300_HCTZ25"]
    colors = {
        "HCTZ25": "black",
        "CAN300_HCTZ25": "tab:blue",
    }

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hydrochlorothiazide"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[f"{fig_id}_{label}"] = dset

        # print(dsets.keys())
        # print(dsets)
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}


        # multiple dosing: S-27T1R28 for HCTZ25 and for
        tc0 = Timecourse(
            start=0,
            end=24 * 60,  # [min]
            steps=500,
            changes={
                **self.default_changes(),
                "PODOSE_hctz": Q_(25, "mg"),
            },
        )
        tc1 = Timecourse(
            start=0,
            end=24 * 60,  # [min]
            steps=500,
            changes={
                "PODOSE_hctz": Q_(25, "mg"),
            },
        )
        tc2 = Timecourse(
            start=0,
            end=25 * 60,  # [min]
            steps=500,
            changes={
                "PODOSE_hctz": Q_(25, "mg"),
            },
        )

        tcsims["hctz25"] = TimecourseSim(
            timecourses=[tc0] + [deepcopy(tc1) for _ in range(27)] + [tc2],
            time_offset=-28 * 24 * 60,  # shift to the last day
        )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}
        for group in self.groups:
            mappings[f"fm_Fig3_hydrochlorothiazide_{group}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig3_hydrochlorothiazide_{group}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(self, task=f"task_hctz25", xid="time", yid="[Cve_hctz]"),
                metadata=HCTZMappingMetaData(
                    tissue=Tissue.PLASMA,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.MULTI,
                    health=Health.HEALTHY,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.CANAGLIFLOZIN if "CAN300" in group else Coadministration.NONE,
                ),
            )
        return mappings

    def figures(self) -> Dict[str, Figure]:
        name = "Fig3"
        fig = Figure(
            experiment=self,
            sid=name,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr", min=-25, max=25), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)

        # simulation
        plots[0].add_data(
            task=f"task_hctz25",
            xid="time",
            yid="[Cve_hctz]",
            label=f"Sim",
            color="black",
        )
        # data
        for group in self.groups:
            plots[0].add_data(
                dataset=f"Fig3_hydrochlorothiazide_{group}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"25 mg ({group})",
                color=self.colors[group],
            )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Devineni2014, output_dir=Devineni2014.__name__)
