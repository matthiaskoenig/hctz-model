from typing import Dict

import pandas as pd
from sbmlsim.data import DataSet, load_pkdb_dataframe
from sbmlsim.fit import FitMapping, FitData

from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Timecourse, TimecourseSim
from sbmlutils.console import console

from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)
from pkdb_models.models.hctz.experiments.metadata import (
    Health, Tissue, ApplicationForm,
    Dosing, Route, Fasting, Coadministration,
    HCTZMappingMetaData,
)
from pkdb_models.models.hctz.helpers import run_experiments


class Patel1984(HCTZSimulationExperiment):
    """Simulation experiment of Patel1984.

    Single oral dosing of 25, 50, 100, and 200mg HCTZ.
    """

    doses = [0, 25, 50, 100, 200]
    forms = ["tab", "sus"]
    colors = ["black", "tab:blue", "tab:orange", "tab:green", "tab:red"]

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig2", "Tab4"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                if label.startswith("amount"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[f"{fig_id}_{label}"] = dset

        # print(dsets.keys())
        # print(dsets)
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        for dose in self.doses:
            tcsims[f"hctz{dose}"] = TimecourseSim(
                Timecourse(
                    start=0,
                    end=50 * 60,  # [min]
                    steps=500,
                    changes={
                        **self.default_changes(),
                        "PODOSE_hctz": Q_(dose, "mg"),
                    },
                )
            )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}

        # plasma
        for kd, dose in enumerate(self.doses[:-1]):
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
                    metadata=HCTZMappingMetaData(
                        tissue=Tissue.PLASMA,
                        application_form=ApplicationForm.TABLET if form == "tab" else ApplicationForm.SUSPENSION,
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
                    metadata=HCTZMappingMetaData(
                        tissue=Tissue.PLASMA,
                        application_form=ApplicationForm.TABLET if form == "tab" else ApplicationForm.SUSPENSION,
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
                    metadata=HCTZMappingMetaData(
                        tissue=Tissue.PLASMA,
                        application_form=ApplicationForm.TABLET if form == "tab" else ApplicationForm.SUSPENSION,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.NONE,
                    ),
                )

        # urine
        for kd, dose in enumerate(self.doses):
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
                    metadata=HCTZMappingMetaData(
                        tissue=Tissue.URINE,
                        application_form=ApplicationForm.TABLET if form == "tab" else ApplicationForm.SUSPENSION,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.NONE,
                    ),
                )

        # console.print(mappings)
        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_Fig1(),
            **self.figure_Fig2(),
            **self.figure_Tab4(),
        }

    def figure_Fig1(self) -> Dict[str, Figure]:
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
            fig.sid: fig,
        }

    def figure_Fig2(self) -> Dict[str, Figure]:
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
            fig.sid: fig,
        }


    def figure_Tab4(self) -> Dict[str, Figure]:
        name = "Tab4"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", max=24), legend=True
        )
        plots[0].set_yaxis(label="Sodium urine", unit="mmole")
        plots[1].set_yaxis(label="Chloride urine", unit="mmole")


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
                )
        return {
            fig.sid: fig,
        }

if __name__ == "__main__":
    run_experiments(Patel1984, output_dir=Patel1984.__name__)
