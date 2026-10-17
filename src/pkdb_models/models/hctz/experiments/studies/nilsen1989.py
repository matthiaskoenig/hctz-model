"""Simulation experiment of the study Nilsen1989."""

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
from sbmlsim.plot import Figure
from sbmlsim.simulation import Change, Simulation

from pkdb_models.models.hctz import MODEL
from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)


class Nilsen1989(HCTZSimulationExperiment):
    """Simulation experiment of Nilsen1989.

    single oral dosing of 25 mg HCTZ with or without 5 mg cilazapril

    The urine was collected before the dose and over 0-1, 1-2, 2-4, 4-8 and
    8-24 hr (Fig4 gives the rates at the "mid-point time of each collection",
    0.5, 1.5, 3, 6 and 16 hr; the 1-2 hr interval and the 0-24 hr collection
    are named in the text). The collection before the dose has its midpoint at
    -0.5 hr (set to 0 hr in the data), assumed to be -1 to 0 hr. The fit
    compares the sodium of every collection, rate times duration, with the
    urine of the simulation, which empties the urine at the end of every
    collection.
    """

    suffixes: ClassVar[list[str]] = [
        "hctz25",
        # "hctz25_cil5"
    ]
    names: ClassVar[list[str]] = [
        "25 mg HCTZ",
        # "25 mg HCTZ + CIL"
    ]
    colors: ClassVar[dict[str, str]] = {
        "hctz25": "black",
        "hctz25_cil5": "tab:blue",
    }
    #: the urine collections of the sodium of Fig4, the first before the dose
    #: [hr]
    collections: ClassVar[list[tuple[float, float]]] = [
        (-1, 0),
        (0, 1),
        (1, 2),
        (2, 4),
        (4, 8),
        (8, 24),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig4", "Fig5"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            if fig_id == "Fig4":
                for label, df_label in df.groupby("label"):
                    label = str(label)
                    dset = DataSet.from_df(df_label, self.ureg)
                    if label.startswith("excretion_hctz25"):
                        dset.unit_conversion("mean", 1 / self.Mr.hctz)
                    dsets[f"{fig_id}_{label}"] = dset
                    if label.startswith("excretion_sodium"):
                        dsets[f"{fig_id}_{label}_collected"] = DataSet.from_df(
                            self.collected_amounts(df_label, self.collections),
                            self.ureg,
                        )

            elif fig_id == "Fig5":
                for label, df_label in df.groupby("x_label"):
                    label = str(label)
                    dset = DataSet.from_df(df_label, self.ureg)
                    if label.startswith("excretion2_hctz25"):
                        dset.unit_conversion("x", 1 / self.Mr.hctz)
                    dsets[f"{fig_id}_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        # the simulation starts 1 hr before the dose, with the collection
        # before the dose, and empties the urine at the end of every collection
        simulations["hctz25"] = Simulation(
            time_unit="hr",
            end=1 + 40,
            steps=500,
            preinit_changes=self.default_changes(),
            changes=[
                Change(1, {"PODOSE_hctz": Q(25, "mg")}),
                Change([1 + end for _, end in self.collections], self.urine_reset),
            ],
            time_shift=-1,
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        for suffix in self.suffixes:
            mappings[f"fm_Fig4_excretion_sodium_{suffix}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig4_excretion_sodium_{suffix}_collected",
                    xid="time",
                    yid="mean",
                    yid_sd=None,
                    count="count",
                ),
                observable=FitData(
                    self, task="task_hctz25", xid="time", yid="na_urine"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.URINE,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,  # Fig4 only volunteers (healthy)
                    fasting=Fasting.NR,
                    coadministration=Coadministration.CILAZAPRIL
                    if "cil5" in suffix
                    else Coadministration.NONE,
                ),
            )
            # FIXME: bugfix in optimization
            # mappings[f"fm_Fig5_excretion2_{suffix}"] = FitMapping(
            #     self,
            #     reference=FitData(
            #         self,
            #         dataset=f"Fig5_excretion2_{suffix}",
            #         xid="x",
            #         yid="y",
            #         xid_sd=None,
            #         yid_sd=None,
            #         count="count"
            #     ),
            #     observable=FitData(self, task=f"task_hctz25", xid="KI__HCTZEX", yid="NA_EXCRETION"),
            #     metadata=PKPDMappingMetaData(
            #         tissue=Tissue.URINE,
            #         application_form=ApplicationForm.TABLET,
            #         route=Route.PO,
            #         dosing=Dosing.SINGLE,
            #         health=Health.HEALTHY,  # Fig5 only volunteers (healthy)
            #         fasting=Fasting.NR,
            #         coadministration=Coadministration.CILAZAPRIL if "cil5" in suffix else Coadministration.NONE,
            #     ),
            # )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self._figures_fig4_5(),
        }

    def _figures_fig4_5(self) -> dict[str, Figure]:
        name = "Fig4_5"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=4,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(legend=True)
        for k in [0, 1, 3]:
            plots[k].set_xaxis(label=self.label_time, unit="hr")
        plots[3].set_yaxis(label="Sodium urine (collection)", unit="mmole")
        plots[3].add_data(
            task="task_hctz25",
            xid="time",
            yid="na_urine",
            label="Sim",
            color=self.color_hctz,
        )
        for ks, suffix in enumerate(self.suffixes):
            plots[3].add_data(
                dataset=f"Fig4_excretion_sodium_{suffix}_collected",
                xid="time",
                yid="mean",
                yid_sd=None,
                count="count",
                label=self.names[ks],
                marker="o" if suffix.endswith("cil5") else "s",
                color=self.colors[suffix],
                linestyle="",
            )

        plots[0].set_yaxis(
            label=self.label_hctz_excretion_urine, unit=self.unit_hctz_excretion_urine
        )
        (plots[1].set_yaxis(label="Sodium excretion\n", unit="mmole/hr"),)

        plots[2].set_xaxis(
            label=self.label_hctz_excretion_urine, unit=self.unit_hctz_excretion_urine
        )
        plots[2].set_yaxis(label="Sodium excretion\n", unit="mmole/hr")

        # simulation
        for k, (xid, yid) in enumerate(
            [
                ("time", "KI__HCTZEX"),
                ("time", "NA_EXCRETION"),
                ("KI__HCTZEX", "NA_EXCRETION"),
            ]
        ):
            plots[k].add_data(
                task="task_hctz25",
                xid=xid,
                yid=yid,
                label="Sim",
                color=self.color_hctz,
            )

        # data
        for ks, suffix in enumerate(self.suffixes):
            for k, (dset_id, xid, yid) in enumerate(
                [
                    (f"Fig4_excretion_{suffix}", "time", "mean"),
                    (f"Fig4_excretion_sodium_{suffix}", "time", "mean"),
                    (f"Fig5_excretion2_{suffix}", "x", "y"),
                ]
            ):
                plots[k].add_data(
                    dataset=dset_id,
                    xid=xid,
                    yid=yid,
                    xid_sd=None,
                    yid_sd=None,
                    count="count",
                    label=self.names[ks],
                    marker="o" if suffix.endswith("cil5") else "s",
                    color=self.colors[suffix],
                )

        return {
            name: fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Nilsen1989, output_dir=Nilsen1989.__name__)
