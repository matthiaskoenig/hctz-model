"""Simulation experiment of the study Weir1998."""

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


class Weir1998(HCTZSimulationExperiment):
    """Simulation experiment of Weir1998.

    Multiple dosing of hydrochlorothiazide 25 mg twice daily.
    """

    suffixes: ClassVar[list[str]] = ["", "_kombi"]
    colors: ClassVar[dict[str, str]] = {
        "": "black",
        "_kombi": "tab:blue",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2", "Fig3"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith(("hctz", "amount_", "excretion_")):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[f"{fig_id}_{label}"] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        # 11 doses, every 12 hours, the data is reported from the last dose
        dose_times = [12 * k for k in range(11)]
        simulations["hctz25"] = Simulation(
            time_unit="hr",
            end=10 * 12 + 60,
            steps=7200,
            preinit_changes=self.default_changes(),
            changes=[
                Change(dose_times, {"PODOSE_hctz": Q(25, "mg")}),
                # reset urine collection
                Change(dose_times[1:], {"Aurine_hctz": Q(0, "mmole")}),
            ],
            time_shift=-10 * 12,
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        infos = [
            ("Fig2_hctz25", "[Cve_hctz]", Tissue.PLASMA),
            # Tab4 is the same cumulative excretion as Fig3 (the table of the
            # figure); the excretion rates of its collections, which the
            # dataset Tab4 derives, are not fitted a second time
            ("Fig3_amount_cumulative_hctz25", "Aurine_hctz", Tissue.URINE),
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
                    observable=FitData(self, task="task_hctz25", xid="time", yid=yid),
                    metadata=PKPDMappingMetaData(
                        tissue=tissue,
                        application_form=ApplicationForm.TABLET,
                        route=Route.PO,
                        dosing=Dosing.MULTIPLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.NR,
                        coadministration=Coadministration.DILTIAZEM
                        if "kombi" in suffix
                        else Coadministration.NONE,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self._figure_Fig2_Fig3(),
        }

    def _figure_Fig2_Fig3(self) -> dict[str, Figure]:
        name = "Fig2_Fig3"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)
        plots[1].set_yaxis(label=self.label_hctz_urine, unit=self.unit_hctz_urine)

        # simulation
        for k, yid in enumerate(["[Cve_hctz]", "Aurine_hctz"]):
            plots[k].add_data(
                task="task_hctz25",
                xid="time",
                yid=yid,
                label="Sim",
                color=self.color_hctz,
            )

        # data
        for k, dset_id in enumerate(["Fig2_hctz25", "Fig3_amount_cumulative_hctz25"]):
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
            name: fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Weir1998, output_dir=Weir1998.__name__)
