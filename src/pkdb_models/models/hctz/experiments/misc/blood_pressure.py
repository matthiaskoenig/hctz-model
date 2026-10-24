"""Simulation experiment BloodPressureExperiment."""

from typing import override

from sbmlsim import Q
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Change, Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.hctz import MODEL
from pkdb_models.models.hctz.experiments.bp_experiment import BPSimulationExperiment


class BloodPressureExperiment(BPSimulationExperiment):
    """Response of the fluid and blood pressure model to perturbations."""

    @override
    def simulations(self) -> dict[str, Simulation]:
        ecf = 13.6125 * 2  # [l] the doubled extracellular fluid
        info: dict[str, dict[str, Quantity | float | str]] = {
            "Reference": {},
            "Increase H2O uptake": {
                "vin_h2o": Q(2.3 / 1440 * 1.5, "l/min"),
            },
            "Increase diuresis via GFR": {
                "GFR_base": Q(200, "ml/min"),
            },
            # "Increase Na excretion": {
            #     "k_na": Q(0.00016975* 2, "l/min"),
            # },
            # "Increase Cl excretion": {
            #     "k_cl": Q(0.000233 * 2, "l/min"),
            # },
            "Increase ECF": {
                "ECF": Q(ecf, "l"),
                # the amounts of the species in the ECF are kept, their
                # concentrations follow the volume [mmole/l]
                "[hctz]": f"hctz / {ecf}",
                "[na]": f"na / {ecf}",
                "[cl]": f"cl / {ecf}",
            },
            "Increase HCTZ": {
                "[hctz]": Q(0.1e-3, "mM"),
            },
        }
        simulations = {}

        # 5 days without a perturbation, then the perturbation for 30 days
        for key, changes in info.items():
            simulations[f"bp_{key.replace(' ', '_')}"] = Simulation(
                time_unit="hr",
                start=0,  # FIXME: report bug with event trigger; libroadrunner
                end=24 * 5 + 24 * 30,
                changes=[Change(24 * 5, changes)] if changes else [],
                time_shift=-24 * 5,
            )

        return simulations

    @override
    def figures(self) -> dict[str, Figure]:
        # the panels with their label and the curves (observable, color) they
        # show, sodium and chloride together; the unit is the one of the first
        panels: list[tuple[str, list[tuple[str, str]]]] = [
            ("Extracellular fluid", [("ECF", "black"), ("ECF_ref", "darkgrey")]),
            ("H2O uptake", [("vin_h2o", "black")]),
            ("Diuresis", [("diuresis", "black")]),
            ("Urine volume", [("Vurine", "black")]),
            (
                "Blood pressure",
                [("bp_systolic", "black"), ("bp_diastolic", "darkgrey")],
            ),
            ("Uptake", [("vin_na", "tab:blue"), ("vin_cl", "tab:green")]),
            ("Concentration (ECF)", [("[na]", "tab:blue"), ("[cl]", "tab:green")]),
            ("Excretion", [("vout_na", "tab:blue"), ("vout_cl", "tab:green")]),
            ("Urine", [("na_urine", "tab:blue"), ("cl_urine", "tab:green")]),
        ]

        figures: dict[str, Figure] = {}
        for sim_key in (key.removeprefix("bp_") for key in self._simulations):
            fig = Figure(
                experiment=self,
                sid=f"Fig_blood_pressure_{sim_key}",
                num_rows=3,
                num_cols=3,
                name=sim_key.replace("_", " "),
            )
            plots = fig.create_plots(xaxis=Axis("time", unit="day"), legend=True)
            for plot, (label, curves) in zip(plots, panels, strict=True):
                plot.set_yaxis(label=label, unit=self.units[curves[0][0]])
                for sid, color in curves:
                    plot.add_data(
                        task=f"task_bp_{sim_key}",
                        xid="time",
                        yid=sid,
                        label=self.labels[sid],
                        color=color,
                    )
            figures[f"Fig_blood_pressure_{sim_key}"] = fig

        return figures


if __name__ == "__main__":
    MODEL.run_experiments(
        BloodPressureExperiment, output_dir=BloodPressureExperiment.__name__
    )
