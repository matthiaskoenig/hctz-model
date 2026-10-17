"""Simulation experiment of the study Heise2015."""

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


class Heise2015(HCTZSimulationExperiment):
    """Simulation experiment of Heise2015.

    Patients with type 2 diabetes received 25 mg HCTZ once daily for 4 days,
    followed by 25 mg HCTZ with 25 mg empagliflozin once daily for 5 days, after
    an overnight fast of at least 10 hours (p. 794, Figure 1). The plasma and
    the urine of 0-24 hr were sampled at steady state after the dose of day 4
    (HCTZ alone) and of day 9 (with empagliflozin) (p. 795). The data refer to
    the last dose. The arms of torasemide are not part of the model.
    """

    groups: ClassVar[list[str]] = ["hctz25", "hctz25,emp25"]
    #: the days of the once daily doses of HCTZ up to the day of sampling
    days: ClassVar[dict[str, int]] = {"hctz25": 4, "hctz25,emp25": 9}
    colors: ClassVar[dict[str, str]] = {
        "hctz25": "black",
        "hctz25,emp25": "tab:blue",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3", "Tab3A"]:
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
        for group, days in self.days.items():
            dose_times = [24 * k for k in range(days)]
            # the urine of the last dosing interval is collected (0-4, 4-8, 8-12
            # and 12-24 hr, the data give its total): the urine is emptied at
            # every dose
            simulations[self.to_sid(group)] = Simulation(
                time_unit="hr",
                end=dose_times[-1] + 30,
                steps=20 * (dose_times[-1] + 30),
                preinit_changes={
                    **self.default_changes(),
                },
                changes=[
                    Change(dose_times, {"PODOSE_hctz": Q(25, "mg")}),
                    Change(dose_times[1:], self.urine_reset),
                ],
                time_shift=-dose_times[-1],
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        infos = [
            ("Fig3", "", "[Cve_hctz]", Tissue.PLASMA),
            ("Tab3A", "_aurine", "Aurine_hctz", Tissue.URINE),
        ]

        for info in infos:
            for group in self.groups:
                (fig_id, suffix, yid, tissue) = info
                mappings[self.to_sid(f"fm_{fig_id}_{group}{suffix}")] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"{fig_id}_{group}{suffix}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=self.to_sid(f"task_{group}"), xid="time", yid=yid
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=tissue,
                        application_form=ApplicationForm.TABLET,
                        route=Route.PO,
                        dosing=Dosing.MULTIPLE,
                        health=Health.T2DM,
                        fasting=Fasting.FASTED,
                        # the metformin of the patients was paused on the last
                        # 2 days of an arm, the days of sampling (p. 794-795)
                        coadministration=Coadministration.EMPAGLIFLOZIN
                        if "emp25" in group
                        else Coadministration.NONE,
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig3 & Tab3A"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", min=-24, max=30), legend=True
        )
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)
        plots[1].set_yaxis(self.label_hctz_urine, unit=self.unit_hctz_urine)

        # simulation
        for group in self.groups:
            for k, yid in enumerate(["[Cve_hctz]", "Aurine_hctz"]):
                plots[k].add_data(
                    task=self.to_sid(f"task_{group}"),
                    xid="time",
                    yid=yid,
                    label=f"Sim {group}",
                    color=self.colors[group],
                )
        # data
        for group in self.groups:
            plots[0].add_data(
                dataset=self.to_sid(f"Fig3_{group}"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"25 mg {group}",
                color=self.colors[group],
            )

            plots[1].add_data(
                dataset=self.to_sid(f"Tab3A_{group}_aurine"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"25 mg {group}",
                linestyle="",
                color=self.colors[group],
            )

        return {
            self.to_sid(name): fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Heise2015, output_dir=Heise2015.__name__)
