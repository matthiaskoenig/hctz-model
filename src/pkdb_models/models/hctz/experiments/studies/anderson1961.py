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


class Anderson1961(HCTZSimulationExperiment):
    """Simulation experiment of Anderson1961.

    C14-labeled hydrochlorothiazide was administered orally and intravenously to 5 healthy controls
    and 14 patients with cardiac/renal/hepatic impairment.
    """

    dose = 50  # mg
    routes = [
        "po",
        "iv",
    ]
    markers = [">", "o", "^", "*", "<"]
    severities = ["mild", "moderate", "severe"]
    colors = {
        "control": "black",

        "cardiac": "tab:red",
        "cardiac mild": HCTZSimulationExperiment.cardiac_colors["Mild cardiac impairment"],
        "cardiac moderate": HCTZSimulationExperiment.cardiac_colors["Moderate cardiac impairment"],
        "cardiac severe": HCTZSimulationExperiment.cardiac_colors["Severe cardiac impairment"],

        "renal": "tab:green",
        "renal mild": HCTZSimulationExperiment.renal_colors["Mild renal impairment"],
        "renal moderate": HCTZSimulationExperiment.renal_colors["Moderate renal impairment"],
        "renal severe": HCTZSimulationExperiment.renal_colors["Severe renal impairment"],

        "hepatic": "tab:blue",
        "hepatic mild": HCTZSimulationExperiment.cirrhosis_colors["Mild cirrhosis"],
        "hepatic moderate": HCTZSimulationExperiment.cirrhosis_colors["Moderate cirrhosis"],
        "hepatic severe": HCTZSimulationExperiment.cirrhosis_colors["Severe cirrhosis"],
    }
    patients = {
        "po": {
            "control": ["1", "3", "4", "5"],
            "cardiac": ["6", "7", "8"],
            "renal": ["9"],
            "hepatic": ["12"],
        },
        "iv": {
            "control": ["2"],
            "cardiac": ["8A", "8B"],
            "renal": ["10", "11"],
            "hepatic": ["12" ,"13A", "13B", "14", "15"],
        }
    }
    interventions = ["control", "cardiac", "renal", "hepatic"]
    diseases = ["cardiac", "hepatic", "renal"]

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab1", "Tab1A", "Tab1B"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("amount"):
                    if fig_id == "Tab1":
                        dset.unit_conversion("value", 1 / self.Mr.hctz)
                    if fig_id == "Tab1A":
                        dset.unit_conversion("mean", 1 / self.Mr.hctz)
                elif label.startswith("cmax"):
                    if fig_id == "Tab1B":
                        dset.unit_conversion("value", 1 / self.Mr.hctz)
                    if fig_id == "Tab1A":
                        dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[label] = dset

        # print(dsets.keys())
        # print(dsets)
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        for route in self.routes:
            for intervention in self.interventions:
                for severity in self.severities:
                    if intervention == "control" and severity != "mild":
                        continue

                    if intervention == "control":
                        changes = {}
                    elif intervention == "cardiac":
                        changes = {
                            "f_cardiac_function": Q_(self.cardiac_map[f"{severity.title()} cardiac impairment"]),
                            # FIXME: handle reduced fraction absorbed ?!
                            # "GU__F_hctz_abs": Q_(0.427, "dimensionless"),  # assumption from recovery [Beermann1979]
                            # "GU__F_hctz_abs": Q_(60 / 101 * 0.75, "dimensionless"),
                        }
                    elif intervention == "renal":
                        changes = {
                            "KI__f_renal_function": Q_(self.renal_map[f"{severity.title()} renal impairment"])
                        }
                    elif intervention == "hepatic":
                        changes = {
                            "f_cirrhosis": Q_(self.cirrhosis_map[f"{severity.title()} cirrhosis"])
                        }
                    else:
                        raise ValueError(f"{intervention} is not a valid intervention")

                    if intervention == "control":
                        label = intervention
                    else:
                        label = f"{intervention}_{severity}"

                    tcsims[f"hctz_{route}{self.dose}_{label}"] = TimecourseSim(
                        Timecourse(
                            start=0,
                            end=180 * 60,  # [min]
                            steps=2000,
                            changes={
                                **self.default_changes(),
                                f"{route.upper()}DOSE_hctz": Q_(self.dose, "mg"),
                                **changes
                            },
                        )
                    )
        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}
        for route in self.routes:
            for disease in self.diseases:
                for subset in [disease, "control"]:
                    if subset == "cardiac":
                        h_label = Health.CARDIAC_IMPAIRMENT
                    elif subset == "renal":
                        h_label = Health.RENAL_IMPAIRMENT
                    elif subset == "hepatic":
                        h_label = Health.CIRRHOSIS
                    elif subset == "control":
                        h_label = Health.HEALTHY
                    else:
                        raise ValueError(f"{subset} is not a valid disease")

                    # mean data HCTZ Urine
                    mappings[(f"fm_amount_HCTZ{route}_{subset}")] = FitMapping(
                        self,
                        reference=FitData(
                            self,
                            dataset=f"amount_HCTZ{route}_{subset}",
                            xid="time",
                            yid="mean",
                            yid_sd="mean_sd",
                            count="count",
                        ),
                        observable=FitData(
                            self,
                            task=f"task_hctz_{route}{self.dose}_control" if subset == "control" else f"task_hctz_{route}{self.dose}_{disease}_severe",
                            xid="time",
                            yid="Aurine_hctz",
                        ),
                        metadata=HCTZMappingMetaData(
                                tissue=Tissue.URINE,
                                application_form=ApplicationForm.TABLET if route == "po" else ApplicationForm.SOLUTION,
                                route=Route.PO if route == "po" else Route.IV,
                                dosing=Dosing.SINGLE,
                                health=h_label,
                                fasting=Fasting.NR,
                                coadministration=Coadministration.NONE,
                        ),
                    )

                    # individual data HCTZ Urine healthy control
                    for subject in self.patients[route][subset]:
                        mappings[(f"fm_amount_HCTZ{route}_{subject}")] = FitMapping(
                            self,
                            reference=FitData(
                                self,
                                dataset=f"amount_HCTZ{route}_{subject}",
                                xid="time",
                                yid="value",
                                yid_sd=None,
                                count="count",
                            ),
                            observable=FitData(
                                self,
                                task=f"task_hctz_{route}{self.dose}_control" if subset == "control" else f"task_hctz_{route}{self.dose}_{disease}_severe",
                                xid="time",
                                yid="Aurine_hctz",
                            ),
                            metadata=HCTZMappingMetaData(
                                tissue=Tissue.URINE,
                                application_form=ApplicationForm.TABLET if route == "po" else ApplicationForm.SOLUTION,
                                route=Route.PO if route == "po" else Route.IV,
                                dosing=Dosing.SINGLE,
                                health=h_label,
                                fasting=Fasting.NR,
                                coadministration=Coadministration.NONE,
                            ),
                        )

                    # individual data HCTZ Plasma
                        mappings[(f"fm_cmax_HCTZ{route}_{subject}")] = FitMapping(
                            self,
                            reference=FitData(
                                self,
                                dataset=f"cmax_HCTZ{route}_{subject}",
                                xid="time",
                                yid="value",
                                yid_sd=None,
                                count="count",
                            ),
                            observable=FitData(
                                self,
                                task=f"task_hctz_{route}{self.dose}_control" if subset == "control" else f"task_hctz_{route}{self.dose}_{disease}_severe",
                                xid="time",
                                yid="[Cve_hctz]",
                            ),
                            metadata=HCTZMappingMetaData(
                                tissue=Tissue.PLASMA,
                                application_form=ApplicationForm.TABLET if route == "po" else ApplicationForm.SOLUTION,
                                route=Route.PO if route == "po" else Route.IV,
                                dosing=Dosing.SINGLE,
                                health=h_label,
                                fasting=Fasting.NR,
                                coadministration=Coadministration.NONE,
                            ),
                        )

        return mappings


    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_Tab1urine(),
            **self.figure_Tab1plasma(),
            # **self.figure_Tab1_hep_ren(),
        }


    def figure_Tab1urine(self) -> Dict[str, Figure]:

        figures = {}
        for disease in self.diseases:

            fig = Figure(
                experiment=self,
                sid=f"{disease} urine",
                num_cols=2,
                name=f"{self.__class__.__name__} HCTZ urine {disease} impairment",
            )
            plots = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr"),
                yaxis=Axis(self.label_hctz_urine, unit=self.unit_hctz_urine),
                legend=True
            )

            for kr, route in enumerate(self.routes):
                # simulation
                for severity in self.severities:
                    plots[kr].add_data(
                        task=f"task_hctz_{route}{self.dose}_{disease}_{severity}",
                        xid="time",
                        yid="Aurine_hctz",
                        label=f"Sim {route} {disease} {severity}",
                        color=self.colors[f"{disease} {severity}"],
                    )
                plots[kr].add_data(
                    task=f"task_hctz_{route}{self.dose}_control",
                    xid="time",
                    yid="Aurine_hctz",
                    label=f"Sim {route} control",
                    color=self.colors["control"],
                )

                # mean data
                for subset in [disease, "control"]:
                    plots[kr].add_data(
                        dataset=f"amount_HCTZ{route}_{subset}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        label=subset,
                        linestyle="-",
                        color=self.colors[subset],
                    )
                # individual data
                for subset in [disease, "control"]:
                    for ks, subject in enumerate(self.patients[route][subset]):
                        plots[kr].add_data(
                            dataset=f"amount_HCTZ{route}_{subject}",
                            xid="time",
                            yid="value",
                            yid_sd=None,
                            label=f"{subject}",
                            marker=self.markers[ks],
                            color=self.colors[subset],
                        )

            figures[fig.sid] = fig

        return figures

    def figure_Tab1plasma(self) -> Dict[str, Figure]:

        figures = {}
        for disease in self.diseases:

            fig = Figure(
                experiment=self,
                sid=f"{disease} plasma",
                num_cols=2,
                name=f"{self.__class__.__name__} HCTZ plasma {disease} impairment",
            )
            plots = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr", min=-1, max=24),
                yaxis=Axis(self.label_hctz, unit=self.unit_hctz),
                legend=True
            )

            for kr, route in enumerate(self.routes):
                # simulation
                for severity in self.severities:
                    plots[kr].add_data(
                        task=f"task_hctz_{route}{self.dose}_{disease}_{severity}",
                        xid="time",
                        yid="[Cve_hctz]",
                        label=f"Sim {route} {disease} {severity}",
                        color=self.colors[f"{disease} {severity}"],
                    )
                plots[kr].add_data(
                    task=f"task_hctz_{route}{self.dose}_control",
                    xid="time",
                    yid="[Cve_hctz]",
                    label=f"Sim {route} control",
                    color=self.colors["control"],
                )

                # individual data
                for subset in [disease, "control"]:
                    for ks, subject in enumerate(self.patients[route][subset]):
                        plots[kr].add_data(
                            dataset=f"cmax_HCTZ{route}_{subject}",
                            xid="time",
                            yid="value",
                            yid_sd=None,
                            label=f"{subject}",
                            marker=self.markers[ks],
                            color=self.colors[subset],
                            linestyle=""
                        )

            figures[fig.sid] = fig

        return figures

    # def figure_Tab1_hep_ren(self) -> Dict[str, Figure]:
    #
    #     figures = {}
    #
    #     fig = Figure(
    #         experiment=self,
    #         sid=f"hepatic+renal plasma",
    #         num_rows=2,
    #         num_cols=2,
    #         name=f"{self.__class__.__name__} HCTZ hepatic + renal impairment",
    #     )
    #     plots = fig.create_plots(
    #         xaxis=Axis(self.label_time, unit="hr"),
    #         legend=True
    #     )
    #
    #     plots[0].set_yaxis(label=self.label_hctz_urine, unit=self.unit_hctz_urine)
    #     plots[1].set_yaxis(label=self.label_hctz_urine, unit=self.unit_hctz_urine)
    #     plots[2].set_yaxis(label=self.label_hctz, unit=self.unit_hctz)
    #     plots[3].set_yaxis(label=self.label_hctz, unit=self.unit_hctz)
    #
    #     for kr, route in enumerate(self.routes):
    #         # simulation urine
    #         for severity in self.severities:
    #             plots[kr].add_data(
    #                 task=f"task_hctz_{route}{self.dose}_hepatic_{severity}",
    #                 xid="time",
    #                 yid="Aurine_hctz",
    #                 label=f"Sim {route} hepatic {severity}",
    #                 color=self.colors[f"hepatic {severity}"],
    #             )
    #         plots[kr].add_data(
    #             task=f"task_hctz_{route}{self.dose}_control",
    #             xid="time",
    #             yid="Aurine_hctz",
    #             label=f"Sim {route} control",
    #             color=self.colors["control"],
    #         )
    #
    #         # simulation plasma
    #         for severity in self.severities:
    #             plots[kr+2].add_data(
    #                 task=f"task_hctz_{route}{self.dose}_hepatic_{severity}",
    #                 xid="time",
    #                 yid="[Cve_hctz]",
    #                 label=f"Sim {route} hepatic {severity}",
    #                 color=self.colors[f"hepatic {severity}"],
    #             )
    #         plots[kr+2].add_data(
    #             task=f"task_hctz_{route}{self.dose}_control",
    #             xid="time",
    #             yid="[Cve_hctz]",
    #             label=f"Sim {route} control",
    #             color=self.colors["control"],
    #         )
    #
    #         # mean data urine
    #         for subset in ["hepatic", "renal", "control"]:
    #             plots[kr].add_data(
    #                 dataset=f"amount_HCTZ{route}_{subset}",
    #                 xid="time",
    #                 yid="mean",
    #                 yid_sd="mean_sd",
    #                 label=subset,
    #                 linestyle="-",
    #                 color=self.colors[subset],
    #             )
    #         # individual data urine
    #         for subset in ["hepatic", "renal", "control"]:
    #             for ks, subject in enumerate(self.patients[route][subset]):
    #                 plots[kr].add_data(
    #                     dataset=f"amount_HCTZ{route}_{subject}",
    #                     xid="time",
    #                     yid="value",
    #                     yid_sd=None,
    #                     label=f"{subject}",
    #                     marker=self.markers[ks],
    #                     color=self.colors[subset],
    #                 )
    #
    #
    #         # individual data plasma
    #         for subset in ["hepatic", "renal", "control"]:
    #             for ks, subject in enumerate(self.patients[route][subset]):
    #                 plots[kr+2].add_data(
    #                     dataset=f"cmax_HCTZ{route}_{subject}",
    #                     xid="time",
    #                     yid="value",
    #                     yid_sd=None,
    #                     label=f"{subject}",
    #                     marker=self.markers[ks],
    #                     color=self.colors[subset],
    #                     linestyle=""
    #                 )
    #
    #     figures[fig.sid] = fig
    #
    #     return figures


if __name__ == "__main__":
    run_experiments(Anderson1961, output_dir=Anderson1961.__name__)
