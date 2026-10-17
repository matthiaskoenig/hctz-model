"""Simulation experiment of the study Beermann1976.

Fig2 (subject 4, 5 mg oral 14C-hct) shows radioactivity: plasma and
erythrocytes in cpm/ml, the urinary excretion of label in cpm x 10^3 x min^-1.
The data (``valuecpm``) are converted with the specific activity of the dose,
10 µCi in 5 mg = 2 µCi/mg:

2 µCi/mg x 2.22e6 dpm/µCi x 297.74 mg/mmol = 1.322e9 dpm/mmol = 1322 dpm/nmol
c [nmol/l] = A [cpm/ml] x 1000 ml/l / 1322 dpm/nmol
e [µmol/min] = R [cpm/min] / 10 / 1322 dpm/nmol / 1000

The counting efficiency is not reported and is taken as 1 (cpm = dpm), so the
values are lower bounds by the efficiency. The urine axis is read as
cpm x 10^2 x min^-1: with 10^3 the label excreted in 0-9.4 h would be 475 % of
the dose (Table I: 60.2 % in 12 h) and the renal clearance at 1 h 2.8 l/min;
with 10^2 it is 47.5 % and 276 ml/min. The curation in pkdb_data
(hydrochlorothiazide/Beermann1976) keeps the counts and these calculated
values, with the argument in the row comments. The earlier conversion with the
maximum specific activity of 14C (62.4 mCi/mmol) and counts per second divided
by 60 put the concentrations 29 times too low and the excretion 343 times too
high.
"""

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


