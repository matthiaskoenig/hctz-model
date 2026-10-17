"""Simulation experiment of the study Koytchev2004."""

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


class Koytchev2004(HCTZSimulationExperiment):
    """Simulation experiment of Koytchev2004.

    Single oral dosing of 20mg lisinopril/12.5mg hydrochlorothiazide combination tablet.
    Comparing test product to reference drug.
    """

    prefixes: ClassVar[list[str]] = [
        "test",
        "reference",
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label == "reference_hydro" or label == "test_hydro":
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[self.to_sid(f"{fig_id}_{label}")] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        simulations["hctz12p5"] = Simulation(
            time_unit="hr",
            end=80,
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
        for prefix in self.prefixes:
            mappings[self.to_sid(f"fm_Fig2_{prefix}_hydro")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig2_{prefix}_hydro"),
                    xid="time",
                    yid="mean",
                    yid_sd=None,
                    count="count",
                ),
                observable=FitData(
                    self, task="task_hctz12p5", xid="time", yid="[Cve_hctz]"
                ),
                metadata=PKPDMappingMetaData(
                    # coadministration with lisinopril
                    tissue=Tissue.PLASMA,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.LISINOPRIL,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig 2"
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
            label="Sim",
            color=self.color_hctz,
        )
        # data
        for prefix in self.prefixes:
            plots[0].add_data(
                dataset=self.to_sid(f"Fig2_{prefix}_hydro"),
                xid="time",
                yid="mean",
                yid_sd=None,
                count="count",
                label="12.5 mg + LIS20 A" if prefix == "test" else "12.5 mg + LIS20 B",
                color="tab:orange" if prefix == "test" else "tab:blue",
            )

        return {
            self.to_sid(name): fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Koytchev2004, output_dir=Koytchev2004.__name__)
