from typing import Dict

import pandas as pd
from sbmlutils.console import console
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


class Azumaya1990(HCTZSimulationExperiment):
    """Simulation experiment of Azumaya1990.

    Single oral dosing of 12,5 or 25mg HCTZ.
    """

    doses = [12.5, 25]
    colors = ["tab:blue", "tab:orange"]

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

        # console.print(dsets.keys())
        # console.print(dsets)
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        for dose in self.doses:
            tcsims[f"hctz{dose}"] = TimecourseSim(
                Timecourse(
                    start=0,
                    end=60 * 60,  # [min]
                    steps=500,
                    changes={
                        **self.default_changes(),
                        "PODOSE_hctz": Q_(dose, "mg"),
                    },
                )
            )
        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}
        for kd, dose in enumerate(self.doses):
            mappings[f"fm_hctz{dose}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig3_hctz{dose}",
                    xid="time",
                    yid="mean",
                    yid_sd=None,
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_hctz{dose}", xid="time", yid="[Cve_hctz]",
                ),
                metadata=HCTZMappingMetaData(
                    tissue=Tissue.PLASMA,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.NONE,
                ),
            )
        # console.print(mappings)
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
        for kd, dose in enumerate(self.doses):
            plots[0].add_data(
                task=f"task_hctz{dose}",
                xid="time",
                yid="[Cve_hctz]",
                label=f"Sim {dose}",
                color=self.colors[kd],
            )
            # data
            plots[0].add_data(
                dataset=f"Fig3_hctz{dose}",
                xid="time",
                yid="mean",
                yid_sd=None,
                count="count",
                label=f"{dose} mg",
                color=self.colors[kd],
            )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Azumaya1990, output_dir=Azumaya1990.__name__)
