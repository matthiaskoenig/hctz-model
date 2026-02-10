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


class Januszewicz1959(HCTZSimulationExperiment):
    """Simulation experiment of Januszewicz1959.

    single iv dosing of 25, 50, 100 mg HCTZ.
    """
    doses = [25, 50, 100]
    colors = {
        25: "black",
        50: "tab:blue",
        100: "tab:orange",
    }

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2tc1"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                dsets[label] = dset

        # print(dsets.keys())
        # print(dsets)
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        for dose in self.doses:
            tcsims[f"hctz{dose}"] = TimecourseSim(
                Timecourse(
                    start=0,
                    end=40 * 60,  # [min]
                    steps=500,
                    changes={
                        **self.default_changes(),
                        "IVDOSE_hctz": Q_(dose, "mg"),
                    },
                )
            )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}
        infos = [
            ("diuresis", "diuresis"),
            ("excretion_na", "NA_EXCRETION"),
            ("excretion_cl", "CL_EXCRETION")
        ]

        for dose in self.doses:
            for info in infos:
                (name, yid) = info
                mappings[f"fm_{name}_{dose}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"{name}_{dose}",
                    xid="time",
                    yid="mean",
                    yid_sd=None,
                    count="count",
                ),
                observable=FitData(self, task=f"task_hctz{dose}", xid="time", yid=yid),
                metadata=HCTZMappingMetaData(
                    tissue=Tissue.URINE,
                    application_form=ApplicationForm.TABLET,
                    route=Route.IV,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.NONE,
                    outlier=True,
                ),
            )

        return mappings

    def figures(self) -> Dict[str, Figure]:
        name = "Fig2tc"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=3,
            num_cols=1,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(label=self.labels["diuresis"], unit=self.units["diuresis"]),
        plots[1].set_yaxis(label="Sodium excretion\n", unit="mmole/hr"),
        plots[2].set_yaxis(label="Chloride excretion\n", unit="mmole/hr"),

        # simulation
        for dose in self.doses:
            for k, yid in enumerate([
                "diuresis", "NA_EXCRETION", "CL_EXCRETION",
            ]):
                plots[k].add_data(
                    task=f"task_hctz{dose}",
                    xid="time",
                    yid=yid,
                    label=f"Sim {dose}",
                    color=self.colors[dose],
                )

            # data
            for k, name in enumerate([
                "diuresis", "excretion_na", "excretion_cl",
            ]):
                    plots[k].add_data(
                        dataset=f"{name}_{dose}",
                        xid="time",
                        yid="mean",
                        yid_sd=None,
                        count="count",
                        label= f"{dose} mg",
                        color=self.colors[dose],
                    )

        return {
            fig.sid: fig,
        }

if __name__ == "__main__":
    run_experiments(Januszewicz1959, output_dir=Januszewicz1959.__name__)
