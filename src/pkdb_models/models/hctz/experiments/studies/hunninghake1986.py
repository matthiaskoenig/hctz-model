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


class Hunninghake1986(HCTZSimulationExperiment):
    """Simulation experiment of Hunninghake1986.

    single oral dose of HCTZ 75 mg with and without various doses of Cholestyramin.
    """

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig2", "Fig3"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                elif label.startswith("amount"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[f"{fig_id}_{label}"] = dset

        # print(dsets.keys())
        # print(dsets)
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        tcsims["hctz75"] = TimecourseSim(
            Timecourse(
                start=0,
                end=30 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "PODOSE_hctz": Q_(75, "mg"),
                },
            )
        )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}

        for dset_id in ["Fig1_amount_cumulative_hctz75", "Fig2_amount_cumulative_hctz75_def"]:
            mappings[f"fm_{dset_id}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"{dset_id}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_hctz75", xid="time", yid="Aurine_hctz"
                ),
                metadata=HCTZMappingMetaData(
                    tissue=Tissue.URINE,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.CHOLESTYRAMINE if "chol" in dset_id else Coadministration.NONE,
                ),
            )

        mappings["fm_Fig3_hctz75"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset=f"Fig3_hctz75",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
            ),
            observable=FitData(self, task=f"task_hctz75", xid="time", yid="[Cve_hctz]"),
            metadata=HCTZMappingMetaData(
                tissue=Tissue.PLASMA,
                application_form=ApplicationForm.TABLET,
                route=Route.PO,
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                fasting=Fasting.NR,
                coadministration=Coadministration.CHOLESTYRAMINE if "chol" in dset_id else Coadministration.NONE,
            ),
        )

        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_Fig1_2_3(),
        }

    def figure_Fig1_2_3(self) -> Dict[str, Figure]:
        name = "Fig1_2_3"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=2,
            num_cols=1,
            name=f"{self.__class__.__name__} {name}",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(label=self.label_hctz, unit=self.unit_hctz)
        plots[1].set_yaxis(label=self.label_hctz_urine, unit=self.unit_hctz_urine)

        # simulation
        for k, yid in enumerate(["[Cve_hctz]", "Aurine_hctz"]):
            plots[k].add_data(
                task=f"task_hctz75",
                xid="time",
                yid=yid,
                label=f"Sim",
                color=self.color_hctz,
            )

        # data
        plots[0].add_data(
            dataset=f"Fig3_hctz75",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label=f"75 mg",
            color="black",
        )

        for dset_id in ["Fig1_amount_cumulative_hctz75", "Fig2_amount_cumulative_hctz75_def"]:
            plots[1].add_data(
                dataset=dset_id,
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"75 mg" if dset_id.startswith("Fig1") else "75 mg (def)",
                color="black" if dset_id.startswith("Fig1") else "tab:blue",
            )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Hunninghake1986, output_dir=Hunninghake1986.__name__)
