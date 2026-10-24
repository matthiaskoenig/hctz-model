"""Simulation experiment of the study Dussol2005."""

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
    ecf_expansion,
)


class Dussol2005(HCTZSimulationExperiment):
    """Simulation experiment of Dussol2005.

    Patients with chronic kidney disease (GFR 29 ml/min, DTPA) after a basal
    period took 25 mg HCTZ once daily for 30 days (and furosemide and both in
    other periods, not simulated). Table 2 gives the mean arterial pressure,
    Table 3 the 24 hr urine of the basal state and of the last day.

    The kidney disease of the patients is chronic, their basal state is the
    steady state of the impaired renal function: the extracellular fluid of
    the model expands with it and settles at (ECF/ECF_ref)^10 = 1 /
    f_renal_function, the pressures with it (in 68 hr to 95 %). The simulation
    therefore starts `equilibration` days before the first dose without HCTZ,
    and the references of the pressure are scaled so that the mean arterial
    pressure of the equilibrated state is the basal one.

    The urinary sodium is validation data (`fitting/mapping_collections.py`):
    the model has no sodium balance under chronic HCTZ. The excretion of
    sodium rises with HCTZ on every day, and only the intake, which rises as
    the plasma sodium falls, balances it: on the last day the model excretes
    313 mmol sodium (data 68 mmol) at a plasma sodium of 117 mM (data 138 mM).
    """

    #: the days of the drug-free run before the first dose
    equilibration: ClassVar[int] = 14

    #: the antihypertensive medication of the patients, which was not washed
    #: out and kept at its dose throughout the study (methods p350): beta
    #: blockers (5 of 7 patients), ACE inhibitors (5), AT1 receptor blockers
    #: (2), calcium channel blockers (3) and vasodilators (1); the diuretics
    #: (loop diuretic, 1) were withheld from 1 month before the study on. The
    #: vocabulary has no member of a mix of drugs, the comedication is
    #: `COMEDICATION`. The model has no effect of these drugs: they lower the
    #: basal pressure, which the references of the pressure are scaled to,
    #: and may blunt the effect of HCTZ on the pressure and the sodium balance
    coadministration: ClassVar[Coadministration] = Coadministration.COMEDICATION

    yids: ClassVar[dict[str, str]] = {"Vurine": "urinvol", "na_urine": "amount_na"}

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab2", "Tab3"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                dsets[f"{fig_id}_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        # GFR (DTPA) of the basal state 29 ml/min (Tab2); with HCTZ it falls to
        # 21 ml/min, the model has no effect of HCTZ on the GFR
        f_renal_function = self.renal_function(29)
        # the basal mean arterial pressure of 112 mmHg (Tab2) in the
        # equilibrated state: the systolic and diastolic references of the model
        # scaled to it and divided by the expansion of the extracellular fluid
        # of the steady state (exact within 0.1 %: the plasma sodium settles at
        # 139.8 mM, the relation assumes 140 mM)
        expansion = ecf_expansion(float(f_renal_function.magnitude))
        scale = 112 / ((120 + 2 * 80) / 3) / expansion

        # 30 doses, every 24 hours; the urine is emptied every day, so the
        # urine at a dose is the 24 hr collection before it
        dose_times = [24 * k for k in range(30)]
        days = [24 * k for k in range(1 - self.equilibration, 30)]
        simulations["hctz25"] = Simulation(
            time_unit="hr",
            start=-24 * self.equilibration,
            end=30 * 24,
            preinit_changes={
                **self.default_changes(),
                "f_renal_function": f_renal_function,
                "Psys_ref": Q(120 * scale, "mmHg"),
                "Pdia_ref": Q(80 * scale, "mmHg"),
            },
            changes=[
                self.add_doses(dose_times, {"PODOSE_hctz": Q(25, "mg")}),
                Change(
                    days,
                    {
                        "na_urine": Q(0, "mmole"),
                        "cl_urine": Q(0, "mmole"),
                        "Vurine": Q(1e-6, "l"),
                    },
                ),
            ],
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        mappings["fm_Tab2_map_hctz"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="Tab2_map_hctz",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
            ),
            observable=FitData(
                self,
                task="task_hctz25",
                xid="time",
                yid="bp_mean",
            ),
            metadata=PKPDMappingMetaData(
                tissue=Tissue.NONE,
                application_form=ApplicationForm.TABLET,
                route=Route.PO,
                dosing=Dosing.MULTIPLE,
                health=Health.RENAL_IMPAIRMENT,
                fasting=Fasting.NR,
                coadministration=self.coadministration,
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
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(self, task="task_hctz25", xid="time", yid=yid),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.URINE,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.MULTIPLE,
                    health=Health.RENAL_IMPAIRMENT,
                    fasting=Fasting.NR,
                    coadministration=self.coadministration,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self._figure_Tab2(),
            **self._figure_Tab3(),
        }

    def _figure_Tab2(self) -> dict[str, Figure]:
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
            task="task_hctz25",
            xid="time",
            yid="bp_mean",
            label="Sim (GFR 29 ml/min)",
            color="#2ca25f",
        )

        # data
        plots[0].add_data(
            dataset="Tab2_map_hctz",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="25 mg hctz",
            color="black",
            linestyle="",
        )

        return {
            name: fig,
        }

    def _figure_Tab3(self) -> dict[str, Figure]:
        name = "Tab3"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=2,
            num_cols=1,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        # room for the legend above the data of the last day
        plots[0].set_yaxis(self.label_urine_volume, self.unit_urine_volume, max=3000)
        plots[1].set_yaxis(self.label_na_urine, self.unit_na_urine)

        # simulation
        plots[0].add_data(
            task="task_hctz25",
            xid="time",
            yid="Vurine",
            label="Sim (GFR 29 ml/min)",
            color="#2ca25f",
        )

        plots[1].add_data(
            task="task_hctz25",
            xid="time",
            yid="na_urine",
            label="Sim (GFR 29 ml/min)",
            color="#2ca25f",
        )

        # data
        plots[0].add_data(
            dataset="Tab3_urinvol_hctz",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="25 mg hctz",
            color="black",
            linestyle="",
        )

        plots[1].add_data(
            dataset="Tab3_amount_na_hctz",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="25 mg hctz",
            color="black",
            linestyle="",
        )

        return {
            name: fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Dussol2005, output_dir=Dussol2005.__name__)
