"""Simulation experiment DoseDependencyExperiment."""

from typing import ClassVar, override

from sbmlsim import Q
from sbmlsim.plot import Figure
from sbmlsim.simulation import Change, Simulation

from pkdb_models.models.hctz import MODEL
from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)


class DoseDependencyExperiment(HCTZSimulationExperiment):
    """Dose dependency of HCTZ: single oral and intravenous doses, multiple oral doses."""

    doses: ClassVar[list[float]] = [
        100,
        50,
        25,
        12.5,
        0,
    ]  # [0, 12.5, 25, 50, 100]  # [mg]
    colors: ClassVar[dict[float, str]] = {
        0: "black",
        12.5: "tab:blue",
        25: "tab:orange",
        50: "tab:red",
        100: "tab:green",
    }
    routes: ClassVar[list[str]] = ["iv", "po"]
    applications: ClassVar[list[str]] = ["single", "multi"]

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        changes = {
            # 'KI__HCTZEX_f': Q(2.5, 'dimensionless')
        }

        for application in self.applications:
            for route in self.routes:
                if route == "iv" and application == "multi":
                    continue

                for dose in self.doses:
                    if application == "single":
                        simulations[
                            self.to_sid(f"hctz_{application}_{route}_{dose}")
                        ] = Simulation(
                            time_unit="hr",
                            end=5 * 24,
                            steps=1000,
                            preinit_changes={
                                **self.default_changes(),
                                **changes,
                                f"{route.upper()}DOSE_hctz": Q(dose, "mg"),
                            },
                        )
                    elif application == "multi":
                        # 9 doses, every 24 hours, followed for 5 days after the
                        # last dose
                        dose_times = [24 * k for k in range(9)]
                        simulations[
                            self.to_sid(f"hctz_{application}_{route}_{dose}")
                        ] = Simulation(
                            time_unit="hr",
                            end=8 * 24 + 5 * 24,
                            steps=3744,
                            preinit_changes={
                                **self.default_changes(),
                                **changes,
                            },
                            changes=[
                                Change(
                                    dose_times,
                                    {f"{route.upper()}DOSE_hctz": Q(dose, "mg")},
                                )
                            ],
                        )

        return simulations

    @override
    def figures(self) -> dict[str, Figure]:

        # pharmacokinetics/pharmacodynamics
        sids: list[tuple[str | None, str | None, int]] = [
            ("time", "[Cve_hctz]", 0),
            ("time", "ECF", 1),
            ("time", "[na]", 2),  # sodium ECF
            ("time", "[cl]", 3),  # chloride ECF
            ("time", "Aurine_hctz", 4),
            ("time", "diuresis", 5),
            ("time", "NA_EXCRETION", 6),
            ("time", "CL_EXCRETION", 7),
            ("time", "Afeces_hctz", 8),
            ("time", "H2O_UPTAKE", 9),
            ("time", "NA_UPTAKE", 10),
            ("time", "CL_UPTAKE", 11),
            # ("Aurine_hctz", "diuresis", 12),
            # ("Aurine_hctz", "NA_EXCRETION", 13),
            # ("Aurine_hctz", "CL_EXCRETION", 14),
            # (None, None, 15),
            ("time", "bp_systolic", 12),
            ("time", "bp_diastolic", 13),
            ("[Cve_hctz]", "bp_systolic", 14),
            ("[Cve_hctz]", "bp_diastolic", 15),
        ]

        figures: dict[str, Figure] = {}

        for application in self.applications:
            for route in self.routes:
                if route == "iv" and application == "multi":
                    continue

                fig = Figure(
                    experiment=self,
                    sid=self.to_sid(f"Fig_hctz_{application}_{route}"),
                    num_rows=4,
                    num_cols=4,
                    settings={"legend_scope": "row"},
                    name=f"HCTZ {application} dose {route.upper()}",
                )
                plots = fig.create_plots(legend=True)
                for xid, yid, ksid in sids:
                    if xid is None or yid is None:
                        # empty panel, no data is plotted on it
                        plots[ksid].xaxis = None
                        plots[ksid].yaxis = None
                        continue

                    plots[ksid].set_xaxis(label=self.labels[xid], unit=self.units[xid])
                    plots[ksid].set_yaxis(label=self.labels[yid], unit=self.units[yid])
                    for dose in self.doses:
                        label = f"HCTZ {dose} mg" if dose > 0 else "Placebo"

                        # simulations
                        plots[ksid].add_data(
                            task=self.to_sid(f"task_hctz_{application}_{route}_{dose}"),
                            xid=xid,
                            yid=yid,
                            label=label,
                            color=self.colors[dose],
                        )

                figures[self.to_sid(f"Fig_hctz_{application}_{route}")] = fig

        return figures


if __name__ == "__main__":
    MODEL.run_experiments(
        DoseDependencyExperiment, output_dir=DoseDependencyExperiment.__name__
    )
