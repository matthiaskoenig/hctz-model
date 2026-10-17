"""Simulation experiment of the study Niemeyer1983."""

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


class Niemeyer1983(HCTZSimulationExperiment):
    """Simulation experiment of Niemeyer1983.

    single oral dosing of 50mg HCTZ.

    Fig1 shows three of the 23 subjects (Table 1, p. 662): patient C (71 years,
    arterial hypertension, creatinine clearance 106 ml/min) of group 1 with
    the normal renal function, patients S (30 ml/min) and W (10 ml/min), both
    with chronic glomerulonephritis, of group 3 with moderate to severe renal
    failure (creatinine clearance up to 30 ml/min). The patients were kept on
    their usual therapy, which is not reported, only diuretics were stopped at
    least 3 days before the dose (p. 662).

    The concentrations of 0 of patient C at 33 hr and of patient S at 48 hr
    are not quantified samples: the limit of the assay is not reported, and S
    has 91 ng/ml at 24 hr with a half-life of 15.4 hr (Table 3), i.e. about 30
    ng/ml at 48 hr. They are left out of the data.
    """

    group_labels: ClassVar[list[str]] = ["group 1", "group 3", "group 3"]
    patients: ClassVar[list[str]] = ["C", "S", "W"]
    crcl: ClassVar[list[int]] = [106, 30, 10]  #  [ml/min]
    health: ClassVar[list[Health]] = [
        Health.HYPERTENSION,
        Health.RENAL_IMPAIRMENT,
        Health.RENAL_IMPAIRMENT,
    ]
    colors: ClassVar[list[str]] = [
        "black",
        HCTZSimulationExperiment.renal_colors["Moderate renal impairment"],
        HCTZSimulationExperiment.renal_colors["Severe renal impairment"],
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            df: pd.DataFrame = self.load_dataframe(fig_id)
            # the samples without a quantified concentration, see the docstring
            df = df[df["value"] > 0]
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("hctz"):
                    dset.unit_conversion("value", 1 / self.Mr.hctz)
                dsets[f"{fig_id}_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        for kp, patient in enumerate(self.patients):
            simulations[f"hctz50_{patient}"] = Simulation(
                time_unit="hr",
                end=60,
                steps=500,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_hctz": Q(50, "mg"),
                    "f_renal_function": self.renal_function(self.crcl[kp]),
                },
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for kp, patient in enumerate(self.patients):
            mappings[f"fm_Fig1_hctz50_{patient}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig1_hctz50_{patient}",
                    xid="time",
                    yid="value",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_hctz50_{patient}", xid="time", yid="[Cve_hctz]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    application_form=ApplicationForm.TABLET,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    health=self.health[kp],
                    fasting=Fasting.FASTED,
                    # the usual therapy of the patients
                    coadministration=Coadministration.COMEDICATION,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self._figure_Fig1(),
            #    **self.figure_Fig2(),
        }

    def _figure_Fig1(self) -> dict[str, Figure]:
        name = "Fig1"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_hctz, unit=self.unit_hctz)

        # simulation
        for kp, patient in enumerate(self.patients):
            plots[0].add_data(
                task=f"task_hctz50_{patient}",
                xid="time",
                yid="[Cve_hctz]",
                label=f"Sim {patient}",
                color=self.colors[kp],
            )

            # data
            plots[0].add_data(
                dataset=f"Fig1_hctz50_{patient}",
                xid="time",
                yid="value",
                count="count",
                label=(
                    f"50 mg {patient}, {self.group_labels[kp]} "
                    f"(CrCl {self.crcl[kp]} ml/min)"
                ),
                color=self.colors[kp],
            )

        return {
            name: fig,
        }


if __name__ == "__main__":
    MODEL.run_experiments(Niemeyer1983, output_dir=Niemeyer1983.__name__)
