"""Simulation experiment of the study Patel1984."""

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


class Patel1984(HCTZSimulationExperiment):
    """Simulation experiment of Patel1984.

    Single oral dosing of 25, 50, 100, and 200mg HCTZ.

    Table IV gives the net increase of the sodium, potassium and chloride in
    the urine of the 12 hr after a dose over the urine of the 12 hr before it,
    of the same subjects. The simulation starts 12 hr before the dose and
    subtracts the urine before the dose from the urine at the dose, so that
    the sodium and chloride in the urine 12 hr after the dose are the net
    increases of the model.
    """

    doses: ClassVar[list[int]] = [0, 25, 50, 100, 200]
    forms: ClassVar[list[str]] = ["tab", "sus"]
    colors: ClassVar[list[str]] = [
        "black",
        "tab:blue",
        "tab:orange",
        "tab:green",
        "tab:red",
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig2", "Tab4"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                if label.startswith("amount"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[f"{fig_id}_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        for dose in self.doses:
            simulations[f"hctz{dose}"] = Simulation(
                time_unit="hr",
                end=12 + 50,
                preinit_changes=self.default_changes(),
                changes=[
                    Change(
                        12,
                        {
                            "PODOSE_hctz": Q(dose, "mg"),
                            # the net increase over the 12 hr before the dose
                            "na_urine": "-na_urine",
                            "cl_urine": "-cl_urine",
                        },
                    )
                ],
                time_shift=-12,
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        # plasma
        for dose in self.doses[:-1]:
            if dose == 0:
                continue
            for form in iter(self.forms):
                mappings[f"fm_{dose}_{form}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"Fig1_hctz{dose}_{form}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_hctz{dose}", xid="time", yid="[Cve_hctz]"
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.PLASMA,
                        application_form=ApplicationForm.TABLET
                        if form == "tab"
                        else ApplicationForm.SUSPENSION,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.NONE,
                    ),
                )
                # Na urine
                mappings[f"fm_Naurine_{dose}_{form}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"Tab4_increase_Naurine_HCTZ{dose}_{form}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_hctz{dose}", xid="time", yid="na_urine"
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.URINE,
                        application_form=ApplicationForm.TABLET
                        if form == "tab"
                        else ApplicationForm.SUSPENSION,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.NONE,
                    ),
                )

                # Cl urine
                mappings[f"fm_Clurine_{dose}_{form}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"Tab4_increase_Clurine_HCTZ{dose}_{form}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_hctz{dose}", xid="time", yid="cl_urine"
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.URINE,
                        application_form=ApplicationForm.TABLET
                        if form == "tab"
                        else ApplicationForm.SUSPENSION,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.NONE,
                    ),
                )

        # urine
        for dose in self.doses:
            if dose == 0:
                continue
            for form in iter(self.forms):
                mappings[f"fm_{dose}_{form}_urine"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"Fig2_amount_cumulative_hctz{dose}_{form}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_hctz{dose}", xid="time", yid="Aurine_hctz"
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.URINE,
                        application_form=ApplicationForm.TABLET
                        if form == "tab"
                        else ApplicationForm.SUSPENSION,
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
        return {
            **self._figure_Fig1(),
            **self._figure_Fig2(),
            **self._figure_Tab4(),
        }

    def _figure_Fig1(self) -> dict[str, Figure]:
        name = "Fig1"
        fig = Figure(
            experiment=self,
            sid=name,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)

        # simulation
        for kd, dose in enumerate(self.doses[:-1]):
            plots[0].add_data(
                task=f"task_hctz{dose}",
                xid="time",
                yid="[Cve_hctz]",
                label=f"Sim {dose}",
                color=self.colors[kd],
            )
            # data
            if dose == 0:
                continue
            for form in iter(self.forms):
                plots[0].add_data(
                    dataset=f"Fig1_hctz{dose}_{form}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{dose} mg {form}",
                    marker="o" if form.endswith("tab") else "s",
                    color=self.colors[kd],
                )

        return {
            name: fig,
        }

    def _figure_Fig2(self) -> dict[str, Figure]:
        name = "Fig2"
        fig = Figure(
            experiment=self,
            sid=name,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", max=70), legend=True
        )
        plots[0].set_yaxis(label=self.label_hctz_urine, unit=self.unit_hctz_urine)

        # simulation
        for kd, dose in enumerate(self.doses):
            plots[0].add_data(
                task=f"task_hctz{dose}",
                xid="time",
                yid="Aurine_hctz",
                label=f"Sim {dose}",
                color=self.colors[kd],
            )
            # data
            if dose == 0:
                continue
            for form in iter(self.forms):
                plots[0].add_data(
                    dataset=f"Fig2_amount_cumulative_hctz{dose}_{form}",
                    xid="time",
                    yid="mean",
                    yid_sd=None,
                    count="count",
                    label=f"{dose} mg {form}",
                    marker="o" if form.endswith("tab") else "s",
                    color=self.colors[kd],
                )

        return {
            name: fig,
        }

    def _figure_Tab4(self) -> dict[str, Figure]:
        name = "Tab4"
        fig = Figure(
            experiment=self,
            sid=name,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
            settings={"legend_scope": "row"},
        )

        # the urine from 12 hr before the dose, minus the urine before the dose
        # from the dose on: the net increase after the dose
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", min=-13, max=13), legend=True
        )
        plots[0].set_yaxis(
            label="Sodium urine\n(net increase)", unit="mmole", min=-100, max=300
        )
        plots[1].set_yaxis(
            label="Chloride urine\n(net increase)", unit="mmole", min=-250, max=400
        )

        # simulation
        for kd, dose in enumerate(self.doses[:-1]):
            plots[0].add_data(
                task=f"task_hctz{dose}",
                xid="time",
                yid="na_urine",
                label=f"Sim {dose}",
                color=self.colors[kd],
            )

            plots[1].add_data(
                task=f"task_hctz{dose}",
                xid="time",
                yid="cl_urine",
                label=f"Sim {dose}",
                color=self.colors[kd],
            )

            # data
            if dose == 0:
                continue
            for form in iter(self.forms):
                plots[0].add_data(
                    dataset=f"Tab4_increase_Naurine_HCTZ{dose}_{form}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{dose} mg {form}",
                    marker="o" if form.endswith("tab") else "s",
                    color=self.colors[kd],
                    linestyle="",
                )

                plots[1].add_data(
                    dataset=f"Tab4_increase_Clurine_HCTZ{dose}_{form}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{dose} mg {form}",
                    marker="o" if form.endswith("tab") else "s",
                    color=self.colors[kd],
                    linestyle="",
                )
        return {
            name: fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Patel1984, output_dir=Patel1984.__name__)
