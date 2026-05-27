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


class Jeon2012(HCTZSimulationExperiment):
    """Simulation experiment of Jeon2012.

    Multiple oral dosing of 25mg HCTZ.
    """

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3", "Fig4", "Fig5", "Fig6", "Tab2"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                elif fig_id == "Tab2" and label.startswith("amount_"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                # elif fig_id == "Fig5" and label.startswith("pra_"):
                #     dset.unit_conversion("mean", 1 / self.Mr.ren)
                # elif fig_id == "Fig5" and label.startswith("aldosterone_"):
                #     dset.unit_conversion("mean", 1 / self.Mr.ald)
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

                # # mean value of acute renin at baseline
                # "ren_ref": Q_(7.58, "ng/ml") / self.Mr.ren,  # HCTZ25 mono
                # "[ren]": Q_(7.58, "ng/ml") / self.Mr.ren,  # HCTZ25 mono
                # # mean value of acute aldosterone at baseline
                # "ald_ref": Q_(209.58, "pg/ml") / self.Mr.ald,  # HCTZ25 mono
                # "[ald]": Q_(209.58, "pg/ml") / self.Mr.ald,  # HCTZ25 mono

                # blood pressure
                # blood pressures were within predetermined criteria
                # (systolic blood pressure <140 and >100 mmHg and
                #  diastolic blood pressure <90 and >65 mmHg)
                "Psys_ref": Q_((140+100)/2, "mmHg"),  # HCTZ25 mono
                "Pdia_ref": Q_((90+65)/2, "mmHg"),   # HCTZ25 mono
            },
        )
        tc1 = Timecourse(
            start=0,
            end=24 * 60,  # [min]
            steps=500,
            changes={
                "PODOSE_hctz": Q_(25, "mg"),
                "Aurine_hctz": Q_(0, "mmole"), # reset urinary amount
                "Vurine": Q_(1E-15, "l"),  # reset urinary volume
            },
        )
        tc2 = Timecourse(
            start=0,
            end=30 * 60,  # [min]
            steps=500,
            changes={
                "PODOSE_hctz": Q_(25, "mg"),
                "Aurine_hctz": Q_(0, "mmole"),  # reset urinary amount
                "Vurine": Q_(1E-15, "l"),  # reset urinary volume
            },
        )

        tcsims["hctz25"] = TimecourseSim(
            [tc0] + [tc1 for _ in range(5)] + [tc2],
            time_offset=-6 * 24 * 60,
        )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}
        infos = [
            ("Fig3_hctz25", "[Cve_hctz]", Tissue.PLASMA),
            ("Tab2_amount_cumulative_hctz25", "Aurine_hctz", Tissue.URINE),
            ("Fig4_urine_vol_hctz25", "Vurine", Tissue.URINE),
            # ("Fig5_pra_hctz25", "[ren]", Tissue.PLASMA),  # renin activity
            # ("Fig5_aldosterone_hctz25", "[ald]", Tissue.PLASMA),
            ("Fig6_bpsys_hctz25", "bp_systolic", Tissue.PLASMA),
            ("Fig6_bpdia_hctz25", "bp_diastolic", Tissue.PLASMA),
        ]

        for info in infos:
            (dset_id, yid, tissue) = info
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
                observable=FitData(self, task=f"task_hctz25", xid="time", yid=yid),
                metadata=HCTZMappingMetaData(
                    tissue=tissue,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.MULTI,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.FIMASARTAN if "fima240" in dset_id else Coadministration.NONE,
                ),
            )

        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_Fig3_Tab2(),
            **self.figure_Fig4(),
            # **self.figure_Fig5(),
            **self.figure_Fig6(),
        }

    def figure_Fig3_Tab2(self) -> Dict[str, Figure]:
        name = "Fig3_Tab2"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr", min=-25, max=40), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)
        plots[1].set_yaxis(self.label_hctz_urine, unit=self.unit_hctz_urine)

        # simulation
        for k, yid in enumerate(["[Cve_hctz]", "Aurine_hctz"]):
            plots[k].add_data(
                task=f"task_hctz25",
                xid="time",
                yid=yid,
                label=f"Sim",
                color="black",
            )

        # data
        for kd, suffix in enumerate(["hctz25", "hctz25_kombi"]):
            plots[0].add_data(
                dataset=f"Fig3_{suffix}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="25 mg HCTZ" if suffix == "hctz25" else "25 mg HCTZ + FIMA",
                color="black" if suffix == "hctz25" else "tab:blue",
            )
            plots[1].add_data(
                dataset=f"Tab2_amount_cumulative_{suffix}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="25 mg HCTZ" if suffix == "hctz25" else "25 mg HCTZ + FIMA",
                color="black" if suffix == "hctz25" else "tab:blue",
                linestyle="",
            )

        return {
            fig.sid: fig,
        }


    def figure_Fig4(self) -> Dict[str, Figure]:
        name = "Fig 4"
        fig = Figure(
            experiment=self,
            sid=name,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr", min=-25, max=40), legend=True)
        plots[0].set_yaxis(label="urine volume", unit="l")

        # simulation
        plots[0].add_data(
            task=f"task_hctz25",
            xid="time",
            yid="Vurine",
            label=f"Sim",
            color=self.color_hctz,
        )
        # data
        plots[0].add_data(
            dataset=f"Fig4_urine_vol_hctz25",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label=f"25 mg HCTZ",
            color=self.color_hctz,
        )

        return {
            fig.sid: fig,
        }

    # def figure_Fig5(self) -> Dict[str, Figure]:
    #     name = "Fig 5"
    #     fig = Figure(
    #         experiment=self,
    #         sid=name,
    #         num_rows=2,
    #         num_cols=1,
    #         name=f"{self.__class__.__name__} {name}",
    #     )
    #     plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr", min=-25, max=25), legend=True)
    #     plots[0].set_yaxis(self.labels["[ren]"], self.units["[ren]"])
    #     plots[1].set_yaxis(self.labels["[ald]"], self.units["[ald]"])
    #
    #     # simulation
    #     plots[0].add_data(
    #         task=f"task_hctz25",
    #         xid="time",
    #         yid="[ren]",
    #         label=f"Sim",
    #         color=self.color_hctz,
    #     )
    #     plots[1].add_data(
    #         task=f"task_hctz25",
    #         xid="time",
    #         yid="[ald]",
    #         label=f"Sim",
    #         color=self.color_hctz,
    #     )
    #     # data
    #     plots[0].add_data(
    #         dataset=f"Fig5_pra_hctz25",
    #         xid="time",
    #         yid="mean",
    #         yid_sd="mean_sd",
    #         count="count",
    #         label=f"25 mg HCTZ",
    #         color=self.color_hctz,
    #     )
    #     plots[1].add_data(
    #         dataset=f"Fig5_aldosterone_hctz25",
    #         xid="time",
    #         yid="mean",
    #         yid_sd="mean_sd",
    #         count="count",
    #         label=f"25 mg HCTZ",
    #         color=self.color_hctz,
    #     )
    #
    #     return {
    #         fig.sid: fig,
    #     }

    def figure_Fig6(self) -> Dict[str, Figure]:
        name = "Fig 6"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr",
                                            min=-25, max=25
                                            ), legend=True)
        plots[0].set_yaxis(self.labels["bp_systolic"], unit=self.units["bp_systolic"])
        plots[1].set_yaxis(self.labels["bp_diastolic"], unit=self.units["bp_diastolic"])

        # simulation
        plots[0].add_data(
            task=f"task_hctz25",
            xid="time",
            yid="bp_systolic",
            label=f"Sim",
            color=self.color_hctz,
        )
        plots[1].add_data(
            task=f"task_hctz25",
            xid="time",
            yid="bp_diastolic",
            label=f"Sim",
            color=self.color_hctz,
        )

        # data
        plots[0].add_data(
            dataset=f"Fig6_bpsys_hctz25",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label=f"25 mg HCTZ",
            color=self.color_hctz,
        )
        plots[1].add_data(
            dataset=f"Fig6_bpdia_hctz25",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label=f"25 mg HCTZ",
            color=self.color_hctz,
        )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Jeon2012, output_dir=Jeon2012.__name__)
