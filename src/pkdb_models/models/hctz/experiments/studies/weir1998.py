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


class Weir1998(HCTZSimulationExperiment):
    """Simulation experiment of Weir1998.

    Multiple dosing of hydrochlorothiazide 25 mg twice daily.
    """

    suffixes = ["", "_kombi"]
    colors = {
        "": "black",
        "_kombi": "tab:blue",
    }

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2", "Fig3", "Tab4"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                elif label.startswith("amount_") or label.startswith("excretion_"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[f"{fig_id}_{label}"] = dset
        # print(dsets.keys())
        # print(dsets)
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        # 11 doses, every 12 hours

        tc0 = Timecourse(
            start=0,
            end=12 * 60,  # [min]
            steps=500,
            changes={
                **self.default_changes(),
                "PODOSE_hctz": Q_(25, "mg"),
            },
        )
        tc1 = Timecourse(
            start=0,
            end=12 * 60,  # [min]
            steps=500,
            changes={
                "PODOSE_hctz": Q_(25, "mg"),
                "Aurine_hctz": Q_(0, "mmole"),  # reset urine collection
            },
        )
        tc2 = Timecourse(
            start=0,
            end=60 * 60,  # [min]
            steps=500,
            changes={
                "PODOSE_hctz": Q_(25, "mg"),
                "Aurine_hctz": Q_(0, "mmole"),  # reset urine collection
            },
        )
        tcsims["hctz25"] = TimecourseSim(
            [tc0] + [tc1 for _ in range(9)] + [tc2],
            time_offset=-10*12*60
        )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}

        infos = [
            ("Fig2_hctz25", "[Cve_hctz]", Tissue.PLASMA),
            ("Fig3_amount_cumulative_hctz25", "Aurine_hctz", Tissue.URINE),
            ("Tab4_excretion_hctz25", "KI__HCTZEX", Tissue.URINE),
        ]

        for info in infos:
            (dset_id, yid, tissue) = info
            for suffix in self.suffixes:
                mappings[f"fm_{dset_id}{suffix}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{dset_id}{suffix}",
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
                        fasting=Fasting.NR,
                        coadministration=Coadministration.DILTIAZEM if "kombi" in suffix else Coadministration.NONE,
                    ),
                )

        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_Fig2_Fig3_Tab4(),
        }

    def figure_Fig2_Fig3_Tab4(self) -> Dict[str, Figure]:
        name = "Fig2_Fig3_Tab4"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=3,
            num_cols=1,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr"), legend=True
        )
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)
        plots[1].set_yaxis(label=self.label_hctz_excretion_urine, unit=self.unit_hctz_excretion_urine)
        plots[2].set_yaxis(label=self.label_hctz_urine, unit=self.unit_hctz_urine)

        # simulation
        for k, yid in enumerate(["[Cve_hctz]", "KI__HCTZEX", "Aurine_hctz"]):
            plots[k].add_data(
                task=f"task_hctz25",
                xid="time",
                yid=yid,
                label=f"Sim",
                color=self.color_hctz,
            )

        # data
        for k, dset_id in enumerate(["Fig2_hctz25", "Tab4_excretion_hctz25", "Fig3_amount_cumulative_hctz25"]):
            for suffix in self.suffixes:
                plots[k].add_data(
                    dataset=f"{dset_id}{suffix}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label="25 mg + DIL60" if "kombi" in suffix else "25 mg",
                    color=self.colors[suffix],
                )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Weir1998, output_dir=Weir1998.__name__)
