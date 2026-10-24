"""Simulation experiment of the study Giudicelli1987."""

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


class Giudicelli1987(HCTZSimulationExperiment):
    """Simulation experiment of Giudicelli1987.

    single dose vs multiple dose of hydrochlorothiazide 25 mg in patients with
    moderate essential hypertension (p. 52S).
    """

    colors: ClassVar[list[str]] = ["black", "tab:blue"]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3", "Fig5"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                if label.startswith("renin"):
                    dset.unit_conversion("mean", 1 / self.Mr.ren)
                dsets[self.to_sid(f"{fig_id}_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        simulations["hctz25_acute"] = Simulation(
            time_unit="hr",
            end=24,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_hctz": Q(25, "mg"),
                # mean value of acute renin at baseline
                # "ren_ref": Q((0.11+0.07)/2, "pg/ml") / self.Mr.ren,  # HCTZ25 and CAP50, HCTZ25
                # "[ren]": Q((0.11+0.07)/2, "pg/ml") / self.Mr.ren,  # HCTZ25 and CAP50, HCTZ25
            },
        )

        # 45 doses, every 24 hours, the data is reported from the last dose
        dose_times = [24 * k for k in range(45)]
        simulations["hctz25_chronic"] = Simulation(
            time_unit="hr",
            end=44 * 24 + 40,
            preinit_changes={
                **self.default_changes(),
                # mean value of acute renin at baseline
                # "ren_ref": Q((0.11+0.07)/2, "pg/ml") / self.Mr.ren,  # HCTZ25 and CAP50, HCTZ25
                # "[ren]": Q((0.11+0.07)/2, "pg/ml") / self.Mr.ren,  # HCTZ25 and CAP50, HCTZ25
                "PODOSE_hctz": Q(25, "mg"),
            },
            changes=[
                self.add_doses(dose_times[1:], {"PODOSE_hctz": Q(25, "mg")}),
                # mean value of chronic renin at baseline
                # Change(dose_times[1:], {
                #     "ren_ref": Q((0.33 + 0.26) / 2, "pg/ml") / self.Mr.ren,  # HCTZ25_MULTI, CAP50_MULTI, HCTZ25_MULTI
                #     "[ren]": Q((0.33 + 0.26) / 2, "pg/ml") / self.Mr.ren,  # HCTZ25_MULTI, CAP50_MULTI, HCTZ25_MULTI
                # }),
            ],
            time_shift=-44 * 24,  # shift to the last day
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for suffix in ["acute", "chronic"]:
            for infix in ["hctz25", "hctz25_combi"]:
                mappings[self.to_sid(f"fm_Fig3_{infix}_{suffix}")] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Fig3_{infix}_{suffix}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=self.to_sid(f"task_hctz25_{suffix}"),
                        xid="time",
                        yid="[Cve_hctz]",
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.PLASMA,
                        application_form=ApplicationForm.TABLET,
                        route=Route.PO,
                        dosing=Dosing.SINGLE if suffix == "acute" else Dosing.MULTIPLE,
                        # moderate essential hypertension (p. 52S)
                        health=Health.HYPERTENSION,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.CAPTOPRIL
                        if "combi" in infix
                        else Coadministration.NONE,
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
            #         metadata=PKPDMappingMetaData(
            #             tissue=Tissue.PLASMA,
            #             application_form=ApplicationForm.TABLET,
            #             route=Route.PO,
            #             dosing=Dosing.SINGLE if suffix == "acute" else Dosing.MULTIPLE,
            #             health=Health.HEALTHY,
            #             fasting=Fasting.FASTED,
            #             coadministration=Coadministration.CAPTOPRIL if "combi" in infix else Coadministration.NONE,
            #         ),
            #     )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self._figure_Fig3(),
            # **self.figure_Fig5(),
        }

    def _figure_Fig3(self) -> dict[str, Figure]:
        name = "Fig3"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr"),
            yaxis=Axis(self.label_hctz, unit=self.unit_hctz),
            legend=True,
        )
        plots[1].set_xaxis(self.label_time, unit="hr", min=-25, max=40)  # [hr]

        for k, suffix in enumerate(["acute", "chronic"]):
            # simulation
            plots[k].add_data(
                task=self.to_sid(f"task_hctz25_{suffix}"),
                xid="time",
                yid="[Cve_hctz]",
                label=f"Sim {suffix}",
                color=self.color_hctz,
            )

            # data
            for kd, infix in enumerate(["hctz25", "hctz25_combi"]):
                plots[k].add_data(
                    dataset=self.to_sid(f"Fig3_{infix}_{suffix}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label="25 mg HCTZ" if infix == "hctz25" else "25 mg HCTZ + CAP50",
                    color=self.colors[kd],
                )

        return {
            self.to_sid(name): fig,
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
    MODEL.run_experiments(Giudicelli1987, output_dir=Giudicelli1987.__name__)
