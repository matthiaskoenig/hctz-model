"""Simulation experiment of the study Januszewicz1959."""

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
from sbmlsim.plot import Axis, Figure, Plot
from sbmlsim.simulation import Change, Simulation

from pkdb_models.models.hctz import MODEL
from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)


class Januszewicz1959(HCTZSimulationExperiment):
    """Simulation experiment of Januszewicz1959.

    Ten healthy subjects in water diuresis (1000 ml water by mouth half an hour
    before the study, then 5 % dextrose in water IV at 20 ml/min throughout) in
    the postabsorptive state received a single IV dose of 25 (cases 1-5), 50
    (cases 6, 7) or 100 mg HCTZ (cases 8-10). Table 1 gives every case as the
    average of 2 or 3 control periods before and of 2 or 3 periods after the
    dose (10-min periods, Table 2), assumed to be three periods directly before
    and after the dose: the collections -30 to 0 and 0 to 30 min. Fig2 gives
    the mean values of the doses (25 mg without case 5). The fit compares the
    sodium, chloride and urine of every collection, rate times duration, with
    the urine of the simulation, which empties the urine at the end of every
    collection.

    The urine volumes are validation data (`fitting/mapping_collections.py`):
    the model has no water diuresis, its urine flow is 1.6 ml/min before the
    dose (data 5.6 to 16.3 ml/min). Case 5 had been on a low-sodium diet
    (sodium 34 µmol/min before the dose, the others 60 to 186 µmol/min), the
    intake of a study is not a parameter of the model: its sodium and chloride
    are validation data as well.
    """

    #: the cases of the doses [mg]
    cases: ClassVar[dict[int, list[int]]] = {
        25: [1, 2, 3, 4, 5],
        50: [6, 7],
        100: [8, 9, 10],
    }
    colors: ClassVar[dict[int, str]] = {
        25: "black",
        50: "tab:blue",
        100: "tab:orange",
    }
    #: the group of the mean values of a dose
    mean_groups: ClassVar[dict[int, str]] = {
        25: "HCTZ25_without_case5",
        50: "HCTZ50",
        100: "HCTZ100",
    }
    #: the urine collections before and after the dose [hr]
    collections: ClassVar[list[tuple[float, float]]] = [(-0.5, 0), (0, 0.5)]
    #: the observables of the collections: the measurement of the label, the
    #: urine of the model and the rate of the model
    urine_observables: ClassVar[dict[str, tuple[str, str]]] = {
        "urinary_volume_rate": ("Vurine", "diuresis"),
        "excretion_rate_sodium": ("na_urine", "NA_EXCRETION"),
        "excretion_rate_chloride": ("cl_urine", "CL_EXCRETION"),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        cases = self.load_dataframe("Tab1")
        for fig_id in ["Tab1", "Fig2tc"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            if fig_id == "Fig2tc":
                df["sd"] = self._sd_of_the_cases(df, cases)
            # the midpoints of the collections in hours
            df["time"] = df["time"] / 60
            df["time_unit"] = "hr"
            for label, df_label in df.groupby("label"):
                label = str(label)
                dsets[f"{fig_id}_{label}"] = DataSet.from_df(df_label, self.ureg)
                if fig_id == "Tab1" and label.endswith(tuple(self.urine_observables)):
                    dsets[f"{fig_id}_{label}_collected"] = DataSet.from_df(
                        self.collected_amounts(df_label, self.collections),
                        self.ureg,
                    )

        return dsets

    def _sd_of_the_cases(self, means: pd.DataFrame, cases: pd.DataFrame) -> pd.Series:
        """Get the standard deviation of the cases of every mean value.

        The publication reports no deviation of the mean values (Fig2, Table 1),
        it is the sample standard deviation of the cases of the mean (25 mg
        without case 5).
        """
        sds = []
        for _, row in means.iterrows():
            dose = next(
                d for d, group in self.mean_groups.items() if group == row["group"]
            )
            measurement = str(row["label"]).removeprefix(f"{row['group']}_")
            labels = {
                f"case{case}_{measurement}" for case in self.cases[dose] if case != 5
            }
            values = cases.loc[
                cases["label"].isin(labels) & (cases["time"] == row["time"]), "value"
            ]
            if len(values) != row["count"]:
                raise ValueError(
                    f"{row['label']}: {len(values)} cases, not {row['count']}."
                )
            sds.append(values.std(ddof=1))
        return pd.Series(sds, index=means.index)

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        # the simulation starts with the collection before the dose and
        # empties the urine at the end of every collection
        for dose in self.cases:
            simulations[f"hctz{dose}"] = Simulation(
                time_unit="hr",
                start=self.collections[0][0],
                end=1,
                steps=180,
                preinit_changes=self.default_changes(),
                changes=[
                    Change(0, {"IVDOSE_hctz": Q(dose, "mg")}),
                    Change([end for _, end in self.collections], self.urine_reset),
                ],
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        for dose, cases in self.cases.items():
            for case in cases:
                for name, (yid, _) in self.urine_observables.items():
                    mappings[f"fm_Tab1_case{case}_{name}"] = FitMapping(
                        self,
                        reference=FitData(
                            self,
                            dataset=f"Tab1_case{case}_{name}_collected",
                            xid="time",
                            yid="value",
                            count="count",
                        ),
                        observable=FitData(
                            self, task=f"task_hctz{dose}", xid="time", yid=yid
                        ),
                        metadata=PKPDMappingMetaData(
                            tissue=Tissue.URINE,
                            application_form=ApplicationForm.SOLUTION,
                            route=Route.IV,
                            dosing=Dosing.SINGLE,
                            health=Health.HEALTHY,
                            fasting=Fasting.FASTED,
                            coadministration=Coadministration.NONE,
                        ),
                    )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self._figure_rates(),
            **self._figure_collections(),
        }

    def _figure_rates(self) -> dict[str, Figure]:
        """Rates of the cases and the mean values against the model."""
        name = "Tab1"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=len(self.urine_observables),
            name=f"{self.__class__.__name__} {name}",
            # the panels share their curves, one legend right of them
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        axes = {
            "urinary_volume_rate": ("Urine flow", "ml/min"),
            "excretion_rate_sodium": (self.labels["NA_EXCRETION"], "mmole/min"),
            "excretion_rate_chloride": (self.labels["CL_EXCRETION"], "mmole/min"),
        }
        for plot, (name_obs, (_, rate)) in zip(
            plots, self.urine_observables.items(), strict=True
        ):
            plot.set_yaxis(*axes[name_obs])
            for dose, cases in self.cases.items():
                plot.add_data(
                    task=f"task_hctz{dose}",
                    xid="time",
                    yid=rate,
                    label=f"Sim {dose} mg IV",
                    color=self.colors[dose],
                )
                self._add_cases(plot, dose, cases, f"Tab1_case{{case}}_{name_obs}")
                plot.add_data(
                    dataset=f"Fig2tc_{self.mean_groups[dose]}_{name_obs}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{dose} mg mean",
                    color=self.colors[dose],
                    marker="s",
                    linestyle="",
                )

        return {name: fig}

    def _figure_collections(self) -> dict[str, Figure]:
        """Urine of the collections of the cases against the model."""
        name = "Tab1_collections"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=len(self.urine_observables),
            name=f"{self.__class__.__name__} {name}",
            # the panels share their curves, one legend right of them
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        for plot, (name_obs, (yid, _)) in zip(
            plots, self.urine_observables.items(), strict=True
        ):
            plot.set_yaxis(label=self.labels[yid], unit=self.units[yid])
            for dose, cases in self.cases.items():
                plot.add_data(
                    task=f"task_hctz{dose}",
                    xid="time",
                    yid=yid,
                    label=f"Sim {dose} mg IV",
                    color=self.colors[dose],
                )
                self._add_cases(
                    plot, dose, cases, f"Tab1_case{{case}}_{name_obs}_collected"
                )

        return {name: fig}

    def _add_cases(self, plot: Plot, dose: int, cases: list[int], dataset: str) -> None:
        """Add the cases of a dose to a plot, with one legend entry per dose.

        Case 5 (low-sodium diet) has a marker and an entry of its own.
        """
        for k, case in enumerate(cases):
            if case == 5:
                label: str | None = f"{dose} mg case 5 (low-sodium diet)"
            else:
                label = f"{dose} mg cases" if k == 0 else None
            plot.add_data(
                dataset=dataset.format(case=case),
                xid="time",
                yid="value",
                label=label,
                color=self.colors[dose],
                marker="x" if case == 5 else "o",
                linestyle="",
                alpha=0.6,
            )


if __name__ == "__main__":
    MODEL.run_experiments(Januszewicz1959, output_dir=Januszewicz1959.__name__)
