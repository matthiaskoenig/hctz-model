"""Parameter scans hydrochlorothiazide."""
from typing import Dict

import matplotlib.axes
import matplotlib.cm as cm

import numpy as np
from sbmlsim.simulation import Timecourse, TimecourseSim, ScanSim, Dimension
from sbmlsim.plot.serialization_matplotlib import FigureMPL, MatplotlibFigureSerializer
from sbmlsim.plot.serialization_matplotlib import plt
from sbmlutils.console import console

from pkdb_models.models.hctz.experiments.base_experiment import (
    HCTZSimulationExperiment,
)
from pkdb_models.models.hctz.helpers import run_experiments


class HCTZParameterScan(HCTZSimulationExperiment):
    """Scan the effect of parameters on pharmacokinetics."""

    font = {"weight": "bold", "size": 20}
    tick_font_size = 17

    tend = 96 * 60
    steps = 2000
    doses_hctz = [0, 25]  # [mg]

    num_points = 10
    scan_map = {

        "renal_scan": {
            "parameter": "f_renal_function",
            # "range": np.linspace(0.1, 1.9, num=num_points),
            "default": 1.0,
            "range": np.sort(
                np.append(np.logspace(-1, 1, num=num_points), [1.0])
            ),  # [10^-1=0.1, 10^1=10]
            "scale": "log",
            "colormap": "Greens_r",
            "units": "dimensionless",
            "label": "renal function [-]",
        },
        "hepatic_scan": {
            "parameter": "f_cirrhosis",
            "default": 0.0,
            "range": np.linspace(0, 0.9, num=num_points),
            # "range": np.logspace(-2, 2, num=21),
            "scale": "linear",
            "colormap": "Blues",
            "units": "dimensionless",
            "label": "cirrhosis degree [-]",
        },
        "cardiac_scan": {
            "parameter": "f_cardiac_function",
            # "range": np.linspace(0.1, 1.9, num=num_points),
            "default": 1.0,
            "range": np.sort(
                # np.append(np.logspace(-1, 1, num=num_points), [1.0])
                np.append(np.linspace(0.5, 1.5, num=num_points), [1.0])
            ),  # [10^-1=0.1, 10^1=10]
            "scale": "linear",
            "colormap": "Reds_r",
            "units": "dimensionless",
            "label": "cardiac function [-]",
        },
        "dose_scan": {
            "parameter": "PODOSE_hctz",
            "default": 25,
            "range": np.sort(
                # np.append(np.linspace(1, 100, num=num_points), [10])
                [1, 2.5, 5, 12.5, 25, 30, 40, 50, 75, 100, 200]
            ),  # [10^-1=0.1, 10^1=10]
            # "range": np.sort(
            #     np.append(np.logspace(1, 2, num=num_points), [50])
            # ),  # [10^-1=0.1, 10^1=10]
            "scale": "linear",
            "colormap": "Purples",
            "units": "mg",
            "label": "hydrochlorothiazide dose [mg]",
        },
    }

    def simulations(self) -> Dict[str, ScanSim]:
        Q_ = self.Q_
        tcscans = {}

        for dose_hctz in self.doses_hctz:
            for scan_key, scan_data in self.scan_map.items():
                tcscans[f"scan_po{dose_hctz}_{scan_key}"] = ScanSim(
                    simulation=TimecourseSim(
                        Timecourse(
                            start=0,
                            end=self.tend,
                            steps=self.steps,
                            changes={
                                **self.default_changes(),
                                "PODOSE_hctz": Q_(dose_hctz, "mg"),
                            },
                        )
                    ),
                    dimensions=[
                        Dimension(
                            "dim_scan",
                            changes={
                                scan_data["parameter"]: Q_(
                                    scan_data["range"], scan_data["units"]
                                )
                            },
                        ),
                    ],
                )

        return tcscans

    def figures_mpl(self) -> Dict[str, FigureMPL]:
        """Matplotlib figures."""
        # calculate pharmacokinetic parameters
        self.pk_dfs = self.calculate_hctz_pk()
        self.pd_dfs = self.calculate_hctz_pd()

        # console.print(self.pd_dfs)

        return {
            **self.figures_mpl_timecourses(),
            **self.figures_mpl_pharmacokinetics(),
            **self.figures_mpl_pharmacodynamics(),
        }

    def figures_mpl_timecourses(self) -> Dict[str, FigureMPL]:
        """Timecourse plots for key variables depending on degree of renal impairment."""

        figures = {}
        for scan_key, scan_data in self.scan_map.items():
            range = scan_data["range"]
            rmin, rmax = range[0], range[-1]

            # cmap_str
            cmap_str = scan_data["colormap"]
            cmap = matplotlib.colormaps.get_cmap(cmap_str)

            # -----------------------------------
            # pharmacokinetics & pharmacodynamics
            # -----------------------------------
            sids = [
                "[Cve_hctz]",
                "Aurine_hctz",
                "Afeces_hctz",

                "NA_EXCRETION",
                "CL_EXCRETION",
                "diuresis",

                "ECF",
                "bp_systolic",
                "bp_diastolic",
            ]

            f, axes = plt.subplots(
                nrows=2,
                ncols=6,
                figsize=(6 * 6, 6 * 2),
                dpi=300,
                layout="constrained"
            )

            ymax = {}
            for ksid, sid in enumerate(sids):
                ymax[sid] = 0.0
                ax = axes.flatten()[ksid]

                # get data
                Q_ = self.Q_
                xres = self.results[
                    f"task_scan_po25_{scan_key}"
                ]

                # scanned dimension
                scandim = xres._redop_dims()[0]
                parameter_id = scan_data["parameter"]
                par_vec = Q_(
                    xres[parameter_id].values[0], xres.uinfo[parameter_id]
                )
                t_vec = xres.dim_mean("time").to(self.units["time"])

                for k_par, par in enumerate(par_vec):
                    c_vec = Q_(
                        xres[sid].sel({scandim: k_par}).values,
                        xres.uinfo[sid],
                    ).to(self.units[sid])

                    # update ymax
                    cmax = np.nanmax(c_vec.magnitude)
                    if cmax > ymax[sid]:
                        ymax[sid] = cmax

                    # 0.1 - 1.9
                    linewidth = 2.0
                    if np.isclose(scan_data["default"], par.magnitude):
                        color = "black"
                        t_vec_default = t_vec
                        c_vec_default = c_vec
                    else:
                        # red less function, blue more function
                        if scan_data["scale"] == "linear":
                            cvalue = (par.magnitude - rmin)/np.abs(rmax-rmin)
                        elif scan_data["scale"] == "log":
                            cvalue = (np.log10(par.magnitude) - np.log10(rmin)) / np.abs(np.log10(rmax) - np.log10(rmin))

                        color = cmap(cvalue)

                    ax.plot(
                        t_vec.magnitude,
                        c_vec.magnitude,
                        color=color,
                        linewidth=linewidth,
                    )

                # plot the reference line in black
                ax.plot(
                    t_vec_default.magnitude,
                    c_vec_default.magnitude,
                    color="black",
                    linewidth=2.0,
                )

                ax.set_xlabel(
                    f"{self.label_time} [{self.units['time']}]",
                    fontdict=self.font,
                )
                ax.set_ylabel(
                    f"{self.labels[sid]} [{self.units[sid].replace('dimensionless', '-')}]",
                    fontdict=self.font,
                )
                ax.tick_params(axis="x", labelsize=self.tick_font_size)
                ax.tick_params(axis="y", labelsize=self.tick_font_size)


            # --- colorbar ---
            # 4-tuple of floats rect = (left, bottom, width, height).
            # A new Axes is added with dimensions rect in normalized (0, 1)
            cb_ax = f.add_axes(rect=[0.07, 0.85, 0.07, 0.08])
            cb_ax.set_in_layout(True)

            # colorbar range
            if scan_data["scale"] == "linear":
                norm = matplotlib.colors.Normalize(vmin=rmin, vmax=rmax, clip=False)
            elif scan_data["scale"] == "log":
                norm = matplotlib.colors.LogNorm(vmin=rmin, vmax=rmax, clip=False)

            cbar = f.colorbar(
                cm.ScalarMappable(norm=norm, cmap=cmap_str),
                cax=cb_ax,
                orientation="horizontal",
            )

            # label
            cbar.ax.set_xlabel(
                scan_data["label"], **{"size": 15, "weight": "bold"}
            )
            cbar.ax.axvline(x=scan_data["default"], color="black", linewidth=2)

            # ticks
            ticks = [rmin, rmax]
            if scan_data["default"] not in ticks:
                ticks.append(scan_data["default"])
                ticks = sorted(ticks)
            cbar.set_ticks(ticks)
            cbar.set_ticklabels(
                ticks, **{"size": 15, "weight": "medium"}
            )

            figures[f"timecourse__pk__{scan_key}"] = f

        return figures

    def figures_mpl_pharmacokinetics(self):
        """Visualize dependency of pharmacokinetics parameters."""
        Q_ = self.Q_
        figures = {}

        parameters_info = {
            "hctz": [
                "aucinf",
                # "cmax",
                "kel",
                # "vd",
                "thalf",
                # "cl",
                # "cl_hepatic",
                # "cl_renal",
                # "cl_fecal",
            ],
        }
        colors = {
            "hctz": "black",
        }

        for scan_key, scan_data in self.scan_map.items():
            parameters = parameters_info["hctz"]
            f, axes = plt.subplots(
                nrows=1, ncols=len(parameters), figsize=(6 * len(parameters), 5), dpi=300,
                layout="constrained"
            )
            # f.suptitle(
            #     f"{names[substance]}",
            #     fontsize=self.suptitle_font_size,
            # )
            axes = axes.flatten()

            for substance, parameters in parameters_info.items():
                for k, pk_key in enumerate(parameters):
                    ax = axes[k]
                    ax.axvline(x=scan_data["default"], color="grey", linestyle="--")

                    ymax = 0.0

                    sim_key = f"scan_po25_{scan_key}"
                    xres = self.results[f"task_{sim_key}"]
                    df = self.pk_dfs[sim_key]
                    df = df[df.substance == substance]  # get PK for substance

                    # This was scanned
                    parameter_id = scan_data["parameter"]
                    x_vec = Q_(
                        xres[parameter_id].values[0], xres.uinfo[parameter_id]
                    )

                    pk_vec = df[f"{pk_key}"]
                    pk_vec = pk_vec.to_numpy()

                    x = x_vec
                    y = Q_(pk_vec, df[f"{pk_key}_unit"].values[0])

                    y = y.to(self.pk_units[pk_key])
                    ax.plot(
                        x,
                        y,
                        marker="o",
                        linestyle="-",
                        linewidth=2.0,
                        color=colors[substance],
                        markeredgecolor=colors[substance],
                        markeredgewidth=2.0,
                        markerfacecolor="white",
                        markersize=9,
                        label=f"{substance}",
                    )
                    ymax_value = np.nanmax(y.magnitude)
                    if ymax_value > ymax:
                        ymax = ymax_value


                    # ax.set_xlabel(scan_data["label"], fontdict=EnalaprilSimulationExperiment.scan_font)
                    ax.set_xlabel(
                        scan_data["label"],
                        fontdict=self.font,
                    )
                    ax.set_ylabel(
                        f"{self.pk_labels[pk_key]} [{self.pk_units[pk_key]}]",
                        fontdict=self.font,
                    )
                    ax.tick_params(
                        axis="x", labelsize=self.tick_font_size
                    )
                    ax.tick_params(
                        axis="y", labelsize=self.tick_font_size
                    )

                    # set axis
                    ax.set_ylim(bottom=0.0, top=1.05 * ax.get_ylim()[1])
                    # ax.set_ylim(bottom=0.0)
                    ax.set_xscale("log")
                    ax.legend(fontsize=HCTZSimulationExperiment.legend_font_size)


            figures[f"pk_{scan_key}"] = f
        return figures

    def figures_mpl_pharmacodynamics(self):
        """Visualize dependency of pharmacodynamic parameters."""
        Q_ = self.Q_
        figures = {}

        parameters = {
            "NA_EXCRETION": "max",
            "CL_EXCRETION": "max",
            "diuresis": "max",
            "bp_systolic": "min",
            "bp_diastolic": "min",
        }

        for scan_key, scan_data in self.scan_map.items():

            f, axes = plt.subplots(
                nrows=1, ncols=5, figsize=(6 * 5, 5), dpi=300,
                layout="constrained"
            )
            axes = axes.flatten()

            for k, sid in enumerate(parameters):
                pd_key = parameters[sid]

                ax = axes[k]
                ax.axvline(x=scan_data["default"], color="grey", linestyle="--")

                # ymax = 0.0
                for dose_hctz in self.doses_hctz:

                    if np.isclose(dose_hctz, 0) and scan_key == "dose_scan":
                        # not plotting placebo in the dose scan
                        continue

                    sim_key = f"scan_po{dose_hctz}_{scan_key}"
                    xres = self.results[f"task_{sim_key}"]
                    dfs = self.pd_dfs[sim_key]
                    df = dfs[sid]  # get PD for sid

                    # This was scanned
                    parameter_id = scan_data["parameter"]
                    x_vec = Q_(
                        xres[parameter_id].values[0], xres.uinfo[parameter_id]
                    )
                    pd_vec = df[f"{pd_key}"]
                    pd_vec = pd_vec.to_numpy()

                    x = x_vec
                    y = Q_(pd_vec, df[f"unit"].values[0])

                    y = y.to(self.units[sid])
                    ax.plot(
                        x,
                        y,
                        marker="o",
                        linestyle="-" if dose_hctz == self.doses_hctz[1] else "--",
                        linewidth=2.0,
                        color="black" if dose_hctz == self.doses_hctz[1] else "darkgray",
                        markeredgecolor="black",
                        markeredgewidth=2.0,
                        markerfacecolor="white",
                        markersize=9,
                        label="hctz" if dose_hctz == self.doses_hctz[1] else "placebo",
                    )
                    # ymax_value = np.nanmax(y.magnitude)
                    # if ymax_value > ymax:
                    #     ymax = ymax_value


                # ax.set_xlabel(scan_data["label"], fontdict=EnalaprilSimulationExperiment.scan_font)
                ax.set_xlabel(
                    scan_data["label"],
                    fontdict=self.font,
                )
                ax.set_ylabel(
                    f"{pd_key} {self.labels[sid]} [{self.units[sid].replace('dimensionless', '-')}]",
                    fontdict=self.font,
                )

                ax.tick_params(
                    axis="x", labelsize=self.tick_font_size
                )
                ax.tick_params(
                    axis="y", labelsize=self.tick_font_size
                )

                # set axis
                # ax.set_ylim(bottom=0.0, top=1.05 * ymax)
                # ax.set_ylim(bottom=0.0)
                ax.set_xscale("log")
                ax.legend(fontsize=HCTZSimulationExperiment.legend_font_size)

            figures[f"pd_{scan_key}"] = f
        return figures


if __name__ == "__main__":
    run_experiments(HCTZParameterScan, output_dir=HCTZParameterScan.__name__)
