from copy import deepcopy
from typing import Dict

from sbmlsim.plot import Axis, Figure, Plot
from sbmlsim.simulation import Timecourse, TimecourseSim

from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)
from pkdb_models.models.hctz.helpers import run_experiments


class DoseDependencyExperiment(HCTZSimulationExperiment):
    """Tests iv injection of HCTZ."""

    doses = [0, 50, 100, 200]  # [mg]
    colors = {
        0: "black",
        50: "tab:blue",
        100: "tab:orange",
        200: "tab:green"
    }
    routes = ["iv", "po"]

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        for route in self.routes:
            for dose in self.doses:
                tcsims[f"hctz_{route}_{dose}"] = TimecourseSim(
                    Timecourse(
                        start=0,
                        end=6 * 60 if route == "iv" else 5 * 24 * 60,  # [min]
                        steps=300,
                        changes={
                            **self.default_changes(),
                            f"{route.upper()}DOSE_hctz": Q_(dose, "mg"),
                        },
                    )
                )

        return tcsims

    def figures(self) -> Dict[str, Figure]:

        figures: Dict[str, Figure] = {}

        for route in self.routes:

            # pharmacokinetics
            pk_sids = [
                "[Cve_hctz]",
                "Aurine_hctz",
                "Afeces_hctz",
            ]
            fig = Figure(
                experiment=self,
                sid=f"Fig_application_pk_{route}",
                num_rows=3,
                num_cols=1,
                name=f"HCTZ {route.upper()}: pharmacokinetics",
            )
            plots = fig.create_plots(xaxis=Axis("time", unit="hr"), legend=True)
            for ksid, sid in enumerate(pk_sids):
                plots[ksid].set_yaxis(label=self.labels[sid], unit=self.units[sid])
                for kdose, dose in enumerate(self.doses):
                    # simulations
                    plots[ksid].add_data(
                        task=f"task_hctz_{route}_{dose}",
                        xid="time",
                        yid=sid,
                        label=f"HCTZ {dose} mg ({route})",
                        color=self.colors[dose],
                    )

            figures[fig.sid] = fig

            # pharmacodynamics
            pd_sids = [
                # RAAS
                # "[anggen]",
                ("[ren]", 0),
                ("[ang1]", 1),
                ("[ang2]", 2),
                ("[ald]", 3),

                ("NA_EXCRETION", 4),
                ("CL_EXCRETION", 5),
                ("diuresis", 6),

                # blood pressure
                # "HR",
                ("Vurine", 8),
                ("ECF", 9),
                ("bp_systolic", 10),
                ("bp_diastolic", 11),


                # "na_urine",  # sodium urine
                # "cl_urine",  # chloride urine
            ]
            fig = Figure(
                experiment=self,
                sid=f"Fig_application_pd_{route}",
                num_rows=3,
                num_cols=4,
                name=f"HCTZ {route.upper()}: pharmacodynamics",
            )
            plots = fig.create_plots(xaxis=Axis("time", unit="hr"), legend=True)
            for sid, ksid in pd_sids:
                plots[ksid].set_yaxis(label=self.labels[sid], unit=self.units[sid])
                for kdose, dose in enumerate(self.doses):
                    # simulations
                    plots[ksid].add_data(
                        task=f"task_hctz_{route}_{dose}",
                        xid="time",
                        yid=sid,
                        label=f"HCTZ {dose} mg ({route})",
                        color=self.colors[dose],
                    )

            figures[fig.sid] = fig

        return figures


if __name__ == "__main__":
    run_experiments(
        DoseDependencyExperiment, output_dir=DoseDependencyExperiment.__name__
    )