class Beermann1976(HCTZSimulationExperiment):
    """Simulation experiment of Beermann1976.

    Oral dosing of 5, 50, 75 mg HCTZ and intravenous dosing of 1 and 35 mg HCTZ.

    The subjects 1 to 6 were healthy volunteers. Subjects 1 to 5 took 5 mg
    14C-HCTZ dissolved in 100 ml water (p. 532, 0.05 mg/ml to keep the drug in
    solution, p. 536), subjects 4 and 5 were given 35 mg and 1 mg 14C-HCTZ iv,
    subject 6 75 mg unlabeled HCTZ. The patients I to III were hypertensive and
    had been treated with 25 to 50 mg HCTZ daily for at least 3 months, with no
    other medication than potassium chloride; they took 50 mg 14C-HCTZ in a
    capsule (p. 532). Only the label is measured, and the label of a single
    dose is excreted as a single dose of HCTZ (linear kinetics), so the
    patients are simulated with a single dose without their chronic treatment.
    Patients I and III had a normal renal function, patient II a serum
    creatinine of 1.6 mg/dl (p. 532), a urinary recovery of 41.1 % in 4 days
    and an elimination rate during the first 12 hr about half that of the
    other subjects (p. 536).
    """

    doses: ClassVar[list[int]] = [
        5,
        50,
        75,
        35,
        1,
    ]
    routes: ClassVar[list[str]] = [
        "po",
        "po",
        "po",
        "iv",
        "iv",
    ]
    colors: ClassVar[dict[int, str]] = {
        5: "tab:blue",
        50: "tab:orange",
        75: "tab:red",
        35: "tab:green",
        1: "tab:brown",
    }
    #: the patients, hypertensive and on chronic HCTZ
    patients: ClassVar[list[str]] = ["I", "II", "III"]
    #: the renal function of patient II from his serum creatinine of 1.6 mg/dl
    #: (p. 532). Age, sex and body weight are not reported, so the clearance is
    #: estimated from the inverse proportionality of the serum creatinine to the
    #: glomerular filtration rate, with a serum creatinine of 1.0 mg/dl at the
    #: healthy rate: 101 ml/min x 1.0 / 1.6 = 63 ml/min
    crcl_II: ClassVar[float] = 101.0 * 1.0 / 1.6  # [ml/min]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab1A", "Fig2", "Fig3"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if fig_id == "Tab1A":
                    dset.unit_conversion("value", 1 / self.Mr.hctz)
                if fig_id == "Fig3" and label.startswith("hctz"):
                    dset.unit_conversion("value", 1 / self.Mr.hctz)

                dsets[label] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        for kd, dose in enumerate(self.doses):
            route = self.routes[kd]
            # the oral 5 mg were dissolved in water (p. 532), the 50 mg tablets
            parameter = {"iv": "IVDOSE_hctz", "po": "PODOSE_hctz"}[route]
            if route == "po" and dose == 5:
                parameter = "POSOLUTION_hctz"

            simulations[f"hctz_{route}{dose}"] = Simulation(
                time_unit="hr",
                end=180,
                steps=1000,
                preinit_changes={
                    **self.default_changes(),
                    parameter: Q(dose, "mg"),
                },
            )

        # patient II with his impaired renal function
        simulations["hctz_po50_II"] = Simulation(
            time_unit="hr",
            end=180,
            steps=1000,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_hctz": Q(50, "mg"),
                "f_renal_function": self.renal_function(self.crcl_II),
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        # urine and feces
        for dset_id in self._datasets:
            if not dset_id.startswith("amount"):
                continue

            tokens = dset_id.split("_")
            route = tokens[-2][-2:]
            dose = int(tokens[-2][4:-2])
            individual = tokens[-1]
            tissue = "urine" if "urine" in dset_id else "feces"
            # 5 mg dissolved in 100 ml water, 50 mg in a capsule (p. 532)
            if route == "iv" or dose == 5:
                application_form = ApplicationForm.SOLUTION
            else:
                application_form = ApplicationForm.CAPSULE
            patient = individual in self.patients
            task = f"task_hctz_{route}{dose}"
            if individual == "II":
                task = "task_hctz_po50_II"

            mappings[f"fm_hctz_{route}{dose}_{individual}_{tissue}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=dset_id,
                    xid="time",
                    yid="value",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=task,
                    xid="time",
                    yid=f"A{tissue}_hctz",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.URINE if tissue == "urine" else Tissue.FECES,
                    application_form=application_form,
                    route=Route.PO if route == "po" else Route.IV,
                    # the patients took HCTZ daily, the measured label is a
                    # single dose
                    dosing=Dosing.MULTIPLE if patient else Dosing.SINGLE,
                    health=Health.HYPERTENSION if patient else Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    # potassium chloride, the only other medication of the
                    # patients, has no member of the vocabulary and no known
                    # interaction with HCTZ
                    coadministration=Coadministration.NONE,
                ),
            )

        mappings["fm_hctz5po_4"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="hctz5po_4",
                xid="time",
                yid="value",
                count="count",
            ),
            observable=FitData(
                self, task="task_hctz_po5", xid="time", yid="[Cve_hctz]"
            ),
            metadata=PKPDMappingMetaData(
                tissue=Tissue.PLASMA,
                application_form=ApplicationForm.SOLUTION,
                route=Route.PO,
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                fasting=Fasting.FASTED,
                coadministration=Coadministration.NONE,
            ),
        )
        mappings["fm_excretion_hctz5po_4"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="excretion_hctz5po_4",
                xid="time",
                yid="value",
                count="count",
            ),
            observable=FitData(
                self, task="task_hctz_po5", xid="time", yid="KI__HCTZEX"
            ),
            metadata=PKPDMappingMetaData(
                tissue=Tissue.URINE,
                application_form=ApplicationForm.SOLUTION,
                route=Route.PO,
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                fasting=Fasting.FASTED,
                coadministration=Coadministration.NONE,
            ),
        )

        mappings["fm_hctz75po_6"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="hctz75_po_6",
                xid="time",
                yid="value",
                count="count",
            ),
            observable=FitData(
                self, task="task_hctz_po75", xid="time", yid="[Cve_hctz]"
            ),
            metadata=PKPDMappingMetaData(
                tissue=Tissue.PLASMA,
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
        return {
            **self._figure_Tab1A(),
            **self._figure_Fig2(),
            **self._figure_Fig3(),
        }

    def _figure_Tab1A(self) -> dict[str, Figure]:
        name = "Tab1A"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=4,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(label=self.label_hctz_urine, unit=self.unit_hctz_urine)
        plots[1].set_yaxis(label=self.label_hctz_feces, unit=self.unit_hctz_feces)
        plots[2].set_yaxis(label=self.label_hctz_urine, unit=self.unit_hctz_urine)
        plots[3].set_yaxis(
            label=self.label_hctz_feces, unit=self.unit_hctz_feces, min=-0.5, max=10.5
        )

        # simulation
        for kd, dose in enumerate(self.doses):
            route = self.routes[kd]
            kr = 0 if route == "po" else 1

            for ky, yid in enumerate(["Aurine_hctz", "Afeces_hctz"]):
                plots[kr * 2 + ky].add_data(
                    task=f"task_hctz_{route}{dose}",
                    xid="time",
                    yid=yid,
                    label=f"Sim {route}{dose} mg",
                    color=self.colors[dose],
                )
        for ky, yid in enumerate(["Aurine_hctz", "Afeces_hctz"]):
            plots[ky].add_data(
                task="task_hctz_po50_II",
                xid="time",
                yid=yid,
                label="Sim po50 mg II",
                color=self.colors[50],
                linestyle="--",
            )

        # data urine
        for dset_id in self._datasets:
            if not dset_id.startswith("amount"):
                continue
            tokens = dset_id.split("_")
            route = tokens[-2][-2:]
            dose = int(tokens[-2][4:-2])
            individual = tokens[-1]
            kr = 0 if route == "po" else 1
            ky = 0 if "urine" in dset_id else 1

            plots[kr * 2 + ky].add_data(
                dataset=dset_id,
                xid="time",
                yid="value",
                count="count",
                label=f"{route}{dose} mg {individual}",
                color=self.colors[dose],
            )

        return {
            name: fig,
        }

    def _figure_Fig2(self) -> dict[str, Figure]:

        # FIXME: conversion issues
        name = "Fig2"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", min=-0.1, max=25), legend=True
        )
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)
        plots[1].set_yaxis(
            self.label_hctz_excretion_urine, unit=self.unit_hctz_excretion_urine
        )

        # simulation
        for kp, yid in enumerate(["[Cve_hctz]", "KI__HCTZEX"]):
            plots[kp].add_data(
                task="task_hctz_po5",
                xid="time",
                yid=yid,
                label="Sim po5 mg",
                color=self.colors[5],
            )

        # data
        plots[0].add_data(
            dataset="hctz5po_4",
            xid="time",
            yid="value",
            count="count",
            label="po5 mg HCTZ",
            color=self.colors[5],
        )

        plots[1].add_data(
            dataset="excretion_hctz5po_4",
            xid="time",
            yid="value",
            count="count",
            label="5 mg HCTZ",
            color=self.colors[5],
        )

        return {
            name: fig,
        }

    def _figure_Fig3(self) -> dict[str, Figure]:
        name = "Fig3"
        fig = Figure(
            experiment=self,
            sid=name,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", min=-0.1, max=40), legend=True
        )
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)

        # simulation
        plots[0].add_data(
            task="task_hctz_po75",
            xid="time",
            yid="[Cve_hctz]",
            label="Sim po75 mg",
            color=self.colors[75],
        )

        # data
        plots[0].add_data(
            dataset="hctz75_po_6",
            xid="time",
            yid="value",
            count="count",
            label="po75 mg HCTZ",
            color=self.colors[75],
        )

        return {
            name: fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Beermann1976, output_dir=Beermann1976.__name__)
