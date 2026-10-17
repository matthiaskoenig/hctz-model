"""Simulation experiment of the study Jeon2012."""

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
from sbmlsim.simulation import Change, Simulation

from pkdb_models.models.hctz import MODEL
from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)


class Jeon2012(HCTZSimulationExperiment):
    """Simulation experiment of Jeon2012.

    Multiple oral dosing of 25mg HCTZ.
    """

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3", "Fig4", "Fig5", "Fig6", "Tab2"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz") or (
                    fig_id == "Tab2" and label.startswith("amount_")
                ):
                    dset.unit_conversion("mean", 1 / self.Mr.hctz)
                # elif fig_id == "Fig5" and label.startswith("pra_"):
                #     dset.unit_conversion("mean", 1 / self.Mr.ren)
                # elif fig_id == "Fig5" and label.startswith("aldosterone_"):
                #     dset.unit_conversion("mean", 1 / self.Mr.ald)
                dsets[self.to_sid(f"{fig_id}_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        # 7 doses, every 24 hours, the data is reported from the last dose
        dose_times = [24 * k for k in range(7)]
        # the urine of the last dose is collected over 0-2, 2-4, 4-6, 6-12 and
        # 12-24 hr (Fig4 gives the volume of every collection): the urinary
        # volume is reset at the end of every collection, a data point at the
        # end of a collection is compared with the volume before the reset
        collection_ends = [dose_times[-1] + t for t in [2, 4, 6, 12, 24]]
        simulations["hctz25"] = Simulation(
            time_unit="hr",
            end=6 * 24 + 30,
            steps=4176,
            preinit_changes={
                **self.default_changes(),
                # # mean value of acute renin at baseline
                # "ren_ref": Q(7.58, "ng/ml") / self.Mr.ren,  # HCTZ25 mono
                # "[ren]": Q(7.58, "ng/ml") / self.Mr.ren,  # HCTZ25 mono
                # # mean value of acute aldosterone at baseline
                # "ald_ref": Q(209.58, "pg/ml") / self.Mr.ald,  # HCTZ25 mono
                # "[ald]": Q(209.58, "pg/ml") / self.Mr.ald,  # HCTZ25 mono
                # blood pressure
                # blood pressures were within predetermined criteria
                # (systolic blood pressure <140 and >100 mmHg and
                #  diastolic blood pressure <90 and >65 mmHg)
                "Psys_ref": Q((140 + 100) / 2, "mmHg"),  # HCTZ25 mono
                "Pdia_ref": Q((90 + 65) / 2, "mmHg"),  # HCTZ25 mono
            },
            changes=[
                Change(dose_times, {"PODOSE_hctz": Q(25, "mg")}),
                Change(
                    dose_times[1:],
                    {
                        "Aurine_hctz": Q(0, "mmole"),  # reset urinary amount
                        "Vurine": Q(1e-6, "l"),  # reset urinary volume
                    },
                ),
                Change(collection_ends, {"Vurine": Q(1e-6, "l")}),
            ],
            time_shift=-6 * 24,
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        infos = [
            ("Fig3_hctz25", "[Cve_hctz]", Tissue.PLASMA),
            ("Tab2_amount_cumulative_hctz25", "Aurine_hctz", Tissue.URINE),
            ("Fig4_urine_vol_hctz25", "Vurine", Tissue.URINE),
            # ("Fig5_pra_hctz25", "[ren]", Tissue.PLASMA),  # renin activity
            # ("Fig5_aldosterone_hctz25", "[ald]", Tissue.PLASMA),
            ("Fig6_bpsys_hctz25", "bp_systolic", Tissue.NONE),
            ("Fig6_bpdia_hctz25", "bp_diastolic", Tissue.NONE),
        ]

        for info in infos:
            (dset_id, yid, tissue) = info
            mappings[self.to_sid(f"fm_{dset_id}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(dset_id),
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
                    fasting=Fasting.FASTED,
                    coadministration=Coadministration.FIMASARTAN
                    if "fima240" in dset_id
                    else Coadministration.NONE,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self._figure_Fig3_Tab2(),
            **self._figure_Fig4(),
            # **self.figure_Fig5(),
            **self._figure_Fig6(),
        }

    def _figure_Fig3_Tab2(self) -> dict[str, Figure]:
        name = "Fig3_Tab2"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", min=-25, max=40), legend=True
        )
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)
        plots[1].set_yaxis(self.label_hctz_urine, unit=self.unit_hctz_urine)

        # simulation
        for k, yid in enumerate(["[Cve_hctz]", "Aurine_hctz"]):
            plots[k].add_data(
                task="task_hctz25",
                xid="time",
                yid=yid,
                label="Sim",
                color="black",
            )

        # data
        for suffix in ["hctz25", "hctz25_kombi"]:
            plots[0].add_data(
                dataset=self.to_sid(f"Fig3_{suffix}"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="25 mg HCTZ" if suffix == "hctz25" else "25 mg HCTZ + FIMA",
                color="black" if suffix == "hctz25" else "tab:blue",
            )
            plots[1].add_data(
                dataset=self.to_sid(f"Tab2_amount_cumulative_{suffix}"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="25 mg HCTZ" if suffix == "hctz25" else "25 mg HCTZ + FIMA",
                color="black" if suffix == "hctz25" else "tab:blue",
                linestyle="",
            )

        return {
            self.to_sid(name): fig,
        }

    def _figure_Fig4(self) -> dict[str, Figure]:
        name = "Fig 4"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            name=f"{self.__class__.__name__} {name}",
        )

        # the volume of every collection after the last dose, the simulation is
        # reset at the end of every collection; the upper limit leaves out the
        # volume of the 24 hr before the last dose
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", min=-1, max=30), legend=True
        )
        plots[0].set_yaxis(label="urine volume (collection)", unit="l", max=1.2)

        # simulation
        plots[0].add_data(
            task="task_hctz25",
            xid="time",
            yid="Vurine",
            label="Sim",
            color=self.color_hctz,
        )
        # data
        plots[0].add_data(
            dataset="Fig4_urine_vol_hctz25",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="25 mg HCTZ",
            color=self.color_hctz,
            linestyle="",
        )

        return {
            self.to_sid(name): fig,
        }

    # def figure_Fig5(self) -> Dict[str, Figure]:
    #     name = "Fig 5"
    #     fig = Figure(
    #         experiment=self,
    #         sid=name,
    #         num_rows=2,
    #         num_cols=1,
    #         name=f"{self.__class__.__name__} {name}",
    #     )
    #     plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr", min=-25, max=25), legend=True)
    #     plots[0].set_yaxis(self.labels["[ren]"], self.units["[ren]"])
    #     plots[1].set_yaxis(self.labels["[ald]"], self.units["[ald]"])
    #
    #     # simulation
    #     plots[0].add_data(
    #         task=f"task_hctz25",
    #         xid="time",
    #         yid="[ren]",
    #         label=f"Sim",
    #         color=self.color_hctz,
    #     )
    #     plots[1].add_data(
    #         task=f"task_hctz25",
    #         xid="time",
    #         yid="[ald]",
    #         label=f"Sim",
    #         color=self.color_hctz,
    #     )
    #     # data
    #     plots[0].add_data(
    #         dataset=f"Fig5_pra_hctz25",
    #         xid="time",
    #         yid="mean",
    #         yid_sd="mean_sd",
    #         count="count",
    #         label=f"25 mg HCTZ",
    #         color=self.color_hctz,
    #     )
    #     plots[1].add_data(
    #         dataset=f"Fig5_aldosterone_hctz25",
    #         xid="time",
    #         yid="mean",
    #         yid_sd="mean_sd",
    #         count="count",
    #         label=f"25 mg HCTZ",
    #         color=self.color_hctz,
    #     )
    #
    #     return {
    #         fig.sid: fig,
    #     }

    def _figure_Fig6(self) -> dict[str, Figure]:
        name = "Fig 6"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", min=-25, max=25), legend=True
        )
        plots[0].set_yaxis(self.labels["bp_systolic"], unit=self.units["bp_systolic"])
        plots[1].set_yaxis(self.labels["bp_diastolic"], unit=self.units["bp_diastolic"])

        # simulation
        plots[0].add_data(
            task="task_hctz25",
            xid="time",
            yid="bp_systolic",
            label="Sim",
            color=self.color_hctz,
        )
        plots[1].add_data(
            task="task_hctz25",
            xid="time",
            yid="bp_diastolic",
            label="Sim",
            color=self.color_hctz,
        )

        # data
        plots[0].add_data(
            dataset="Fig6_bpsys_hctz25",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="25 mg HCTZ",
            color=self.color_hctz,
        )
        plots[1].add_data(
            dataset="Fig6_bpdia_hctz25",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="25 mg HCTZ",
            color=self.color_hctz,
        )

        return {
            self.to_sid(name): fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Jeon2012, output_dir=Jeon2012.__name__)
