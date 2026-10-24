"""Simulation experiment of the study Hunninghake1986."""

from typing import override

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
from sbmlsim.simulation import Simulation

from pkdb_models.models.hctz import MODEL
from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)


class Hunninghake1986(HCTZSimulationExperiment):
    """Simulation experiment of Hunninghake1986.

    single oral dose of HCTZ 75 mg with and without various doses of Cholestyramin.

    Fig2 (p. 331) shows the urinary excretion of the definitive study in three
    periods: water only (control), 8 g cholestyramine 4 hr after HCTZ and
    24 g cholestyramine (16 g before and 8 g after HCTZ). The labels of the
    control and the multiple dose arm were swapped in the curation; the data
    follow Table II (p. 331), Ae(0-24) of 56 % of the dose (42 mg) in the
    control, 54 % (40.5 mg) with the single and 36 % (27 mg) with the multiple
    dose of cholestyramine. The subjects fasted for 4 hr after the dose
    (p. 329).
    """

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig2", "Fig3"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith(("hctz", "amount")):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[self.to_sid(f"{fig_id}_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        simulations["hctz75"] = Simulation(
            time_unit="hr",
            end=30,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_hctz": Q(75, "mg"),
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        for dset_id in [
            "Fig1_amount_cumulative_hctz75",
            "Fig2_amount_cumulative_hctz75_def",
        ]:
            mappings[self.to_sid(f"fm_{dset_id}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"{dset_id}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_hctz75", xid="time", yid="Aurine_hctz"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.URINE,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.CHOLESTYRAMINE
                    if "chol" in dset_id
                    else Coadministration.NONE,
                ),
            )

        mappings["fm_Fig3_hctz75"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="Fig3_hctz75",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
            ),
            observable=FitData(self, task="task_hctz75", xid="time", yid="[Cve_hctz]"),
            metadata=PKPDMappingMetaData(
                tissue=Tissue.PLASMA,
                application_form=ApplicationForm.TABLET,
                route=Route.PO,
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                fasting=Fasting.FASTED,
                coadministration=Coadministration.NONE,
            ),
        )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self._figure_Fig1_2_3(),
        }

    def _figure_Fig1_2_3(self) -> dict[str, Figure]:
        name = "Fig1_2_3"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(label=self.label_hctz, unit=self.unit_hctz)
        plots[1].set_yaxis(label=self.label_hctz_urine, unit=self.unit_hctz_urine)

        # simulation
        for k, yid in enumerate(["[Cve_hctz]", "Aurine_hctz"]):
            plots[k].add_data(
                task="task_hctz75",
                xid="time",
                yid=yid,
                label="Sim",
                color=self.color_hctz,
            )

        # data
        plots[0].add_data(
            dataset="Fig3_hctz75",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="75 mg",
            color="black",
        )

        for dset_id in [
            "Fig1_amount_cumulative_hctz75",
            "Fig2_amount_cumulative_hctz75_def",
        ]:
            plots[1].add_data(
                dataset=self.to_sid(dset_id),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="75 mg" if dset_id.startswith("Fig1") else "75 mg (def)",
                color="black" if dset_id.startswith("Fig1") else "tab:blue",
            )

        return {
            self.to_sid(name): fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Hunninghake1986, output_dir=Hunninghake1986.__name__)
