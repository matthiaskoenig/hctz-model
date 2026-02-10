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


class Howes1991(HCTZSimulationExperiment):
    """Simulation experiment of Howes1991.

    Single oral dosing of 25mg HCTZ.
    """

    suffixes = [
        "_hydrochlorothiazide",
        ", ENA10_multi_hydrochlorothiazide",
        "_combi_hydrochlorothiazide",
    ]
    suffix_keys = ["alone", "+ 10mg ENA separate", "+ 10mg ENA combi"]
    prefixes = ["HCTZ25", "ENA10, HCTZ25multi", "ENA10, HCTZ25combi"]
    colors = ["black", "tab:blue", "tab:orange"]

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Tab2"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                if label.endswith("_hydrochlorothiazide"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                elif label.endswith("_enalaprilat"):
                    pass
                dsets[f"{fig_id}_{label}"] = dset

        # print(dsets.keys())
        # print(dsets)
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        tcsims["hctz25"] = TimecourseSim(
            Timecourse(
                start=0,
                end=100 * 60,  # [min]
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
        # plasma
        for k, suffix in enumerate(self.suffixes):
            mappings[f"fm_Fig1_HCTZ25{suffix}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig1_HCTZ25{suffix}",
                    xid="time",
                    yid="mean",
                    yid_sd=None,
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_hctz25", xid="time", yid="[Cve_hctz]"
                ),
                metadata=HCTZMappingMetaData(
                    tissue=Tissue.PLASMA,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.ENALAPRIL if "ENA10" in suffix else Coadministration.NONE,
                ),
            )
        # urine
        for n, prefix in enumerate(self.prefixes):
            mappings[f"fm_Tab2_{prefix}_cumulative amount_hydrochlorothiazide"] = (
                FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"Tab2_{prefix}_cumulative amount_hydrochlorothiazide",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_hctz25", xid="time", yid="Aurine_hctz"
                    ),
                    metadata=HCTZMappingMetaData(
                        tissue=Tissue.URINE,
                        application_form=ApplicationForm.TABLET,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.ENALAPRIL if "ENA10" in suffix else Coadministration.NONE,
                    ),
                )
            )
        # console.print(mappings)
        return mappings

    def figures(self) -> Dict[str, Figure]:
        name = "Fig1 & Tab2"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=2,
            num_cols=1,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)
        plots[1].set_yaxis(label=self.label_hctz_urine, unit=self.unit_hctz_urine)

        # simulation
        for k, yid in enumerate(["[Cve_hctz]", "Aurine_hctz"]):
            plots[k].add_data(
                task=f"task_hctz25",
                xid="time",
                yid=yid,
                label=f"Sim",
                color=self.color_hctz,
            )

        # data
        for k, suffix in enumerate(self.suffixes):
            key = self.suffix_keys[k]

            # plasma
            plots[0].add_data(
                dataset=f"Fig1_HCTZ25{suffix}",
                xid="time",
                yid="mean",
                yid_sd=None,
                count="count",
                label=f"25 mg HCTZ {key}",
                color=self.colors[k],
            )
            # urine
            plots[1].add_data(
                dataset=f"Tab2_{self.prefixes[k]}_cumulative amount_hydrochlorothiazide",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"25 mg HCTZ {key}",
                linestyle="",
                color=self.colors[k],
            )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Howes1991, output_dir=Howes1991.__name__)
