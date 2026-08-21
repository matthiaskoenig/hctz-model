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


class Niopas2011(HCTZSimulationExperiment):
    """Simulation experiment of Niopas2011.

    Combination with enalapril.
    """
    suffixes = ["ENA20", "REF20"]

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2"]:
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

        tcsims["hctz12.5"] = TimecourseSim(
            Timecourse(
                start=0,
                end=40 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "PODOSE_hctz": Q_(12.5, "mg"),
                },
            )
        )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}
        for suffix in self.suffixes:
            mappings[f"fm_Fig2_hydrochlorothiazide_{suffix}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig2_hydrochlorothiazide_{suffix}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_hctz12.5", xid="time", yid="[Cve_hctz]"
                ),
                metadata=HCTZMappingMetaData(
                    # coadministration enalapril 20 mg
                    tissue=Tissue.PLASMA,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.ENALAPRIL,
                ),
            )

        return mappings

    def figures(self) -> Dict[str, Figure]:
        name = "Fig2"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=1,
            # name=f"{self.__class__.__name__} {name}",
            name=f"Niopas2004 {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)

        # simulation
        plots[0].add_data(
            task=f"task_hctz12.5",
            xid="time",
            yid="[Cve_hctz]",
            label=f"Sim 12.5",
            color=self.color_hctz,
        )
        # data
        for suffix in self.suffixes:
            plots[0].add_data(
                dataset=f"Fig2_hydrochlorothiazide_{suffix}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"12.5 mg + {suffix}",
                color="tab:orange" if suffix=="ENA20" else "tab:blue",
            )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Niopas2011, output_dir=Niopas2011.__name__)
