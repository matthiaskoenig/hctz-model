"""Simulation experiment of the study Ripley2000."""

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


class Ripley2000(HCTZSimulationExperiment):
    """Simulation experiment of Ripley2000.

    Single  oral dosing of 25mg HCTZ, comparing between black and white populations.

    The patients had stage 1 or 2 hypertension (p. 158). The cumulative sodium
    after HCTZ is the 0-24 hr total of Fig1 with the 0-12 hr and 24-36 hr
    intervals of Fig2. Fig2 gives the SD of the interval, the data carry the SD
    of the cumulative value at 36 hr as sqrt(SD_0-24^2 + SD_24-36^2), the SD of
    the sum of independent intervals.
    """

    interventions: ClassVar[list[str]] = [
        "baseline",
        "hctz",
    ]  # ["baseline", "diet", "hctz"] no diet data
    groups: ClassVar[list[str]] = ["black", "white"]
    positions: ClassVar[list[str]] = ["supine", "upright"]
    colors: ClassVar[dict[str, str]] = {
        "baseline": "black",
        "diet": "gray",
        "hctz": "tab:blue",
    }
    markers: ClassVar[dict[str, str]] = {
        "supine": "s",
        "upright": "o",
        "black": "<",
        "white": ">",
    }
    doses: ClassVar[dict[str, int]] = {  # [mg]
        "baseline": 0,
        "diet": 25,
        "hctz": 25,
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab3", "Fig1_2", "Fig3"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                # elif fig_id == "Fig3" and label.startswith("renin"):
                #     dset.unit_conversion("mean", 1 / self.Mr.ren)
                # elif fig_id == "Fig3" and label.startswith("aldo"):
                #     dset.unit_conversion("mean", 1 / self.Mr.ald)
                dsets[f"{fig_id}_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        for intervention in self.interventions:
            dose = self.doses[intervention]
            simulations[f"hctz{dose}_{intervention}"] = Simulation(
                time_unit="hr",
                end=40,
                steps=500,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_hctz": Q(dose, "mg"),
                    # # mean value of acute renin at baseline
                    # "ren_ref": Q((0.99 + 1.53 + 1.53 + 2.29)/4, "ng/dl") / self.Mr.ren,  # HCTZ25 mono
                    # "[ren]": Q((0.99 + 1.53 + 1.53 + 2.29)/4, "ng/dl") / self.Mr.ren,  # HCTZ25 mono
                    #
                    # # mean value of acute aldosterone at baseline
                    # "ald_ref": Q((9.08 + 12.16 + 12.16 + 18.90)/4, "ng/ml") / self.Mr.ald,  # HCTZ25 mono
                    # "[ald]": Q((9.08 + 12.16 + 12.16 + 18.90)/4, "ng/ml") / self.Mr.ald,  # HCTZ25 mono
                },
            )
        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        # the dataset, the observable and the intervention whose simulation
        # the dataset is compared with
        infos = [
            ("Tab3_hctz_aurine_black", "Aurine_hctz", "hctz"),
            ("Tab3_hctz_aurine_white", "Aurine_hctz", "hctz"),
            ("Fig1_2_sodium_baseline_black", "na_urine", "baseline"),
            ("Fig1_2_sodium_baseline_white", "na_urine", "baseline"),
            # ("Fig1_2_sodium_diet_black", "na_urine", "diet"),
            # ("Fig1_2_sodium_diet_white", "na_urine", "diet"),
            ("Fig1_2_sodium_hctz_black", "na_urine", "hctz"),
            ("Fig1_2_sodium_hctz_white", "na_urine", "hctz"),
            # ("Fig3_renin_plasma_hctz_black_supine", "[ren]"),
            # ("Fig3_renin_plasma_hctz_white_supine", "[ren]"),
            # ("Fig3_renin_plasma_hctz_black_upright", "[ren]"),
            # ("Fig3_renin_plasma_hctz_white_upright", "[ren]"),
            # ("Fig3_aldo_plasma_hctz_black_supine", "[ald]"),
            # ("Fig3_aldo_plasma_hctz_white_supine", "[ald]"),
            # ("Fig3_aldo_plasma_hctz_black_upright", "[ald]"),
            # ("Fig3_aldo_plasma_hctz_white_upright", "[ald]")
        ]

        for info in infos:
            (dset_id, yid, intervention) = info
            dose = self.doses[intervention]
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
                observable=FitData(
                    self,
                    task=f"task_hctz{dose}_{intervention}",
                    xid="time",
                    yid=yid,
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.URINE,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    # stage 1 or 2 hypertension, antihypertensive drugs
                    # withdrawn 4 weeks before (p. 158)
                    health=Health.HYPERTENSION,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.NONE,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self._figure_Tab3(),
            **self._figure_Fig1_2(),
            # **self.figure_Fig3(),
        }

    def _figure_Tab3(self) -> dict[str, Figure]:
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
        for intervention in self.interventions:
            dose = self.doses[intervention]
            plots[0].add_data(
                task=f"task_hctz{dose}_{intervention}",
                xid="time",
                yid="Aurine_hctz",
                label=f"Sim ({intervention})",
                color=self.colors[intervention],
            )

        # data
        for group in self.groups:
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
            name: fig,
        }

    def _figure_Fig1_2(self) -> dict[str, Figure]:
        name = "Fig1_2"
        fig = Figure(
            experiment=self,
            sid=name,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(label="Urine Sodium\n", unit="mmole")

        for intervention in self.interventions:
            dose = self.doses[intervention]
            # simulation
            plots[0].add_data(
                task=f"task_hctz{dose}_{intervention}",
                xid="time",
                yid="na_urine",
                label="Sim",
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
            name: fig,
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
    MODEL.run_experiments(Ripley2000, output_dir=Ripley2000.__name__)
