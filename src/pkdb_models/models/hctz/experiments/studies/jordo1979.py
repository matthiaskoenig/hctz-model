"""Simulation experiment of the study Jordo1979."""

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


class Jordo1979(HCTZSimulationExperiment):
    """Simulation experiment of Jordo1979.

    Single oral doses of 12.5 and 25 mg HCTZ to six healthy volunteers after a
    fast of at least 10 hours, the plasma for 25 hr and the urine for 48 hr
    (p. 563-564). HCTZ alone was "dissolved in 50 ml of an alcoholic solution
    (20%)" (p. 564), which is what the data are; the arms of the combination
    tablet with metoprolol are not part of the model.

    The model has no form of the dose: the solution dissolves like a tablet,
    with the fitted `Ka_dis_hctz`, which a fit sets in every experiment. Table 1
    gives a tmax of 1.3 hr for 25 mg in solution and 2.2 hr for the
    combination tablet.
    """

    doses: ClassVar[list[float]] = [12.5, 25]
    doses_keys: ClassVar[list[str]] = ["12_5", "25"]
    individuals: ClassVar[list[str]] = ["mean", "JD", "LB", "US", "AH", "LW", "TB"]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig2", "Tab2", "Tab2Mean"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz"):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                elif label.startswith("amount_"):
                    dset.unit_conversion("value", 1 / self.Mr.hctz)
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                dsets[self.to_sid(f"{fig_id}_{label}")] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        for dose in self.doses:
            simulations[self.to_sid(f"hctz{dose}")] = Simulation(
                time_unit="hr",
                end=60,
                steps=500,
                preinit_changes={
                    **self.default_changes(),
                    # HCTZ alone was an alcoholic solution (p. 564)
                    "POSOLUTION_hctz": Q(dose, "mg"),
                },
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        # Fig1_2
        for kd, dose in enumerate([12.5, 25]):
            fig_id = f"Fig{kd + 1}"
            mappings[self.to_sid(f"fm_{fig_id}_{dose}_hctz")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"{fig_id}_hctz{str(dose).replace('.', '_')}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_hctz{dose}"),
                    xid="time",
                    yid="[Cve_hctz]",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    application_form=ApplicationForm.SOLUTION,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.NONE,
                ),
            )

        # Tab2
        tab2_info = [
            (12.5, "Aurine_hctz", "amount_cumulative"),
            (25, "Aurine_hctz", "amount_cumulative"),
        ]
        for kd, individual in enumerate(self.individuals):
            for dose, yid, name in tab2_info:
                mappings[self.to_sid(f"fm_Tab2_{kd}_{dose}_{name}")] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(
                            f"Tab2Mean_{name}_hctz{str(dose).replace('.', '_')}"
                            if "mean" in individual
                            else f"Tab2_{name}_hctz{str(dose).replace('.', '_')}_{individual}"
                        ),
                        xid="time",
                        yid="mean" if "mean" in individual else "value",
                        yid_sd="mean_sd" if "mean" in individual else None,
                        count="count",
                    ),
                    observable=FitData(
                        self, task=self.to_sid(f"task_hctz{dose}"), xid="time", yid=yid
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.URINE,
                        application_form=ApplicationForm.SOLUTION,
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
            **self._figure_Fig1_2(),
            **self._figure_Tab2(),
        }

    def _figure_Fig1_2(self) -> dict[str, Figure]:
        name = "Fig1_2"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} {name}",
        )

        colors = ["tab:blue", "tab:orange"]
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", max=30),
            legend=True,
        )
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)

        # simulation
        for kd, dose in enumerate([12.5, 25]):
            plots[0].add_data(
                task=self.to_sid(f"task_hctz{dose}"),
                xid="time",
                yid="[Cve_hctz]",
                label=f"Sim {dose}",
                color=colors[kd],
            )
        # data
        for kd, dose in enumerate([12.5, 25]):
            plots[0].add_data(
                dataset=self.to_sid(f"Fig{kd + 1}_hctz{str(dose).replace('.', '_')}"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg",
                color=colors[kd],
            )

        return {
            self.to_sid(name): fig,
        }

    def _figure_Tab2(self) -> dict[str, Figure]:
        name = "Tab2"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(label=self.label_hctz_urine, unit=self.unit_hctz_urine)
        plots[1].set_yaxis(label=self.label_hctz_urine, unit=self.unit_hctz_urine)

        colors = ["black", "tab:blue", "tab:green", "red", "violet", "grey", "cyan"]

        # simulation
        for kplot, dose, yid in [
            (0, 12.5, "Aurine_hctz"),
            (1, 25, "Aurine_hctz"),
        ]:
            plots[kplot].add_data(
                task=self.to_sid(f"task_hctz{dose}"),
                xid="time",
                yid=yid,
                label=f"Sim {dose}",
                color="black",
            )

        # data
        for kd, individual in enumerate(self.individuals):
            for kplot, dose, name in [
                (0, 12.5, "amount_cumulative"),
                (1, 25, "amount_cumulative"),
            ]:
                plots[kplot].add_data(
                    dataset=self.to_sid(
                        f"Tab2Mean_{name}_hctz{str(dose).replace('.', '_')}"
                        if "mean" in individual
                        else f"Tab2_{name}_hctz{str(dose).replace('.', '_')}_{individual}"
                    ),
                    xid="time",
                    yid="mean" if "mean" in individual else "value",
                    yid_sd="mean_sd" if "mean" in individual else None,
                    count="count",
                    label=f"{individual}",
                    color=colors[kd],
                    linestyle="",
                )
        return {
            self.to_sid(name): fig,
        }

    ##### Plotting Tab2Mean which is the mean of individual data listed in Tab2
    # def figure_Tab2Mean(self) -> Dict[str, Figure]:
    #     name = "Tab2"
    #     fig = Figure(
    #         experiment=self,
    #         sid=name,
    #         num_rows=1,
    #         num_cols=1,
    #         name=f"{self.__class__.__name__} {name}",
    #     )
    #
    #     plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
    #     #plots[0].set_yaxis(label="urinary recovery", unit="percent") ##unable to model recovery yet hence conversion to cumulative amount below
    #     plots[0].set_yaxis(label="cumulative amount in urine", unit="mg")
    #
    #     # simulation ## recovery
    #     for kd, dose in enumerate(self.doses):
    #         dose_key = self.doses_keys[kd]
    #         plots[0].add_data(
    #             task=f"task_hctz{dose}",
    #             xid="time",
    #             yid="Aurine_hctz",         #FIXME
    #             label=f"Sim {dose_key}",
    #             color=self.color_hctz,
    #         )
    #
    #         # data
    #         plots[0].add_data(
    #             dataset=f"Tab2_amount_cumulative_hctz{dose_key}",
    #             xid="time",
    #             yid="mean",
    #             yid_sd="mean_sd",
    #             count="count",
    #             label=f"{dose} mg hydrochlorothiazide",
    #             color=self.color_hctz,
    #         )
    #
    #         return {
    #             fig.sid: fig,
    #         }


if __name__ == "__main__":
    MODEL.run_experiments(Jordo1979, output_dir=Jordo1979.__name__)
