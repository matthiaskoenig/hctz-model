"""Simulation experiment of the study Niopas2011."""

from typing import ClassVar, override

import pandas as pd
from pkpdsim.metadata import (
    ApplicationForm,
    Coadministration,
    Dosing,
    Fasting,
    Health,
    PKPDMappingMetaData,
    Route,
    Tissue,
)
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.hctz import MODEL
from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)


class Niopas2011(HCTZSimulationExperiment):
    """Simulation experiment of Niopas2011.

    Combination with enalapril.
    """

    suffixes: ClassVar[list[str]] = ["ENA20", "REF20"]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hydrochlorothiazide"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[self.to_sid(f"{fig_id}_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        simulations["hctz12p5"] = Simulation(
            time_unit="hr",
            end=40,
            steps=500,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_hctz": Q(12.5, "mg"),
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for suffix in self.suffixes:
            mappings[self.to_sid(f"fm_Fig2_hydrochlorothiazide_{suffix}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig2_hydrochlorothiazide_{suffix}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_hctz12p5", xid="time", yid="[Cve_hctz]"
                ),
                metadata=PKPDMappingMetaData(
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

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig2"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)

        # simulation
        plots[0].add_data(
            task="task_hctz12p5",
            xid="time",
            yid="[Cve_hctz]",
            label="Sim 12.5",
            color=self.color_hctz,
        )
        # data
        for suffix in self.suffixes:
            plots[0].add_data(
                dataset=self.to_sid(f"Fig2_hydrochlorothiazide_{suffix}"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"12.5 mg + {suffix}",
                color="tab:orange" if suffix == "ENA20" else "tab:blue",
            )

        return {
            self.to_sid(name): fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Niopas2011, output_dir=Niopas2011.__name__)
