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


class Hsiao2015(HCTZSimulationExperiment):
    """Simulation experiment of Hsiao2015.

    Multiple oral dosing of 25mg HCTZ.
    """

    suffixes = ["hctz25", "hctz25_kombi"]
    colors = ["black", "tab:blue"]

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
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

        tcsims["hctz25"] = TimecourseSim(
            Timecourse(
                start=0,
                end=30 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "PODOSE_hctz": Q_(25, "mg"),
                },
            )
        )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}
        # plasma
        for k, suffix in enumerate(self.suffixes):
            mappings[f"fm_Fig1_{suffix}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig1_{suffix}",
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
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.LCZ696 if "kombi" in suffix else Coadministration.NONE,
                ),
            )
            return mappings

    def figures(self) -> Dict[str, Figure]:
        name = "Fig1"
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
            label=f"Sim",
            color=self.color_hctz,
        )
        # data
        for k, suffix in enumerate(self.suffixes):
            plots[0].add_data(
                dataset=f"Fig1_{suffix}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="25 mg HCTZ" if suffix == "hctz25" else "25 mg HCTZ + 400 mg LCZ696",
                color=self.colors[k],
            )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Hsiao2015, output_dir=Hsiao2015.__name__)
