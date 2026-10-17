"""Simulation experiment of the study Ernst2006."""

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


class Ernst2006(HCTZSimulationExperiment):
    """Simulation experiment of Ernst2006.

    Untreated patients with prehypertension or stage 1 or 2 hypertension in a
    crossover of 8 weeks of HCTZ and 8 weeks of chlorthalidone with a washout
    of 4 weeks in between. Each drug was taken every morning, the first 4
    weeks at half of the target dose (HCTZ 25 mg, chlorthalidone 12.5 mg) and
    then force-titrated to the full dose (HCTZ 50 mg, chlorthalidone 25 mg).
    Fig1 gives the 24 hr mean of the ambulatory systolic blood pressure at
    weeks 0 and 8 of both periods of the 24 patients who completed both, by
    the order of the drugs. Time is in weeks from the start of the first
    period; the second period starts at week 12.

    The HCTZ periods are simulated: the first period of the HCTZ-first group
    and the second period of the chlorthalidone-first group, each from the
    systolic pressure of its week 0 as the reference of the model. The model
    has no chlorthalidone: the chlorthalidone periods are shown as data only,
    and the baseline of the second HCTZ period (4.4 mmHg below the one of the
    chlorthalidone period before it) carries the effect of the
    chlorthalidone, so its mapping is validation data of a limitation of the
    model.

    The 24 hr mean of the ABPM is compared with the pressure of the model at
    the visit, before the dose of the day; the pressure of the model varies
    by about 2 mmHg over a dosing interval.
    """

    #: the arms with HCTZ: the label of the data, the dataset with the data of
    #: the chlorthalidone period of the same subjects, and the day of the first
    #: dose
    arms: ClassVar[dict[str, tuple[str, str, int]]] = {
        "hctz_first": ("sbp_hctz_hctzfirst", "sbp_cltd_hctzfirst", 0),
        "hctz_second": ("sbp_hctz_cltdfirst", "sbp_cltd_cltdfirst", 84),
    }
    #: the systolic pressure at week 0 of the HCTZ period (Fig1)
    baselines: ClassVar[dict[str, float]] = {
        "hctz_first": 138.19,
        "hctz_second": 132.62,
    }
    #: the daily doses of the HCTZ periods: 28 days of 25 mg, 28 days of 50 mg
    #: and the dose of the day of the ABPM at the end of week 8, which runs on
    #: the treatment (the office pressure of a visit is measured at the trough,
    #: 23 to 26 hr after the dose of the day before)
    doses: ClassVar[list[float]] = [25.0] * 28 + [50.0] * 29

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df: pd.DataFrame = self.load_dataframe("Fig1")
        for label, df_label in df.groupby("label"):
            dsets[f"Fig1_{label}"] = DataSet.from_df(df_label, self.ureg)
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        for arm, (_, _, start) in self.arms.items():
            dose_times = [24 * (start + k) for k in range(len(self.doses))]
            changes = [
                Change([time], {"PODOSE_hctz": Q(dose, "mg")})
                for time, dose in zip(dose_times, self.doses, strict=True)
            ]
            # the 24 hr ABPM after the visit at the end of week 8
            end = 24 * (start + len(self.doses))
            simulations[arm] = Simulation(
                time_unit="hr",
                start=24 * start,
                end=end,
                steps=(end - 24 * start) * 2,
                preinit_changes={
                    **self.default_changes(),
                    "Psys_ref": Q(self.baselines[arm], "mmHg"),
                },
                changes=changes,
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for arm, (label, _, _) in self.arms.items():
            mappings[f"fm_Fig1_{label}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig1_{label}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_{arm}", xid="time", yid="bp_systolic"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.NONE,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.MULTIPLE,
                    health=Health.HYPERTENSION,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.NONE,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig1"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="week", min=-1, max=21), legend=True
        )
        for plot, title in zip(
            plots, ["HCTZ first", "Chlorthalidone first"], strict=True
        ):
            plot.set_title(title)
            plot.set_yaxis(
                self.labels["bp_systolic"],
                unit=self.units["bp_systolic"],
                min=100,
                max=150,
            )

        for k, (arm, (label, label_cltd, _)) in enumerate(self.arms.items()):
            # simulation
            plots[k].add_data(
                task=f"task_{arm}",
                xid="time",
                yid="bp_systolic",
                label="Sim HCTZ",
                color=self.color_hctz,
            )
            # data
            plots[k].add_data(
                dataset=f"Fig1_{label}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="HCTZ 25/50 mg",
                color=self.color_hctz,
            )
            plots[k].add_data(
                dataset=f"Fig1_{label_cltd}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="chlorthalidone 12.5/25 mg (no sim)",
                color="tab:gray",
            )

        return {
            name: fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Ernst2006, output_dir=Ernst2006.__name__)
