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


class Vaidyanathan2006(HCTZSimulationExperiment):
    """Simulation experiment of Vaidyanathan2006.

    multiple dose 25mg HCTZ alone and in combination with aliskiren 300 mg.
    """
    labels = ["hctz_HCTZ25", "hctz_HCTZ25,ALI300HCTZ"]
    colors = {
        "hctz_HCTZ25": "black",
        "hctz_HCTZ25,ALI300HCTZ": "tab:blue",
    }

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[f"{fig_id}_{label}"] = dset

        # print(dsets.keys())
        # print(dsets)
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}
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
            }
        )
        tc2 = Timecourse(
            start=0,
            end=25 * 60,  # [min]
            steps=500,
            changes={
                "PODOSE_hctz": Q_(25, "mg"),
            }
        )
        tcsims["hctz25"] =TimecourseSim(
            [tc0, tc1, tc1, tc2],
            time_offset=-3*24*60,
        )
        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}
        for label in self.labels:
            mappings[f"fm_Fig3_{label}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig3_{label}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_hctz25", xid="time", yid="[Cve_hctz]"
                ),
                metadata=HCTZMappingMetaData(
                    tissue=Tissue.PLASMA,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.MULTI,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.ALISKIREN if "ALI300" in label else Coadministration.NONE,
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

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)

        # simulation
        plots[0].add_data(
            task=f"task_hctz25",
            xid="time",
            yid="[Cve_hctz]",
            label=f"Sim 25",
            color="black",
        )
        # data
        for label in self.labels:
            plots[0].add_data(
                dataset=f"Fig3_{label}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="25 mg + Aliskiren" if label == self.labels[1] else "25 mg",
                color=self.colors[label],
            )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Vaidyanathan2006, output_dir=Vaidyanathan2006.__name__)
