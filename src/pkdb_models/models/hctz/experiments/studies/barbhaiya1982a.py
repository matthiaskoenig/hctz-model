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


class Barbhaiya1982a(HCTZSimulationExperiment):
    """Simulation experiment of Barbhaiya1982a.
    Comparative bioavailability and pharmacokinetics of hydrochlorothiazide from oral tablet dosage forms, determined by plasma level and urinary excretion methods.
    Single 50 mg oral doses of hydrochlorothiazide, comparing bioavailability of two hydrochlorothiazide products
    """

    group_keys = ["msd", "stanlab"]
    group_labels = [
        "HCTZ 50 msd",
        "HCTZ 50 stanlab"
    ]
    colors = ["tab:blue", "tab:green"]

    yids = [
        "[Cve_hctz]",  # plasma concentration
        "Aurine_hctz",  # cumulative amount urine
    ]
    prefixes = [
        "hctz50_",
        "amount_",
    ]

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab1", "Tab2"]:
            df: pd.DataFrame = load_pkdb_dataframe(
                f"{self.sid}_{fig_id}", data_path=self.data_path
            )
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                if (
                    label.startswith("hctz")
                    or label.startswith("amount")
                ):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[label] = dset

        # console.print(dsets.keys())
        # console.print(dsets)
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        # no simulation of fasting or different water amounts !
        tcsims["hctz50"] = TimecourseSim(
            Timecourse(
                start=0,
                end=50 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "PODOSE_hctz": Q_(50, "mg"),
                },
            )
        )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}

        for kg, group_key in enumerate(self.group_keys):
            for k, yid in enumerate(self.yids):
                prefix = self.prefixes[k]
                mappings[f"fm_{prefix}{group_key}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{prefix}{group_key}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_hctz50",
                        xid="time",
                        yid=yid,
                    ),
                    metadata=HCTZMappingMetaData(
                        tissue=Tissue.PLASMA if yid.startswith("[Cve_") else Tissue.URINE,
                        application_form=ApplicationForm.TABLET,
                        route=Route.PO,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=Coadministration.NONE,
                    ),
                )

        # console.print(mappings)
        return mappings

    def figures(self) -> Dict[str, Figure]:
        name = "Tab 1 & 2"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)
        plots[1].set_yaxis(self.label_hctz_urine, unit=self.unit_hctz_urine)

        for kg, group_key in enumerate(self.group_keys):
            group_label = self.group_labels[kg]

            # simulation
            for k, yid in enumerate(self.yids):
                plots[k].add_data(
                    task=f"task_hctz50",
                    xid="time",
                    yid=yid,
                    label=f"Sim hctz50",
                    color="black",
                )

            # data
            for k, prefix in enumerate(self.prefixes):
                plots[k].add_data(
                    dataset=f"{prefix}{group_key}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{group_label}",
                    color=self.colors[kg],
                )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Barbhaiya1982a, output_dir=Barbhaiya1982a.__name__)
