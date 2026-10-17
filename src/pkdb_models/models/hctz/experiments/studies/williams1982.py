"""Simulation experiment of the study Williams1982."""

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


class Williams1982(HCTZSimulationExperiment):
    """Simulation experiment of Williams1982.

    Single oral dosing of 50 or 100 mg HCTZ alone or in combination with multiple dose of Indomethacin 25 mg.

    The urine was collected over 0-2, 2-4, 4-6, 6-8, 8-12 and 12-24 hr after the
    7 AM dose of placebo (study day 2) and of HCTZ (study day 3). Fig2 gives
    the rate of every collection, the amount divided by its duration, at the
    midpoint of the collection. The fit compares the amount of every
    collection: the simulation empties the urine at the end of every
    collection, and a data point at the end of a collection is compared with
    the amount before the reset. The instantaneous rate at the midpoint
    differs from the rate of a collection by up to 16 % (0-2 hr, HCTZ) and
    25 % (12-24 hr, sodium) in the simulation.

    The arms of Fig2 are the markers open triangle (50 mg), open diamond (100
    mg), filled triangle (50 mg with indomethacin) and filled diamond (100 mg
    with indomethacin). The printed legend swaps the filled triangle and the
    open diamond, but then the 24 hr excretion of HCTZ of panel I would be about
    52 mg after 50 mg and 29 mg after 100 mg, against 31.6 and 53.7 mg in
    Table I; with the markers by dose the amounts of panel I agree with Table
    I (review of Fig2 in pkdb_data).
    """

    suffixes: ClassVar[list[str]] = [
        "hctz50",
        # "hctz50_ind25",
        "hctz100",
        # "hctz100_ind25",
    ]
    names: ClassVar[list[str]] = [
        "50 mg HCTZ",
        # "50 mg HCTZ + IND",
        "100 mg HCTZ",
        # "100 mg HCTZ + IND"
    ]
    doses: ClassVar[list[int]] = [50, 100]
    colors: ClassVar[dict[int, str]] = {
        50: "tab:blue",
        100: "tab:orange",
    }
    #: the collections after a dose [hr]
    collections: ClassVar[list[tuple[int, int]]] = [
        (0, 2),
        (2, 4),
        (4, 6),
        (6, 8),
        (8, 12),
        (12, 24),
    ]
    #: the data of Fig2: label -> rate in the model, amount in the urine
    fig2_observables: ClassVar[dict[str, tuple[str, str]]] = {
        "excretion": ("KI__HCTZEX", "Aurine_hctz"),
        "diuresis": ("diuresis", "Vurine"),
        "sodium": ("NA_EXCRETION", "na_urine"),
        "chlor": ("CL_EXCRETION", "cl_urine"),
    }

    def _collected(self, df: pd.DataFrame) -> pd.DataFrame:
        """Get the amounts of the collections from their rates at the midpoints."""
        intervals = {
            (start + end) / 2 + day: (start + day, end + day)
            for day in [-24, 0]
            for start, end in self.collections
        }
        times = df.loc[df["mean"].notna(), "time"]
        return self.collected_amounts(df, [intervals[float(t)] for t in times])

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2", "Fig3A", "Fig3B", "Fig2A", "Fig2B", "Fig2C"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            if fig_id == "Fig2":
                for label, df_label in df.groupby("label"):
                    label = str(label)
                    dset = DataSet.from_df(df_label, self.ureg)
                    collected = DataSet.from_df(self._collected(df_label), self.ureg)
                    if label.startswith("excretion"):
                        dset.unit_conversion("mean", 1 / self.Mr.hctz)
                        collected.unit_conversion("mean", 1 / self.Mr.hctz)
                    dsets[f"{fig_id}_{label}"] = dset
                    dsets[f"{fig_id}_{label}_collected"] = collected

            elif fig_id == "Fig3A" or fig_id == "Fig3B":
                for label, df_label in df.groupby("x_label"):
                    label = str(label)
                    dset = DataSet.from_df(df_label, self.ureg)
                    if label.startswith("hctz"):
                        dset.unit_conversion("x", 1 / self.Mr.hctz)
                    dsets[f"{fig_id}_{label}"] = dset

            elif fig_id == "Fig2A" or fig_id == "Fig2B" or fig_id == "Fig2C":
                for label, df_label in df.groupby("x_label"):
                    label = str(label)
                    dset = DataSet.from_df(df_label, self.ureg)
                    if label.startswith("excretion"):
                        dset.unit_conversion("x", 1 / self.Mr.hctz)
                    dsets[f"{fig_id}_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        # the ends of the collections of the placebo day and of the day of the
        # dose, in the time of the simulation
        collection_ends = [
            24 + day + end for day in [-24, 0] for _, end in self.collections
        ]
        for dose in self.doses:
            # one day without hydrochlorothiazide, then a single dose; the
            # simulation ends 1 hr after the last collection (24 hr)
            simulations[f"hctz{dose}"] = Simulation(
                time_unit="hr",
                end=24 + 25,
                steps=1960,
                preinit_changes={
                    **self.default_changes(),
                    # the diet of the treatment days: 2000 ml fluid a day
                    # (Methods), with the water of the food and of the
                    # metabolism about 3.0 l a day (the model has 2.3 l, of
                    # which 0.2 l of the metabolism, Hall2021)
                    "vin_h2o": Q(3.0, "l/day"),
                },
                changes=[
                    Change(24, {"PODOSE_hctz": Q(dose, "mg")}),
                    # empty the urine at the end of every collection
                    Change(collection_ends, self.urine_reset),
                ],
                time_shift=-24,
            )
        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        for label, (_, yid) in self.fig2_observables.items():
            for suffix in self.suffixes:
                if "hctz50" in suffix:
                    dose = 50
                elif "hctz100" in suffix:
                    dose = 100
                mappings[f"fm_Fig2_{label}_{suffix}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"Fig2_{label}_{suffix}_collected",
                        xid="time",
                        yid="mean",
                        yid_sd=None,
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_hctz{dose}", xid="time", yid=yid
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.URINE,
                        application_form=ApplicationForm.TABLET,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.INDOMETACIN
                        if "ind25" in suffix
                        else Coadministration.NONE,
                    ),
                )

        # FIXME: support
        # for dose in self.doses:
        #     for k, (dset_id, xid, yid) in enumerate([
        #         (f"Fig3A_hctz_HCTZ{dose}_urine", "x", "y"),
        #         (f"Fig3B_hctz_HCTZ{dose}_urine2", "x", "y"),
        #     ]):
        #         mappings[f"fm_{dset_id}"] = FitMapping(
        #             self,
        #             reference=FitData(
        #                 self,
        #                 dataset=f"{dset_id}",
        #                 xid=xid,
        #                 yid=yid,
        #                 xid_sd=None,
        #                 yid_sd=None,
        #                 count="count",
        #             ),
        #             observable=FitData(
        #                 self,
        #                 task=f"task_hctz{dose}",
        #                 xid="[Cve_hctz]",        # FIXME: concentration HCTZ in URINE not plasma
        #                 yid="NA_EXCRETION" if "3A" in dset_id else "diuresis",
        #             ),
        #             metadata=PKPDMappingMetaData(
        #                 tissue=Tissue.URINE,
        #                 application_form=ApplicationForm.TABLET,
        #                 route=Route.PO,
        #                 dosing=Dosing.SINGLE,
        #                 health=Health.HEALTHY,
        #                 fasting=Fasting.FASTED,
        #                 coadministration=Coadministration.NONE,           #FIXME Coadministration IND?
        #             ),
        #         )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self._figures_fig2(),
            **self._figures_fig3(),
            **self._figures_fig2ABC(),
        }

    def _figures_fig2(self) -> dict[str, Figure]:
        """Fig2: the rates (top) and the amounts of the collections (bottom)."""
        name = "Fig2"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=2,
            num_cols=4,
            name=f"{self.__class__.__name__} {name}",
        )

        # the placebo day and the day of the dose, the collections end at 24 hr
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", min=-25, max=25), legend=True
        )
        for k, (label, unit) in enumerate(
            [
                (self.labels["KI__HCTZEX"], self.units["KI__HCTZEX"]),
                (self.labels["diuresis"], self.units["diuresis"]),
                ("Sodium excretion\n", "mmole/hr"),
                ("Chloride excretion\n", "mmole/hr"),
            ]
        ):
            plots[k].set_yaxis(label=label, unit=unit)
        for k, (_, yid) in enumerate(self.fig2_observables.values()):
            plots[4 + k].set_yaxis(
                label=f"{self.labels[yid].strip()} (collection)", unit=self.units[yid]
            )

        for k, (label, (rate, amount)) in enumerate(self.fig2_observables.items()):
            for ks, suffix in enumerate(self.suffixes):
                dose = 50 if "50" in suffix else 100
                color = self.colors[dose]
                # rates at the midpoints of the collections
                plots[k].add_data(
                    task=f"task_hctz{dose}",
                    xid="time",
                    yid=rate,
                    label=f"Sim {self.names[ks]}",
                    color=color,
                )
                plots[k].add_data(
                    dataset=f"Fig2_{label}_{suffix}",
                    xid="time",
                    yid="mean",
                    yid_sd=None,
                    count="count",
                    label=self.names[ks],
                    marker="o" if suffix.endswith("ind25") else "s",
                    color=color,
                )
                # amounts of the collections at their ends
                plots[4 + k].add_data(
                    task=f"task_hctz{dose}",
                    xid="time",
                    yid=amount,
                    label=f"Sim {self.names[ks]}",
                    color=color,
                )
                plots[4 + k].add_data(
                    dataset=f"Fig2_{label}_{suffix}_collected",
                    xid="time",
                    yid="mean",
                    yid_sd=None,
                    count="count",
                    label=self.names[ks],
                    marker="o" if suffix.endswith("ind25") else "s",
                    color=color,
                    linestyle="",
                )

        return {
            name: fig,
        }

    def _figures_fig3(self) -> dict[str, Figure]:
        name = "Fig3"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        for k in [0, 1]:
            plots[k].set_xaxis(
                label=self.label_hctz_urine, unit=self.unit_hctz
            )  # FIXME: concentration HCTZ in URINE not plasma

        plots[0].set_yaxis(label="Sodium excretion\n", unit="mmole/hr")
        (
            plots[1].set_yaxis(
                label=self.labels["diuresis"], unit=self.units["diuresis"]
            ),
        )

        # simulation
        for dose in self.doses:
            # time ~ hctz_urine_excretion;

            for k, (xid, yid) in enumerate(
                [
                    ("hctz_urine_excretion", "NA_EXCRETION"),
                    ("hctz_urine_excretion", "diuresis"),
                ]
            ):
                plots[k].add_data(
                    task=f"task_hctz{dose}",
                    xid=xid,
                    yid=yid,
                    label="Sim",
                    color=self.colors[dose],
                )

            for k, (dset_id, xid, yid) in enumerate(
                [
                    (f"Fig3A_hctz_HCTZ{dose}_urine", "x", "y"),
                    (f"Fig3B_hctz_HCTZ{dose}_urine2", "x", "y"),
                ]
            ):
                plots[k].add_data(
                    dataset=dset_id,
                    xid=xid,
                    yid=yid,
                    xid_sd=None,
                    yid_sd=None,
                    count="count",
                    label=f"HCTZ {dose}mg",
                    color=self.colors[dose],
                    # linestyle="",
                )

        return {
            name: fig,
        }

    def _figures_fig2ABC(self) -> dict[str, Figure]:
        name = "Fig2ABC"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        for k in [0, 1, 2]:
            plots[k].set_xaxis(
                label=self.labels["KI__HCTZEX"], unit=self.units["KI__HCTZEX"]
            )  # FIXME: concentration HCTZ in URINE not plasma

        (
            plots[0].set_yaxis(
                label=self.labels["diuresis"], unit=self.units["diuresis"]
            ),
        )
        plots[1].set_yaxis(label="Sodium excretion\n", unit="mmole/hr")
        plots[2].set_yaxis(label="Chloride excretion\n", unit="mmole/hr")

        # simulation
        for dose in self.doses:
            # time ~ hctz_urine_excretion;

            for k, (xid, yid) in enumerate(
                [
                    ("KI__HCTZEX", "diuresis"),
                    ("KI__HCTZEX", "NA_EXCRETION"),
                    ("KI__HCTZEX", "CL_EXCRETION"),
                ]
            ):
                plots[k].add_data(
                    task=f"task_hctz{dose}",
                    xid=xid,
                    yid=yid,
                    label=f"Sim {dose}",
                    color=self.colors[dose],
                )

            for k, (dset_id, xid, yid) in enumerate(
                [
                    (f"Fig2A_excretion_hctz{dose}", "x", "y"),
                    (f"Fig2B_excretion_hctz{dose}", "x", "y"),
                    (f"Fig2C_excretion_hctz{dose}", "x", "y"),
                ]
            ):
                plots[k].add_data(
                    dataset=dset_id,
                    xid=xid,
                    yid=yid,
                    xid_sd=None,
                    yid_sd=None,
                    count="count",
                    label=f"HCTZ {dose}mg",
                    color=self.colors[dose],
                    # linestyle="",
                )

        return {
            name: fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Williams1982, output_dir=Williams1982.__name__)
