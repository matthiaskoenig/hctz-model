"""Simulation experiment of the study Barbhaiya1982a."""

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


class Barbhaiya1982a(HCTZSimulationExperiment):
    """Simulation experiment of Barbhaiya1982a.

    Comparative bioavailability and pharmacokinetics of hydrochlorothiazide from oral tablet dosage forms, determined by plasma level and urinary excretion methods.
    Single 50 mg oral doses of hydrochlorothiazide, comparing bioavailability of two hydrochlorothiazide products
    """

    group_keys: ClassVar[list[str]] = ["msd", "stanlab"]
    group_labels: ClassVar[list[str]] = ["HCTZ 50 msd", "HCTZ 50 stanlab"]
    colors: ClassVar[list[str]] = ["tab:blue", "tab:green"]

    yids: ClassVar[list[str]] = [
        "[Cve_hctz]",  # plasma concentration
        "Aurine_hctz",  # cumulative amount urine
    ]
    prefixes: ClassVar[list[str]] = [
        "hctz50_",
        "amount_",
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab1", "Tab2"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith(("hctz", "amount")):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[self.to_sid(label)] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        # no simulation of fasting or different water amounts !
        simulations["hctz50"] = Simulation(
            time_unit="hr",
            end=50,
            steps=500,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_hctz": Q(50, "mg"),
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        for group_key in self.group_keys:
            for k, yid in enumerate(self.yids):
                prefix = self.prefixes[k]
                mappings[self.to_sid(f"fm_{prefix}{group_key}")] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"{prefix}{group_key}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task="task_hctz50",
                        xid="time",
                        yid=yid,
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.PLASMA
                        if yid.startswith("[Cve_")
                        else Tissue.URINE,
                        application_form=ApplicationForm.TABLET,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.NONE,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Tab 1 & 2"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)
        plots[1].set_yaxis(self.label_hctz_urine, unit=self.unit_hctz_urine)

        for kg, group_key in enumerate(self.group_keys):
            group_label = self.group_labels[kg]

            # simulation
            for k, yid in enumerate(self.yids):
                plots[k].add_data(
                    task="task_hctz50",
                    xid="time",
                    yid=yid,
                    label="Sim hctz50",
                    color="black",
                )

            # data
            for k, prefix in enumerate(self.prefixes):
                plots[k].add_data(
                    dataset=self.to_sid(f"{prefix}{group_key}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{group_label}",
                    color=self.colors[kg],
                )

        return {
            self.to_sid(name): fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Barbhaiya1982a, output_dir=Barbhaiya1982a.__name__)
