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


class Nilsen1989(HCTZSimulationExperiment):
    """Simulation experiment of Nilsen1989.

    single oral dosing of 25 mg HCTZ with or without 5 mg cilazapril
    """

    suffixes = [
        "hctz25",
        # "hctz25_cil5"
    ]
    names = [
        "25 mg HCTZ",
        # "25 mg HCTZ + CIL"
    ]
    colors = {
        "hctz25" : "black",
        "hctz25_cil5" : "tab:blue",
    }

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig4", "Fig5"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            if fig_id == "Fig4":
                for label, df_label in df.groupby("label"):
                    dset = DataSet.from_df(df_label, self.ureg)
                    if label.startswith("excretion_hctz25"):
                        dset.unit_conversion("mean", 1 / self.Mr.hctz)
                    dsets[f"{fig_id}_{label}"] = dset

            elif fig_id == "Fig5":
                for label, df_label in df.groupby("x_label"):
                    dset = DataSet.from_df(df_label, self.ureg)
                    if label.startswith("excretion2_hctz25"):
                         dset.unit_conversion("x", 1 / self.Mr.hctz)
                    dsets[f"{fig_id}_{label}"] = dset
                    # console.print(dset)


        # print(dsets.keys())
        # print(dsets)
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        tcsims["hctz25"] = TimecourseSim(
            Timecourse(
                start=0,
                end=40 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "PODOSE_hctz": Q_(25, "mg"),
                },
            )
        )

        return tcsims


    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}

        for ks, suffix in enumerate(self.suffixes):
            mappings[f"fm_Fig4_excretion_sodium_{suffix}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig4_excretion_sodium_{suffix}",
                    xid="time",
                    yid="mean",
                    yid_sd=None,
                    count="count"
                ),
                observable=FitData(self, task=f"task_hctz25", xid="time", yid="NA_EXCRETION"),
                metadata=HCTZMappingMetaData(
                    tissue=Tissue.URINE,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,          #Fig4 only volunteers (healthy)
                    fasting=Fasting.NR,
                    coadministration=Coadministration.CILAZAPRIL if "cil5" in suffix else Coadministration.NONE,
                ),
            )
            # FIXME: bugfix in optimization
            # mappings[f"fm_Fig5_excretion2_{suffix}"] = FitMapping(
            #     self,
            #     reference=FitData(
            #         self,
            #         dataset=f"Fig5_excretion2_{suffix}",
            #         xid="x",
            #         yid="y",
            #         xid_sd=None,
            #         yid_sd=None,
            #         count="count"
            #     ),
            #     observable=FitData(self, task=f"task_hctz25", xid="KI__HCTZEX", yid="NA_EXCRETION"),
            #     metadata=HCTZMappingMetaData(
            #         tissue=Tissue.URINE,
            #         application_form=ApplicationForm.TABLET,
            #         route=Route.PO,
            #         dosing=Dosing.SINGLE,
            #         health=Health.HEALTHY,  # Fig5 only volunteers (healthy)
            #         fasting=Fasting.NR,
            #         coadministration=Coadministration.CILAZAPRIL if "cil5" in suffix else Coadministration.NONE,
            #     ),
            # )
            return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figures_fig4_5(),
        }

    def figures_fig4_5(self) -> Dict[str, Figure]:
        name = "Fig4_5"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(legend=True)
        for k in [0, 1]:
            plots[k].set_xaxis(label=self.label_time, unit="hr"),

        plots[0].set_yaxis(label=self.label_hctz_excretion_urine, unit=self.unit_hctz_excretion_urine)
        plots[1].set_yaxis(label="Sodium excretion\n", unit="mmole/hr"),

        plots[2].set_xaxis(label=self.label_hctz_excretion_urine, unit=self.unit_hctz_excretion_urine)
        plots[2].set_yaxis(label="Sodium excretion\n", unit="mmole/hr")

        # simulation
        for k, (xid, yid) in enumerate([
            ("time", "KI__HCTZEX"),
            ("time", "NA_EXCRETION"),
            ("KI__HCTZEX", "NA_EXCRETION"),
        ]):
            plots[k].add_data(
                task=f"task_hctz25",
                xid=xid,
                yid=yid,
                label=f"Sim",
                color=self.color_hctz,
            )

        # data
        for ks, suffix in enumerate(self.suffixes):
            for k, (dset_id, xid, yid) in enumerate([
                (f"Fig4_excretion_{suffix}", "time", "mean"),
                (f"Fig4_excretion_sodium_{suffix}", "time", "mean"),
                (f"Fig5_excretion2_{suffix}", "x", "y"),
            ]):
                plots[k].add_data(
                    dataset=dset_id,
                    xid=xid,
                    yid=yid,
                    xid_sd=None,
                    yid_sd=None,
                    count="count",
                    label=self.names[ks],
                    marker="o" if suffix.endswith("cil5") else "s",
                    color=self.colors[suffix],
                )

        return {
            fig.sid: fig,
        }

if __name__ == "__main__":
    run_experiments(Nilsen1989, output_dir=Nilsen1989.__name__)
