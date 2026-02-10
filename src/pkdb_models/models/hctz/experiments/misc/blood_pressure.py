from typing import Dict

from sbmlsim.plot import Axis, Figure, Plot
from sbmlsim.simulation import Timecourse, TimecourseSim

from pkdb_models.models.hctz.experiments.bp_experiment import BPSimulationExperiment
from pkdb_models.models.hctz.helpers import run_experiments


class BloodPressureExperiment(BPSimulationExperiment):
    """Tests of blood pressure model."""

    # sexes = {
    #     0: "male",
    #     1: "female",
    # }

    simulation_keys: list[str] = []

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        info = {
            "Reference": {},
            "Increase H2O uptake": {
                "vin_h2o": Q_(2.3/1440 * 2, "l/min"),
            },
            "Increase diuresis": {
                "k_h2o": Q_(0.0001173 * 2, "1/min"),
            },
            "Increase salt uptake": {
                "vin_nacl": Q_(0.023766 * 2, "mmole/min"),
            },
            "Increase Na excretion": {
                "k_na": Q_(0.00016975* 2, "l/min"),
            },
            "Increase Cl excretion": {
                "k_cl": Q_(0.000233 * 2, "l/min"),
            },
            "Increase ECF": {
                "ECF": Q_(13.6125 * 2, "l"),
            },
            "Increase HCTZ": {
                "[hctz]": Q_(0.1E-3, "mM"),
            },

        }
        self.simulation_keys = [key.replace(" ", "_") for key in info.keys()]

        tcsims = {}

        for key, changes in info.items():
            tcsims[f"bp_{key.replace(' ', '_')}"] = TimecourseSim([
                Timecourse(
                    start=0, # FIXME: report bug with event trigger; libroadrunner
                    end=24 * 60 * 5,  # [min]
                    steps=300,
                    changes={
                        **self.default_changes(),
                    },
                ),
                Timecourse(
                    start=0,
                    end=24 * 60 * 30,  # [min]
                    steps=300,
                    changes={
                        **changes,
                    },
                )
                ], time_offset=-24 * 60 * 5
            )

        return tcsims

    def figures(self) -> Dict[str, Figure]:
        # sex_colors = ["tab:blue", "tab:red"]
        figures: Dict[str, Figure] = {}

        info = [
            # fluid volumes
            ("ECF", 0),
            ("ECF_ref", 0),
            ("vin_h2o", 1),
            ("diuresis", 2),
            ("Vurine", 3),

            # blood pressure
            ("bp_systolic", 4),
            ("bp_diastolic", 4),

            # sodium
            ("vin_na", 8),
            ("[na]", 9),
            ("vout_na", 10),
            ("na_urine", 11),

            # chloride
            ("vin_cl", 12),
            ("[cl]", 13),
            ("vout_cl", 14),
            ("cl_urine", 15),
        ]

        for sim_key in self.simulation_keys:

            fig = Figure(
                experiment=self,
                sid=f"Fig_blood_pressure_{sim_key}",
                num_rows=4,
                num_cols=4,
                name=sim_key.replace("_", " "),
            )
            plots = fig.create_plots(xaxis=Axis("time", unit="day"), legend=True)
            task_id = f"task_bp_{sim_key}"
            for sid, ksid in info:
                plots[ksid].set_yaxis(label=self.labels[sid], unit=self.units[sid])
                plots[ksid].add_data(
                    task=task_id,
                    xid="time",
                    yid=sid,
                    label=sid,
                    color="black",
                )
            figures[fig.sid] = fig

        return figures


if __name__ == "__main__":
    run_experiments(
        BloodPressureExperiment, output_dir=BloodPressureExperiment.__name__
    )
