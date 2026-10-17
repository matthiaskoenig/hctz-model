"""Simulation experiment of the study Azumaya1990."""

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


class Azumaya1990(HCTZSimulationExperiment):
    """Simulation experiment of Azumaya1990.

    Single oral dosing of 12,5 or 25mg HCTZ.
    """

    doses: ClassVar[list[float]] = [12.5, 25]
    colors: ClassVar[list[str]] = ["tab:blue", "tab:orange"]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[self.to_sid(f"{fig_id}_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        for dose in self.doses:
            simulations[self.to_sid(f"hctz{dose}")] = Simulation(
                time_unit="hr",
                end=60,
                steps=500,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_hctz": Q(dose, "mg"),
                },
            )
        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for dose in self.doses:
            mappings[self.to_sid(f"fm_hctz{dose}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig3_hctz{dose}"),
                    xid="time",
                    yid="mean",
                    yid_sd=None,
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_hctz{dose}"),
                    xid="time",
                    yid="[Cve_hctz]",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.NONE,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig3"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            name=f"{self.__class__.__name__} {name}",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)
        # simulation
        for kd, dose in enumerate(self.doses):
            plots[0].add_data(
                task=self.to_sid(f"task_hctz{dose}"),
                xid="time",
                yid="[Cve_hctz]",
                label=f"Sim {dose}",
                color=self.colors[kd],
            )
            # data
            plots[0].add_data(
                dataset=self.to_sid(f"Fig3_hctz{dose}"),
                xid="time",
                yid="mean",
                yid_sd=None,
                count="count",
                label=f"{dose} mg",
                color=self.colors[kd],
            )

        return {
            self.to_sid(name): fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Azumaya1990, output_dir=Azumaya1990.__name__)
