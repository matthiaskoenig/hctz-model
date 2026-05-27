from typing import Dict

import pandas as pd
from sbmlsim.data import DataSet, load_pkdb_dataframe
from sbmlsim.fit import FitMapping, FitData

from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Timecourse, TimecourseSim

from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)
from pkdb_models.models.hctz.experiments.metadata import (
    Health, Tissue, ApplicationForm,
    Dosing, Route, Fasting, Coadministration,
    HCTZMappingMetaData,
)
from pkdb_models.models.hctz.helpers import run_experiments


class Ripley2000(HCTZSimulationExperiment):
    """Simulation experiment of Ripley2000.

    Single  oral dosing of 25mg HCTZ, comparing between black and white populations.
    """

    interventions = ["baseline", "hctz"]  # ["baseline", "diet", "hctz"] no diet data
    groups = ["black", "white"]
    positions = ["supine", "upright"]
    colors = {
        "baseline": "black",
        "diet": "gray",
        "hctz": "tab:blue",
    }
    markers = {
        "supine": "s",
        "upright": "o",
        "black": "<",
        "white": ">",
    }
    doses = {  # [mg]
        "baseline": 0,
        "diet": 25,
        "hctz": 25,
    }


    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab3", "Fig1_2", "Fig3"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                # elif fig_id == "Fig3" and label.startswith("renin"):
                #     dset.unit_conversion("mean", 1 / self.Mr.ren)
                # elif fig_id == "Fig3" and label.startswith("aldo"):
                #     dset.unit_conversion("mean", 1 / self.Mr.ald)
                dsets[f"{fig_id}_{label}"] = dset

        # print(dsets.keys())
        # print(dsets)
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        for intervention in self.interventions:
            dose = self.doses[intervention]
            tcsims[f"hctz{dose}_{intervention}"] = TimecourseSim(
                Timecourse(
                    start=0,
                    end=40 * 60,  # [min]
                    steps=500,
                    changes={
                        **self.default_changes(),
                        "PODOSE_hctz": Q_(dose, "mg"),

                        # # mean value of acute renin at baseline
                        # "ren_ref": Q_((0.99 + 1.53 + 1.53 + 2.29)/4, "ng/dl") / self.Mr.ren,  # HCTZ25 mono
                        # "[ren]": Q_((0.99 + 1.53 + 1.53 + 2.29)/4, "ng/dl") / self.Mr.ren,  # HCTZ25 mono
                        #
                        # # mean value of acute aldosterone at baseline
                        # "ald_ref": Q_((9.08 + 12.16 + 12.16 + 18.90)/4, "ng/ml") / self.Mr.ald,  # HCTZ25 mono
                        # "[ald]": Q_((9.08 + 12.16 + 12.16 + 18.90)/4, "ng/ml") / self.Mr.ald,  # HCTZ25 mono
                    },
                )
            )
        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}
        infos = [
            ("Tab3_hctz_aurine_black", "Aurine_hctz"),
            ("Tab3_hctz_aurine_white", "Aurine_hctz"),
            ("Fig1_2_sodium_baseline_black", "na_urine"),
            ("Fig1_2_sodium_baseline_white", "na_urine"),
            # ("Fig1_2_sodium_diet_black", "na_urine"),
            # ("Fig1_2_sodium_diet_white", "na_urine"),
            ("Fig1_2_sodium_hctz_black", "na_urine"),
            ("Fig1_2_sodium_hctz_white", "na_urine"),
            # ("Fig3_renin_plasma_hctz_black_supine", "[ren]"),
            # ("Fig3_renin_plasma_hctz_white_supine", "[ren]"),
            # ("Fig3_renin_plasma_hctz_black_upright", "[ren]"),
            # ("Fig3_renin_plasma_hctz_white_upright", "[ren]"),
            # ("Fig3_aldo_plasma_hctz_black_supine", "[ald]"),
            # ("Fig3_aldo_plasma_hctz_white_supine", "[ald]"),
            # ("Fig3_aldo_plasma_hctz_black_upright", "[ald]"),
            # ("Fig3_aldo_plasma_hctz_white_upright", "[ald]")
            ]

        # FIXME: use the correct simulations, i.e. diet, baseline or hctz!!

        for info in infos:
            (dset_id, yid) = info
            mappings[f"fm_{dset_id}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=dset_id,
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(self, task=f"task_hctz25_hctz", xid="time", yid=yid),
                metadata=HCTZMappingMetaData(
                    tissue=Tissue.URINE,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.NONE,
                ),
            )
        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_Tab3(),
            **self.figure_Fig1_2(),
            # **self.figure_Fig3(),
        }

    def figure_Tab3(self) -> Dict[str, Figure]:
        name = "Tab3"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.labels["Aurine_hctz"], self.units["Aurine_hctz"])

        # simulation
        for k, intervention in enumerate(self.interventions):
            dose = self.doses[intervention]
            plots[0].add_data(
                task=f"task_hctz{dose}_{intervention}",
                xid="time",
                yid="Aurine_hctz",
                label=f"Sim ({intervention})",
                color=self.colors[intervention],
            )

        # data
        for k, group in enumerate(self.groups):
            plots[0].add_data(
                dataset=f"Tab3_hctz_aurine_{group}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{group}",
                color=self.colors["hctz"],
                marker=self.markers[group],
                linestyle="",
            )
        return {
            fig.sid: fig,
        }

    def figure_Fig1_2(self) -> Dict[str, Figure]:
        name = "Fig1_2"
        fig = Figure(
            experiment=self,
            sid=name,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(label="Urine Sodium\n", unit="mmole")

        for k, intervention in enumerate(self.interventions):
            dose = self.doses[intervention]
            # simulation
            plots[0].add_data(
                task=f"task_hctz{dose}_{intervention}",
                xid="time",
                yid="na_urine",
                label=f"Sim",
                color=self.colors[intervention],
            )

            # data
            for group in self.groups:
                plots[0].add_data(
                    dataset=f"Fig1_2_sodium_{intervention}_{group}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{intervention} {group}",
                    color=self.colors[intervention],
                    marker=self.markers[group],
                )
        # URINE POTASSIUM
        # plots[1].add_data(
        #     dataset=f"Fig1_2_pot_{intervention}_{group}",
        #     xid="time",
        #     yid="mean",
        #     yid_sd="mean_sd",
        #     count="count",
        #     label=self.names[ks],
        #     color=self.color_hctz,
        # )

        return {
            fig.sid: fig,
        }

    # def figure_Fig3(self) -> Dict[str, Figure]:
    #     name = "Fig 3"
    #     fig = Figure(
    #         experiment=self,
    #         sid=name,
    #         num_rows=2,
    #         num_cols=1,
    #         name=f"{self.__class__.__name__} {name}",
    #     )
    #     plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
    #     plots[0].set_yaxis(self.labels["[ren]"], self.units["[ren]"])
    #     plots[1].set_yaxis(self.labels["[ald]"], self.units["[ald]"])
    #
    #     # simulation
    #     for k, intervention in enumerate(self.interventions):
    #         dose = self.doses[intervention]
    #         for k, sid in enumerate(["[ren]", "[ald]"]):
    #             plots[k].add_data(
    #                 task=f"task_hctz{dose}_{intervention}",
    #                 xid="time",
    #                 yid=sid,
    #                 label=f"Sim",
    #                 color=self.colors[intervention],
    #             )
    #
    #     # data
    #     for group in self.groups:
    #         for position in self.positions:
    #             for k, name in enumerate(["renin", "aldo"]):
    #
    #                 plots[k].add_data(
    #                     dataset=f"Fig3_{name}_plasma_hctz_{group}_{position}",
    #                     xid="time",
    #                     yid="mean",
    #                     yid_sd="mean_sd",
    #                     count="count",
    #                     label=f"{group} ({position})",
    #                     marker=self.markers[group],
    #                     color=self.colors["hctz"],
    #                 )
    #
    #     return {
    #         fig.sid: fig,
    #     }

if __name__ == "__main__":
    run_experiments(Ripley2000, output_dir=Ripley2000.__name__)
