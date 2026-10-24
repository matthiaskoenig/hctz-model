"""Simulation experiment of the study Barbhaiya1982."""

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


class Barbhaiya1982(HCTZSimulationExperiment):
    """Simulation experiment of Barbhaiya1982.

    Single oral dosing of 50mg HCTZ under fasting and non fasting conditions with 250ml and 20ml of water.

    The urine was collected over 0-1, 1-2, 2-4, 4-6, 6-8, 8-12, 12-24 and 24-48
    hr (the intervals are not listed, the times of Fig1-3 are their midpoints,
    and the rates times the durations add up to the cumulative amounts of Fig5
    and Table I). The fit compares the amount of every collection, rate times
    duration, with the urine of the simulation `hctz50_collections`, which
    empties the urine at the end of every collection. The cumulative amounts
    of Fig5 are the same urine and are not fitted a second time.
    """

    group_keys: ClassVar[list[str]] = ["fast250", "fast20", "nofast250"]
    group_labels: ClassVar[list[str]] = [
        "250 ml water, fasting",
        "20 ml water, fasting",
        "250 ml water, no fasting",
    ]
    colors: ClassVar[list[str]] = ["black", "tab:blue", "tab:green"]

    yids: ClassVar[list[str]] = [
        "[Cve_hctz]",  # plasma concentration
        "KI__HCTZEX",  # excretion rate
        "Aurine_hctz",  # cumulative amount urine
    ]
    prefixes: ClassVar[list[str]] = [
        "hctz50_",
        "excretion_hctz50_",
        "amount_cumulative_hctz50_",
    ]
    #: the urine collections [hr]
    collections: ClassVar[list[tuple[float, float]]] = [
        (0, 1),
        (1, 2),
        (2, 4),
        (4, 6),
        (6, 8),
        (8, 12),
        (12, 24),
        (24, 48),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig2", "Fig3", "Fig5"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith(("hctz", "excretion_", "amount_")):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[self.to_sid(label)] = dset
                if label.startswith("excretion_"):
                    collected = DataSet.from_df(
                        self.collected_amounts(df_label, self.collections),
                        self.ureg,
                    )
                    collected.unit_conversion("mean", 1 / self.Mr.hctz)
                    dsets[self.to_sid(f"{label}_collected")] = collected

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        # no simulation of fasting or different water amounts !
        simulations["hctz50"] = Simulation(
            time_unit="hr",
            end=50,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_hctz": Q(50, "mg"),
            },
        )
        # the urine emptied at the end of every collection
        simulations["hctz50_collections"] = Simulation(
            time_unit="hr",
            end=50,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_hctz": Q(50, "mg"),
            },
            changes=[Change([end for _, end in self.collections], self.urine_reset)],
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        # the plasma, and the amounts of the collections in the urine
        observables = {
            "hctz50_": ("hctz50_", "task_hctz50", "[Cve_hctz]"),
            "excretion_hctz50_": (
                "excretion_hctz50_",
                "task_hctz50_collections",
                "Aurine_hctz",
            ),
        }
        for group_key in self.group_keys:
            for prefix, (dataset, task, yid) in observables.items():
                suffix = "_collected" if prefix.startswith("excretion") else ""
                mappings[self.to_sid(f"fm_{prefix}{group_key}")] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"{dataset}{group_key}{suffix}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(self, task=task, xid="time", yid=yid),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.PLASMA
                        if yid.startswith("[Cve_")
                        else Tissue.URINE,
                        application_form=ApplicationForm.TABLET,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FED
                        if "nofast" in group_key
                        else Fasting.FASTED,
                        coadministration=Coadministration.NONE,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig1-5"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=1,
            num_cols=4,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)
        plots[1].set_yaxis(
            self.label_hctz_excretion_urine, unit=self.unit_hctz_excretion_urine
        )
        plots[2].set_yaxis(self.label_hctz_urine, unit=self.unit_hctz_urine)
        plots[3].set_yaxis(
            f"{self.label_hctz_urine.strip()} (collection)", unit=self.unit_hctz_urine
        )

        for kg, group_key in enumerate(self.group_keys):
            group_label = self.group_labels[kg]

            # simulation
            for k, yid in enumerate(self.yids):
                plots[k].add_data(
                    task="task_hctz50",
                    xid="time",
                    yid=yid,
                    label=f"Sim {group_key}",
                    color=self.colors[kg],
                )

            plots[3].add_data(
                task="task_hctz50_collections",
                xid="time",
                yid="Aurine_hctz",
                label=f"Sim {group_key}",
                color=self.colors[kg],
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
            plots[3].add_data(
                dataset=self.to_sid(f"excretion_hctz50_{group_key}_collected"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{group_label}",
                color=self.colors[kg],
                linestyle="",
            )

        return {
            self.to_sid(name): fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Barbhaiya1982, output_dir=Barbhaiya1982.__name__)
