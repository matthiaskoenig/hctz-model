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


class Beermann1977a(HCTZSimulationExperiment):
    """Simulation experiment of Beermann1977a.

    HCTZ in various single oral doses 12.5, 25, 50 and 75 mg.
    """
    colors_dose = {
        0: "black",
        12.5: "tab:blue",
        25: "tab:orange",
        50: "tab:green",
        75: "tab:red",
    }
    doses = list(colors_dose.keys())



    # Figure 1_2
    individuals_fig1_2 = ["HD", "MLL"]
    info_fig1_2 = {
        "[Cve_hctz]": "hctz25",  # plasma concentration
        "KI__HCTZEX": "excretion_hctz25",  # excretion rate
    }
    # Figure 5
    info_fig5 = {
        "Vurine": "urinvol",  # urine volume
        "na_urine": "aurine_na",  # cumulative amount of sodium in urine
    }
    # Table 4
    markers_tab4 = {
        "IJ": "o",
        "YO": "D",
        "MLL": "*",
        "ACL": "x",
        "HD": "v",
        "KCL": "^",
        "AH": ">",
        "LE": "<",
    }
    subjects_tab4 = list(markers_tab4.keys())

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1_2", "Fig5tc", "Tab4", "Tab4mean"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                if (
                        label.startswith("hctz")
                        or label.startswith("excretion_")
                        or label.startswith("amount")
                ):
                    dset.unit_conversion("value", 1 / self.Mr.hctz)
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

        # Figure 1_2
        for k, sid in enumerate(self.info_fig1_2):
            name = self.info_fig1_2[sid]
            for individual in self.individuals_fig1_2:

                mappings[f"fm_Fig1_2_{name}_{individual}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"Fig1_2_{name}_{individual}",
                        xid="time",
                        yid="value",
                        count="count",
                    ),
                    observable=FitData(self, task=f"task_hctz25", xid="time", yid=sid),
                    metadata=HCTZMappingMetaData(
                        tissue=Tissue.URINE if "excretion" in name else Tissue.PLASMA,
                        application_form=ApplicationForm.TABLET,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.NONE,
                    ),
                )

        # Figure 5
        for kd, dose in enumerate(self.doses):
            dose_str = str(dose).replace('.', '_')
            for k, sid in enumerate(self.info_fig5):
                name = self.info_fig5[sid]
                mappings[f"fm_Fig5tc_{dose_str}_{name}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"Fig5tc_{dose_str}_{name}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_hctz{dose}", xid="time", yid=sid
                    ),
                    metadata=HCTZMappingMetaData(
                        tissue=Tissue.URINE,
                        application_form=ApplicationForm.TABLET,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.NONE,
                    ),
                )

        # Table 4
        for dose in self.doses:
            dose_str = str(dose).replace('.', '_')
            if dose == 0:
                continue

            # data (mean)
            mappings[f"fm_Tab4_amount_HCTZ{dose}_mean"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Tab4_amount_HCTZ{dose_str}_mean",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(self, task=f"task_hctz{dose}", xid="time", yid="Aurine_hctz"),
                metadata=HCTZMappingMetaData(
                    tissue=Tissue.URINE,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.NONE,
                ),
            )

            # data (individual)
            for k, subject in enumerate(self.subjects_tab4):
                # HD and AH missing in 12.5 mg
                if dose == 12.5 and subject in {"HD", "AH"}:
                    continue

                mappings[f"fm_Tab4_amount_HCTZ{dose}_{subject}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"Tab4_amount_HCTZ{dose_str}_{subject}",
                        xid="time",
                        yid="value",
                        yid_sd=None,
                        count="count",
                    ),
                    observable=FitData(self, task=f"task_hctz{dose}", xid="time", yid="Aurine_hctz"),
                    metadata=HCTZMappingMetaData(
                        tissue=Tissue.URINE,
                        application_form=ApplicationForm.TABLET,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.NONE,
                    ),
                )

        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_Fig1_2(),
            **self.figure_Fig5tc(),
            **self.figure_Tab4(),
        }

    def figure_Fig1_2(self) -> Dict[str, Figure]:
        name = "Fig1_2"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=2,
            num_cols=1,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)
        plots[1].set_yaxis(self.label_hctz_excretion_urine, unit=self.unit_hctz_excretion_urine)

        for k, sid in enumerate(self.info_fig1_2):
            name = self.info_fig1_2[sid]

            for individual in self.individuals_fig1_2:
                # simulation
                plots[k].add_data(
                    task=f"task_hctz25",
                    xid="time",
                    yid=sid,
                    label=f"Sim {individual}",
                    color=self.colors_dose[25],
                )

                # data
                plots[k].add_data(
                    dataset=f"Fig1_2_{name}_{individual}",
                    xid="time",
                    yid="value",
                    yid_sd=None,
                    count="count",
                    label=individual,
                    marker= "v" if "HD" in individual else "*",
                    color=self.colors_dose[25],
                ),

        return {
            fig.sid: fig,
        }

    def figure_Fig5tc(self) -> Dict[str, Figure]:
        name = "Fig5tc"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=2,
            num_cols=1,
            name=f"{self.__class__.__name__} {name}",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time, min=-0.5, max=10.5), legend=True)
        plots[0].set_yaxis(label=self.label_urine_volume, unit=self.unit_urine_volume)
        plots[1].set_yaxis(label=self.label_na_urine, unit=self.unit_na_urine)
        plots[0].yaxis.max = 3000
        plots[1].yaxis.max = 400

        for kd, dose in enumerate(self.doses):
            for k, sid in enumerate(self.info_fig5):
                name = self.info_fig5[sid]
                # simulation
                plots[k].add_data(
                    task=f"task_hctz{dose}",
                    xid="time",
                    yid=sid,
                    label=f"Sim {dose}",
                    color=self.colors_dose[dose],
                )
                # data
                plots[k].add_data(
                    dataset=f"Fig5tc_{str(dose).replace('.', '_')}_{name}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"hctz {dose} mg",
                    color=self.colors_dose[dose],
                )

        return {
            fig.sid: fig,
        }

    def figure_Tab4(self) -> Dict[str, Figure]:
        name = "Tab4"
        fig = Figure(
            experiment=self,
            sid=name,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz_urine, unit=self.unit_hctz_urine)

        for dose in self.doses:
            dose_str = str(dose).replace('.', '_')
            if dose == 0:
                continue

            # simulation
            plots[0].add_data(
                task=f"task_hctz{dose}",
                xid="time",
                yid="Aurine_hctz",
                label=f"Sim {dose}",
                color=self.colors_dose[dose],
            )
            # data (individual)
            for k, subject in enumerate(self.subjects_tab4):
                # HD and AH missing in 12.5 mg
                if dose == 12.5 and subject in {"HD", "AH"}:
                    continue

                plots[0].add_data(
                    dataset=f"Tab4_amount_HCTZ{dose_str}_{subject}",
                    xid="time",
                    yid="value",
                    yid_sd=None,
                    count="count",
                    label=None,
                    linestyle="",
                    marker=self.markers_tab4[subject],
                    color=self.colors_dose[dose],
                    markersize=4
               )

            # data (mean)
            plots[0].add_data(
                dataset=f"Tab4_amount_HCTZ{dose_str}_mean",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"hctz {dose} mg",
                marker="s",
                linestyle="",
                color=self.colors_dose[dose],
            )

        return {
                fig.sid: fig,
        }

if __name__ == "__main__":
    run_experiments(Beermann1977a, output_dir=Beermann1977a.__name__)
