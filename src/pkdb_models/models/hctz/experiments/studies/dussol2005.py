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


class Dussol2005(HCTZSimulationExperiment):
    """Simulation experiment of Dussol2005.

    multiple oral dosing of 25mg HCTZ .
    """

    yids = {
        "Vurine": "urinvol",
        "na_urine": "amount_na"
    }


    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab2","Tab3"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
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
                "f_renal_function": Q_(
                    19.5 / 100, "dimensionless")
            },
        )
        tc1 = Timecourse(
            start=0,
            end=24 * 60,  # [min]
            steps=500,
            changes={
                "PODOSE_hctz": Q_(25, "mg"),
                "na_urine": Q_(0, "mmole"), # reset urinary amount
                "Vurine": Q_(1E-15, "l"),  # reset urinary volume
            },
        )

        tcsims["hctz25"] = TimecourseSim(
            [tc0] + [tc1 for _ in range(29)],
            # time_offset=-29 * 24 * 60,
        )

        return tcsims


    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}

        mappings[f"fm_Tab2_map_hctz"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset=f"Tab2_map_hctz",
                xid="time",
                yid="mean",
                count="count",
            ),
            observable=FitData(
                self, task=f"task_hctz25", xid="time", yid="bp_systolic" #FIXME:MAP
            ),
            metadata=HCTZMappingMetaData(
                tissue=Tissue.PLASMA,
                application_form=ApplicationForm.TABLET,
                route=Route.PO,
                dosing=Dosing.MULTI,
                health=Health.RENAL_IMPAIRMENT,
                fasting=Fasting.NR,
                coadministration=Coadministration.NONE,
            ),
        )

        for yid, label in self.yids.items():
            mappings[f"fm_Tab3_{label}_hctz"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Tab3_{label}_hctz",
                    xid="time",
                    yid="mean",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_hctz25", xid="time", yid=yid
                ),
                metadata=HCTZMappingMetaData(
                    tissue=Tissue.URINE,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.MULTI,
                    health=Health.RENAL_IMPAIRMENT,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.NONE,
                ),
            )

        # console.print(mappings)
        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_Tab2(),
            **self.figure_Tab3(),
        }

    def figure_Tab2(self) -> Dict[str, Figure]:
        name = "Tab2"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(label="MAP", unit="mmHg")

        # simulation
        plots[0].add_data(
            task=f"task_hctz25",
            xid="time",
            yid="bp_systolic",      #FIXME: MAP
            label=f"Sim RI sev",
            color="#2ca25f",
        )

        # data
        plots[0].add_data(
            dataset=f"Tab2_map_hctz",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label=f"25 mg hctz",
            color="black",
            linestyle="",
        )

        return {
            fig.sid: fig,
        }

    def figure_Tab3(self) -> Dict[str, Figure]:
        name = "Tab3"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=2,
            num_cols=1,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_urine_volume, self.unit_urine_volume)
        plots[1].set_yaxis(self.label_na_urine, self.unit_na_urine)

        # simulation
        plots[0].add_data(
            task=f"task_hctz25",
            xid="time",
            yid="Vurine",
            label=f"Sim RI sev",
            color="#2ca25f",
        )

        plots[1].add_data(
            task=f"task_hctz25",
            xid="time",
            yid="na_urine",
            label=f"Sim RI sev",
            color="#2ca25f",
        )


        # data
        plots[0].add_data(
            dataset=f"Tab3_urinvol_hctz",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label=f"25 mg hctz",
            color="black",
            linestyle="",
        )

        plots[1].add_data(
            dataset=f"Tab3_amount_na_hctz",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label=f"25 mg hctz",
            color="black",
            linestyle="",
        )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Dussol2005, output_dir=Dussol2005.__name__)
