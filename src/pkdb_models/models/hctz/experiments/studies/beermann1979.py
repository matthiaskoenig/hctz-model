from typing import Dict

import numpy as np
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


class Beermann1979(HCTZSimulationExperiment):
    """Simulation experiment of Beermann1979.

    HCTZ single oral doses 50 in patients with congestive heart failure.
    WITHOUT subject SL who was given 75 mg dose by mistake
    """


    individuals = ["NL", "SP", "JG", "SH", "NK", "GN"]
    crcl = {
        "NL": 27,
        "SP": 116,
        "JG": 19,
        "SH": 47,
        "NK": 53,
        "GN": 24,
    }  # [ml/min]
    dyspnea = {
        "NL": True,
        "SP": False,
        "JG": True,
        "SH": False,
        "NK": True,
        "GN": False,
    }
    colors = {
        "NL": "tab:red",
        "SP": "black",
        "JG": "tab:red",
        "SH": "tab:red",
        "NK": "tab:red",
        "GN": "tab:red",
    }
    markers = {
        "NL": ">",
        "SP": "s",
        "JG": "o",
        "SH": "^",
        "NK": "*",
        "GN": "<",
    }

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Tab3"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz") or label.startswith("amount"):
                    dset.unit_conversion("value", 1 / self.Mr.hctz)
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[f"{fig_id}_{label}"] = dset

        # print(dsets.keys())
        # print(dsets)
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        for individual in self.individuals:
            tcsims[f"hctz50_{individual}"] = TimecourseSim(
                Timecourse(
                    start=0,
                    end= 250 * 60,  # [min]
                    steps=2000,
                    changes={
                        **self.default_changes(),
                        "PODOSE_hctz": Q_(50, "mg"),
                        "KI__f_renal_function": Q_(
                            self.crcl[individual] / 101, "dimensionless"
                        ),
                        # f_cardiac_function => severe
                        "f_cardiac_function": Q_(
                            3/5.25 if self.dyspnea[individual] else  3.5/5.25 , "dimensionless"
                        ),
                        # FIXME: handle reduced fraction absorbed ?!
                        # "GU__F_hctz_abs": Q_(np.min([self.crcl[individual] / 101, 1.0]) * 0.75, "dimensionless"),  # assumption from recovery [Beermann1979]
                    },
                )
            )

        return tcsims


    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}
        # FIXME
        # plasma
        for individual in ["SP", "NL"]:
            mappings[(f"fm_Fig1_hctz50_{individual}")] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset=f"Fig1_hctz50_{individual}",
                xid="time",
                yid="value",
                count="count",
            ),
            observable=FitData(self, task=f"task_hctz50_{individual}", xid="time", yid="[Cve_hctz]"),
            metadata=HCTZMappingMetaData(
                tissue=Tissue.PLASMA,
                application_form=ApplicationForm.TABLET,
                route=Route.PO,
                dosing=Dosing.SINGLE,
                health=Health.CARDIAC_RENAL_IMPAIRMENT,
                fasting=Fasting.FASTED,
                coadministration=Coadministration.NONE,
            ),
        )
        #
        for individual in self.individuals:
            mappings[f"fm_Tab3_amount_{individual}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Tab3_amount_{individual}",
                    xid="time",
                    yid="value",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_hctz50_{individual}", xid="time", yid="Aurine_hctz"
                ),
                metadata=HCTZMappingMetaData(
                    tissue=Tissue.PLASMA,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.CARDIAC_RENAL_IMPAIRMENT,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.NONE,
                ),
            )

        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_Fig1(),
            **self.figure_Tab3(),
        }

    def figure_Fig1(self) -> Dict[str, Figure]:
        name = "Fig1"
        fig = Figure(
            experiment=self,
            sid=name,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr", min=-5, max=80), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)

        # simulation
        for individual in ["SP", "NL"]:
            plots[0].add_data(
                task=f"task_hctz50_{individual}",
                xid="time",
                yid="[Cve_hctz]",
                label=f"Sim 50 mg",
                color=self.colors[individual],
            )

            # data
            plots[0].add_data(
                dataset=f"Fig1_hctz50_{individual}",
                xid="time",
                yid="value",
                yid_sd=None,
                count="count",
                label=f"hctz50 {individual}",
                color=self.colors[individual],
                marker=self.markers[individual],
            ),

        return {
            fig.sid: fig,
        }

    def figure_Tab3(self) -> Dict[str, Figure]:
        name = "Tab3"
        fig = Figure(
            experiment=self,
            sid=name,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz_urine, unit=self.unit_hctz_urine)

        # mean data from controls from Beermann1977a
        plots[0].add_data(
            dataset=f"Tab3_amount_HCTZ50",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="control",
            color="black",
        )

        for individual in self.individuals:
            # simulation
            plots[0].add_data(
                task=f"task_hctz50_{individual}",
                xid="time",
                yid="Aurine_hctz",
                label=f"Sim {individual}",
                color=self.colors[individual],
            )
            # patient data
            plots[0].add_data(
                dataset=f"Tab3_amount_{individual}",
                xid="time",
                yid="value",
                count="count",
                label=individual,
                color=self.colors[individual],
                marker=self.markers[individual],
            )

        return {
            fig.sid: fig,
        }

if __name__ == "__main__":
    run_experiments(Beermann1979, output_dir=Beermann1979.__name__)
