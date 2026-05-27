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


class Heise2015(HCTZSimulationExperiment):
    """Simulation experiment of Heise2015.

    Multiple oral dosing of 25mg Empagliflozin, 25 mg HCTZ or 5 mg Torasemide alone or in combination (Emp+HCTZ or Emp+Tor).
    """

    groups = ["hctz25", "hctz25,emp25"]
    colors = {
        "hctz25": "black",
        "hctz25,emp25": "tab:blue",
    }

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3", "Tab3A"]:
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
        infos = [
            ("Fig3", "", "[Cve_hctz]", Tissue.PLASMA),
            ("Tab3A", "_aurine", "Aurine_hctz", Tissue.URINE),
        ]

        for info in infos:
            for group in self.groups:
                (fig_id, suffix, yid, tissue) = info
                mappings[f"fm_{fig_id}_{group}{suffix}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{fig_id}_{group}{suffix}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(self, task=f"task_hctz25", xid="time", yid=yid),
                    metadata=HCTZMappingMetaData(
                        tissue=tissue,
                        application_form=ApplicationForm.TABLET,
                        route=Route.PO,
                        dosing=Dosing.MULTI,
                        health=Health.HEALTHY,
                        fasting=Fasting.NR,
                        coadministration=Coadministration.EMPAGLIFLOZIN if "emp25" in group else Coadministration.NONE,
                    ),
                )
        return mappings

    def figures(self) -> Dict[str, Figure]:
        name = "Fig3 & Tab3A"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)
        plots[1].set_yaxis(self.label_hctz_urine, unit=self.unit_hctz_urine)

        # simulation
        plots[0].add_data(
            task=f"task_hctz25",
            xid="time",
            yid="[Cve_hctz]",
            label=f"Sim",
            color="black",
        )

        plots[1].add_data(
            task=f"task_hctz25",
            xid="time",
            yid="Aurine_hctz",
            label=f"Sim",
            color="black",
        )
        # data
        for group in self.groups:
            plots[0].add_data(
                dataset=f"Fig3_{group}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"25 mg {group}",
                color=self.colors[group],
            )

            plots[1].add_data(
                dataset=f"Tab3A_{group}_aurine",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"25 mg {group}",
                linestyle="",
                color=self.colors[group],
            )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Heise2015, output_dir=Heise2015.__name__)
