"""Simulation experiment of the study Howes1991."""

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
    SamplingSite,
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


class Howes1991(HCTZSimulationExperiment):
    """Simulation experiment of Howes1991.

    Single oral dosing of 25mg HCTZ, alone or with 10mg enalapril.
    """

    #: the arms with HCTZ of the crossover study, every subject received each
    #: as a single dose: HCTZ alone, HCTZ and enalapril as separate tablets
    #: (`multi` in the labels of the data is the two tablets, not multiple
    #: dosing) and both in one combination tablet. Per arm the key, the suffix
    #: of the plasma data (Fig1), the interventions of the urine data (Tab2),
    #: the coadministration and the color.
    arms: ClassVar[list[tuple[str, str, str, Coadministration, str]]] = [
        (
            "alone",
            "_hydrochlorothiazide",
            "HCTZ25",
            Coadministration.NONE,
            "black",
        ),
        (
            "+ 10mg ENA separate",
            "_ENA10_multi_hydrochlorothiazide",
            "ENA10_HCTZ25",
            Coadministration.ENALAPRIL,
            "tab:blue",
        ),
        (
            "+ 10mg ENA combi",
            "_combi_ENA10_combi_hydrochlorothiazide",
            "ENA10_combi_HCTZ25_combi",
            Coadministration.ENALAPRIL,
            "tab:orange",
        ),
    ]

    #: the label of the urinary recovery in Tab2, followed by the interventions
    tab2_amount: ClassVar[str] = "cumulative_amount_hydrochlorothiazide_urine"

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Tab2"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.endswith("_hydrochlorothiazide") or label.startswith(
                    "cumulative_amount_hydrochlorothiazide"
                ):
                    dset.unit_conversion("mean", 1 / self.Mr["hctz"])
                elif label.endswith("_enalaprilat"):
                    pass
                dsets[self.to_sid(f"{fig_id}_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        simulations["hctz25"] = Simulation(
            time_unit="hr",
            end=100,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_hctz": Q(25, "mg"),
            },
        )
        return self.equilibrated_all(simulations)

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for _, suffix, interventions, coadministration, _ in self.arms:
            # plasma
            mappings[self.to_sid(f"fm_Fig1_HCTZ25{suffix}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig1_HCTZ25{suffix}"),
                    xid="time",
                    yid="mean",
                    yid_sd=None,
                    count="count",
                ),
                observable=FitData(
                    self, task="task_hctz25", xid="time", yid="Carm_hctz"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=coadministration,
                ),
            )
            # urine
            mappings[
                f"fm_Tab2_{interventions}_cumulative_amount_hydrochlorothiazide"
            ] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Tab2_{self.tab2_amount}_{interventions}_all",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_hctz25", xid="time", yid="Aurine_hctz"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.URINE,
                    sampling_site=SamplingSite.NOT_APPLICABLE,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=coadministration,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig1 & Tab2"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)
        plots[1].set_yaxis(label=self.label_hctz_urine, unit=self.unit_hctz_urine)

        # simulation
        for k, yid in enumerate(["Carm_hctz", "Aurine_hctz"]):
            plots[k].add_data(
                task="task_hctz25",
                xid="time",
                yid=yid,
                label="Sim",
                color=self.color_hctz,
            )

        # data
        for key, suffix, interventions, _, color in self.arms:
            # plasma
            plots[0].add_data(
                dataset=self.to_sid(f"Fig1_HCTZ25{suffix}"),
                xid="time",
                yid="mean",
                yid_sd=None,
                count="count",
                label=f"25 mg HCTZ {key}",
                color=color,
            )
            # urine
            plots[1].add_data(
                dataset=f"Tab2_{self.tab2_amount}_{interventions}_all",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"25 mg HCTZ {key}",
                linestyle="",
                color=color,
            )

        return {
            self.to_sid(name): fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Howes1991, output_dir=Howes1991.__name__)
