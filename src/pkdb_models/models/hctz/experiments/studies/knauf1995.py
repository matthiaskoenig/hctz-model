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


class Knauf1995(HCTZSimulationExperiment):
    """Simulation experiment of Knauf1995.

    single oral dosing of 50mg HCTZ.
    """
    # labels = ["NRF", "MRI", "SRI"]
    # patients = ["C", "S", "W"]
    crcl = [4,5,1,17,20,22,25,31,36,38,42,52,52,60,60,65,73,73,75,100,107,107,122,130,153]   #  [ml/min]
    # colors = ["black", "tab:orange", "tab:red"]

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1","Fig2"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                # if label.startswith("hctz"):
                #     dset.unit_conversion("value", 1 / self.Mr.hctz)
                dsets[f"{fig_id}_{label}"] = dset

        # print(dsets.keys())
        # print(dsets)
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        for patient, crcl in enumerate(self.crcl):
            tcsims[f"hctz25_{patient}"] = TimecourseSim(
                Timecourse(
                    start=0,
                    end=30 * 60,  # [min]
                    steps=500,
                    changes={
                        **self.default_changes(),
                        "PODOSE_hctz": Q_(25, "mg"),
                        "KI__f_renal_function": Q_(
                            crcl / 100, "dimensionless"
                        ),  # relative kidney function
                    },
                )
            )

        return tcsims

    # def fit_mappings(self) -> Dict[str, FitMapping]:
    #     mappings = {}
    #     for kp, patient in enumerate(self.patients):
    #         mappings[f"fm_Fig1_hctz50_{patient}"] = FitMapping(
    #             self,
    #             reference=FitData(
    #                 self,
    #                 dataset=f"Fig1_hctz50_{patient}",
    #                 xid="time",
    #                 yid="value",
    #                 count="count",
    #             ),
    #             observable=FitData(
    #                 self, task=f"task_hctz50_{patient}", xid="time", yid="[Cve_hctz]"
    #             ),
    #             metadata=HCTZMappingMetaData(
    #                 tissue=Tissue.PLASMA,
    #                 application_form=ApplicationForm.TABLET,
    #                 route=Route.PO,
    #                 dosing=Dosing.SINGLE,
    #                 health=Health.HEALTHY if self.labels[kp] == "NRF" else Health.RENAL_IMPAIRMENT,
    #                 fasting=Fasting.FASTED,
    #                 coadministration=Coadministration.NONE,
    #             ),
    #         )
    #
    #     # console.print(mappings)
    #     return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_Fig1_2(),
            #    **self.figure_Fig2(),
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
        plots[0].set_yaxis(self.label_na_urine, unit=self.unit_na_urine)
        plots[1].set_yaxis(label="Sodium excretion\n", unit="mmole/hr")

        # simulation

        plots[0].add_data(
            task=f"task_hctz25_20",
            xid="time",
            yid="na_urine",
            label=f"Sim normal gfr",
            color="black",
        )

        plots[1].add_data(
            task=f"task_hctz25_20",
            xid="time",
            yid="NA_EXCRETION",
            label=f"Sim normal gfr",
            color="black",
)

        # data
        plots[0].add_data(
            dataset=f"Fig1_na_urine_healthy",
            xid="time",
            yid="value",
            count="count",
            label=f"25 mg hctz",
            color="green",
        )

        plots[1].add_data(
            dataset=f"Fig2_exc_na_healthy",
            xid="time",
            yid="value",
            count="count",
            label=f"25 mg hctz",
            color="green",
        )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Knauf1995, output_dir=Knauf1995.__name__)
