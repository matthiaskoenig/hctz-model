"""Simulation experiment of the study Vaidyanathan2006."""

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
from sbmlsim.simulation import Change, Simulation

from pkdb_models.models.hctz import MODEL
from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)


class Vaidyanathan2006(HCTZSimulationExperiment):
    """Simulation experiment of Vaidyanathan2006.

    multiple dose 25mg HCTZ alone and in combination with aliskiren 300 mg.
    """

    groups: ClassVar[list[str]] = ["hctz_HCTZ25", "hctz_HCTZ25,ALI300HCTZ"]
    colors: ClassVar[dict[str, str]] = {
        "hctz_HCTZ25": "black",
        "hctz_HCTZ25,ALI300HCTZ": "tab:blue",
    }

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
        # 4 doses, every 24 hours, the data is reported from the last dose
        dose_times = [24 * k for k in range(4)]
        simulations["hctz25"] = Simulation(
            time_unit="hr",
            end=3 * 24 + 25,
            steps=2328,
            preinit_changes=self.default_changes(),
            changes=[Change(dose_times, {"PODOSE_hctz": Q(25, "mg")})],
            time_shift=-3 * 24,
        )
        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for label in self.groups:
            mappings[self.to_sid(f"fm_Fig3_{label}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig3_{label}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_hctz25", xid="time", yid="[Cve_hctz]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.MULTIPLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.ALISKIREN
                    if "ALI300" in label
                    else Coadministration.NONE,
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
        plots[0].add_data(
            task="task_hctz25",
            xid="time",
            yid="[Cve_hctz]",
            label="Sim 25",
            color="black",
        )
        # data
        for label in self.groups:
            plots[0].add_data(
                dataset=self.to_sid(f"Fig3_{label}"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="25 mg + Aliskiren" if label == self.groups[1] else "25 mg",
                color=self.colors[label],
            )

        return {
            self.to_sid(name): fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Vaidyanathan2006, output_dir=Vaidyanathan2006.__name__)
