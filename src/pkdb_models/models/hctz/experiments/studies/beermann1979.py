"""Simulation experiment of the study Beermann1979."""

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
from sbmlsim.simulation import Simulation

from pkdb_models.models.hctz import MODEL
from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)


class Beermann1979(HCTZSimulationExperiment):
    """Simulation experiment of Beermann1979.

    HCTZ single oral doses 50 in patients with congestive heart failure.
    WITHOUT subject SL who was given 75 mg dose by mistake

    All patients were treated with a digitalis preparation, four of them had
    their frusemide changed to ethacrynic acid at least 24 hr before the study,
    and all patients were given ethacrynic acid in various doses on the
    following days (p. 579), i.e. on days 2 to 7 of the collection of the
    urine. The vocabulary has no member for digitalis (the preparation is not
    named) or ethacrynic acid, the mappings carry `Coadministration.COMEDICATION`
    for this chronic and concomitant medication.

    The urinary recovery of 21 to 37 % of the dose in SH, NK and GN indicates
    about half the absorption of healthy subjects, where it is about 70 %
    (p. 579, p. 582). The model keeps the absorbed fraction of healthy
    subjects: a reduced absorption in heart failure is not a process of the
    model, and an absorbed fraction per patient from his recovery would be
    fitted to the data it is compared with.
    """

    individuals: ClassVar[list[str]] = ["NL", "SP", "JG", "SH", "NK", "GN"]
    crcl: ClassVar[dict[str, int]] = {
        "NL": 27,
        "SP": 116,
        "JG": 19,
        "SH": 47,
        "NK": 53,
        "GN": 24,
    }  # [ml/min]
    dyspnea: ClassVar[dict[str, bool]] = {
        "NL": True,
        "SP": False,
        "JG": True,
        "SH": False,
        "NK": True,
        "GN": False,
    }
    colors: ClassVar[dict[str, str]] = {
        "NL": "tab:green",
        "SP": "black",
        "JG": "tab:green",
        "SH": "tab:green",
        "NK": "tab:green",
        "GN": "tab:green",
    }
    markers: ClassVar[dict[str, str]] = {
        "NL": ">",
        "SP": "s",
        "JG": "o",
        "SH": "^",
        "NK": "*",
        "GN": "<",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Tab3"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith(("hctz", "amount")):
                    dset.unit_conversion("value", 1 / self.Mr.hctz)
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[f"{fig_id}_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        for individual in self.individuals:
            # f_cardiac_function => severe
            f_cardiac = 3 / 5.25 if self.dyspnea[individual] else 3.5 / 5.25
            simulations[f"hctz50_{individual}"] = Simulation(
                time_unit="hr",
                end=250,
                steps=2000,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_hctz": Q(50, "mg"),
                    # the measured creatinine clearance includes the effect of
                    # the heart failure
                    "f_renal_function": self.renal_function(
                        self.crcl[individual], f_cardiac_function=f_cardiac
                    ),
                    "f_cardiac_function": Q(f_cardiac, "dimensionless"),
                    # the absorbed fraction of healthy subjects, see the
                    # docstring for the reduced absorption of the study
                },
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        # plasma, Fig1 shows the patients SP and NL
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
                observable=FitData(
                    self, task=f"task_hctz50_{individual}", xid="time", yid="[Cve_hctz]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.CARDIAC_RENAL_IMPAIRMENT,
                    fasting=Fasting.FASTED,
                    # digitalis, ethacrynic acid, see the docstring
                    coadministration=Coadministration.COMEDICATION,
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
                    self,
                    task=f"task_hctz50_{individual}",
                    xid="time",
                    yid="Aurine_hctz",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.URINE,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.CARDIAC_RENAL_IMPAIRMENT,
                    fasting=Fasting.FASTED,
                    # digitalis, ethacrynic acid, see the docstring
                    coadministration=Coadministration.COMEDICATION,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self._figure_Fig1(),
            **self._figure_Tab3(),
        }

    def _figure_Fig1(self) -> dict[str, Figure]:
        name = "Fig1"
        fig = Figure(
            experiment=self,
            sid=name,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", min=-5, max=80), legend=True
        )
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)

        # simulation
        for individual in ["SP", "NL"]:
            plots[0].add_data(
                task=f"task_hctz50_{individual}",
                xid="time",
                yid="[Cve_hctz]",
                label=f"Sim {individual}",
                color=self.colors[individual],
            )

            # data
            plots[0].add_data(
                dataset=f"Fig1_hctz50_{individual}",
                xid="time",
                yid="value",
                yid_sd=None,
                count="count",
                label=f"{individual} (CrCl {self.crcl[individual]} ml/min)",
                color=self.colors[individual],
                marker=self.markers[individual],
            )

        return {
            name: fig,
        }

    def _figure_Tab3(self) -> dict[str, Figure]:
        name = "Tab3"
        fig = Figure(
            experiment=self,
            sid=name,
            name=f"{self.__class__.__name__} {name}",
            # the legend of the 13 curves right of the plot, not over the data
            settings={"legend_scope": "row"},
        )

        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", min=-5, max=300), legend=True
        )
        plots[0].set_yaxis(self.label_hctz_urine, unit=self.unit_hctz_urine)

        # mean data from controls from Beermann1977a
        plots[0].add_data(
            dataset="Tab3_amount_HCTZ50",
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
                label=f"{individual} (CrCl {self.crcl[individual]} ml/min)",
                color=self.colors[individual],
                marker=self.markers[individual],
            )

        return {
            name: fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Beermann1979, output_dir=Beermann1979.__name__)
