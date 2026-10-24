"""Simulation experiment of the study Devineni2014."""

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


class Devineni2014(HCTZSimulationExperiment):
    """Simulation experiment of Devineni2014.

    Multiple oral dosing of 25mg HCTZ alone or with Canagliflozin 300mg per day
    """

    groups: ClassVar[list[str]] = ["HCTZ25", "CAN300_HCTZ25"]
    #: the legend names of the groups
    legends: ClassVar[dict[str, str]] = {
        "HCTZ25": "25 mg",
        "CAN300_HCTZ25": "25 mg + canagliflozin 300 mg",
    }
    colors: ClassVar[dict[str, str]] = {
        "HCTZ25": "black",
        "CAN300_HCTZ25": "tab:blue",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hydrochlorothiazide"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[f"{fig_id}_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        # multiple dosing: S-27T1R28 for HCTZ25 and for
        # 29 doses, every 24 hours, the data is reported from the last dose
        dose_times = [24 * k for k in range(29)]
        simulations["hctz25"] = Simulation(
            time_unit="hr",
            end=28 * 24 + 25,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_hctz": Q(25, "mg"),
            },
            changes=[self.add_doses(dose_times[1:], {"PODOSE_hctz": Q(25, "mg")})],
            time_shift=-28 * 24,  # shift to the last day
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for group in self.groups:
            mappings[f"fm_Fig3_hydrochlorothiazide_{group}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig3_hydrochlorothiazide_{group}",
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
                    fasting=Fasting.NR,
                    coadministration=Coadministration.CANAGLIFLOZIN
                    if "CAN300" in group
                    else Coadministration.NONE,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig3"
        fig = Figure(
            experiment=self,
            sid=name,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", min=-25, max=25), legend=True
        )
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)

        # simulation
        plots[0].add_data(
            task="task_hctz25",
            xid="time",
            yid="[Cve_hctz]",
            label="Sim",
            color="black",
        )
        # data
        for group in self.groups:
            plots[0].add_data(
                dataset=f"Fig3_hydrochlorothiazide_{group}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=self.legends[group],
                color=self.colors[group],
            )

        return {
            name: fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Devineni2014, output_dir=Devineni2014.__name__)
