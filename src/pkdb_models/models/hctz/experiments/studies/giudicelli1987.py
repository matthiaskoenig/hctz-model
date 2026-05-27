from copy import deepcopy
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


class Giudicelli1987(HCTZSimulationExperiment):
    """Simulation experiment of Giudicelli1987.

    single dose vs multiple dose of hydrochlorothiazide 25 mg.
    """
    colors = ["black", "tab:blue"]


    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3", "Fig5"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                if label.startswith("renin"):
                    dset.unit_conversion("mean", 1 / self.Mr.ren)
                dsets[f"{fig_id}_{label}"] = dset

        # print(dsets.keys())
        # print(dsets)
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        tc0 = Timecourse(
            start=0,
            end=24 * 60,  # [min]
            steps=500,
            changes={
                **self.default_changes(),
                "PODOSE_hctz": Q_(25, "mg"),

                # mean value of acute renin at baseline
                # "ren_ref": Q_((0.11+0.07)/2, "pg/ml") / self.Mr.ren,  # HCTZ25 and CAP50, HCTZ25
                # "[ren]": Q_((0.11+0.07)/2, "pg/ml") / self.Mr.ren,  # HCTZ25 and CAP50, HCTZ25
            },
        )

        tc1 = Timecourse(
            start=0,
            end=24 * 60,  # [min]
            steps=500,
            changes={
                "PODOSE_hctz": Q_(25, "mg"),
                # mean value of chronic renin at baseline
                # "ren_ref": Q_((0.33 + 0.26) / 2, "pg/ml") / self.Mr.ren,  # HCTZ25_MULTI, CAP50_MULTI, HCTZ25_MULTI
                # "[ren]": Q_((0.33 + 0.26) / 2, "pg/ml") / self.Mr.ren,  # HCTZ25_MULTI, CAP50_MULTI, HCTZ25_MULTI
            },
        )
        tc2 = Timecourse(
            start=0,
            end=40 * 60,  # [min]
            steps=500,
            changes={
                "PODOSE_hctz": Q_(25, "mg"),
                # mean value of chronic renin at baseline
                # "ren_ref": Q_((0.33 + 0.26) / 2, "pg/ml") / self.Mr.ren,  # HCTZ25_MULTI, CAP50_MULTI, HCTZ25_MULTI
                # "[ren]": Q_((0.33 + 0.26) / 2, "pg/ml") / self.Mr.ren,  # HCTZ25_MULTI, CAP50_MULTI, HCTZ25_MULTI
            },
        )

        tcsims["hctz25_acute"] = TimecourseSim(timecourses=tc0)
        tcsims["hctz25_chronic"] = TimecourseSim(
            timecourses=[tc0] + [deepcopy(tc1) for _ in range(43)] + [tc2],
            time_offset=-44 * 24 * 60,  # shift to the last day
        )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}
        for k, suffix in enumerate(["acute", "chronic"]):
            for kd, infix in enumerate(["hctz25", "hctz25_combi"]):
                mappings[f"fm_Fig3_{infix}_{suffix}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"Fig3_{infix}_{suffix}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_hctz25_{suffix}", xid="time", yid="[Cve_hctz]"
                    ),
                    metadata=HCTZMappingMetaData(
                        tissue=Tissue.PLASMA,
                        application_form=ApplicationForm.TABLET,
                        route=Route.PO,
                        dosing=Dosing.SINGLE if suffix == "acute" else Dosing.MULTI,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.CAPTOPRIL if "combi" in infix else Coadministration.NONE,
                    ),
                )
            # for kd, infix in enumerate(["hctz25", "combi"]):
            #     mappings[f"fm_Fig5_pra_{infix}_{suffix}"] = FitMapping(
            #         self,
            #         reference=FitData(
            #             self,
            #             dataset=f"Fig5_renin_{infix}_{suffix}",
            #             xid="time",
            #             yid="mean",
            #             yid_sd="mean_sd",
            #             count="count",
            #         ),
            #         observable=FitData(
            #             self, task=f"task_hctz25_{suffix}", xid="time", yid="[ren]"
            #         ),
            #         metadata=HCTZMappingMetaData(
            #             tissue=Tissue.PLASMA,
            #             application_form=ApplicationForm.TABLET,
            #             route=Route.PO,
            #             dosing=Dosing.SINGLE if suffix == "acute" else Dosing.MULTI,
            #             health=Health.HEALTHY,
            #             fasting=Fasting.FASTED,
            #             coadministration=Coadministration.CAPTOPRIL if "combi" in infix else Coadministration.NONE,
            #         ),
            #     )
            # console.print(mappings)
            return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_Fig3(),
            # **self.figure_Fig5(),
        }

    def figure_Fig3(self) -> Dict[str, Figure]:
        name = "Fig3"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr"),
            yaxis=Axis(self.label_hctz, unit=self.unit_hctz),
            legend=True,
        )
        plots[1].xaxis.min = -25  # [hr]
        plots[1].xaxis.max = 40  # [hr]

        for k, suffix in enumerate(["acute", "chronic"]):
            # simulation
            plots[k].add_data(
                task=f"task_hctz25_{suffix}",
                xid="time",
                yid="[Cve_hctz]",
                label=f"Sim {suffix}",
                color=self.color_hctz,
            )

            # data
            for kd, infix in enumerate(["hctz25", "hctz25_combi"]):
                plots[k].add_data(
                    dataset=f"Fig3_{infix}_{suffix}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label="25 mg HCTZ" if infix == "hctz25" else "25 mg HCTZ + CAP50",
                    color=self.colors[kd],
                )

        return {
            fig.sid: fig,
        }

    # def figure_Fig5(self) -> Dict[str, Figure]:
    #     name = "Fig5"
    #     fig = Figure(
    #         experiment=self,
    #         sid=name,
    #         num_rows=2,
    #         num_cols=1,
    #         name=f"{self.__class__.__name__} {name}",
    #     )
    #
    #     plots = fig.create_plots(
    #         xaxis=Axis(self.label_time, unit="hr"),
    #         yaxis=Axis(self.labels["[ren]"], unit=self.units["[ren]"]),
    #         legend=True,
    #     )
    #     plots[1].xaxis.min = -25  # [hr]
    #     plots[1].xaxis.max = 25  # [hr]
    #
    #     # simulation
    #     for k, suffix in enumerate(["acute", "chronic"]):
    #         plots[k].add_data(
    #             task=f"task_hctz25_{suffix}",
    #             xid="time",
    #             yid="[ren]",
    #             label=f"Sim {suffix}",
    #             color=self.color_hctz,
    #         )
    #         # data
    #         for kd, infix in enumerate(["hctz25", "combi"]):
    #             plots[k].add_data(
    #                 dataset=f"Fig5_renin_{infix}_{suffix}",
    #                 xid="time",
    #                 yid="mean",
    #                 yid_sd="mean_sd",
    #                 count="count",
    #                 label="25 mg HCTZ" if infix == "hctz25" else "25 mg HCTZ + CAP50",
    #                 color=self.colors[kd],
    #             )
    #
    #     return {
    #         fig.sid: fig,
    #     }


if __name__ == "__main__":
    run_experiments(Giudicelli1987, output_dir=Giudicelli1987.__name__)
