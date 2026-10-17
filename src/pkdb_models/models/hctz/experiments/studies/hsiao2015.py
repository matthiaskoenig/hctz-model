"""Simulation experiment of the study Hsiao2015."""

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
from sbmlsim.simulation import Change, Simulation

from pkdb_models.models.hctz import MODEL
from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)


class Hsiao2015(HCTZSimulationExperiment):
    """Simulation experiment of Hsiao2015.

    Healthy subjects received 25 mg HCTZ once daily for 4 days alone (Period 1)
    and with 400 mg LCZ696 once daily (Period 3), after an overnight fast of at
    least 10 hours; the plasma was sampled at steady state after the dose of
    day 4 (p. 4, Study 1). The data refer to the last dose.
    """

    suffixes: ClassVar[list[str]] = ["hctz25", "hctz25_kombi"]
    colors: ClassVar[list[str]] = ["black", "tab:blue"]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[f"{fig_id}_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        # 4 doses, every 24 hours, the data is reported from the last dose
        dose_times = [24 * k for k in range(4)]
        simulations["hctz25"] = Simulation(
            time_unit="hr",
            end=dose_times[-1] + 30,
            steps=20 * (dose_times[-1] + 30),
            preinit_changes={
                **self.default_changes(),
            },
            changes=[Change(dose_times, {"PODOSE_hctz": Q(25, "mg")})],
            time_shift=-dose_times[-1],
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        # plasma
        for suffix in self.suffixes:
            mappings[f"fm_Fig1_{suffix}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig1_{suffix}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_hctz25", xid="time", yid="[Cve_hctz]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.MULTIPLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.LCZ696
                    if "kombi" in suffix
                    else Coadministration.NONE,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig1"
        fig = Figure(
            experiment=self,
            sid=name,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", min=-24, max=30), legend=True
        )
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)

        # simulation
        plots[0].add_data(
            task="task_hctz25",
            xid="time",
            yid="[Cve_hctz]",
            label="Sim",
            color=self.color_hctz,
        )
        # data
        for k, suffix in enumerate(self.suffixes):
            plots[0].add_data(
                dataset=f"Fig1_{suffix}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="25 mg HCTZ"
                if suffix == "hctz25"
                else "25 mg HCTZ + 400 mg LCZ696",
                color=self.colors[k],
            )

        return {
            name: fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Hsiao2015, output_dir=Hsiao2015.__name__)
