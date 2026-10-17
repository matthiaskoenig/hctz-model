"""Parameters to optimize in the HCTZ fits."""

from sbmlsim.fit import FitParameter

parameters_pk_po: list[FitParameter] = [
    # absorption
    FitParameter(
        pid="Ka_dis_hctz",
        start_value=1.0,
        lower_bound=1e-4,
        upper_bound=10,
        unit="1/hr",
    ),
    # the fraction absorbed GU__F_hctz_abs is not fitted, it is the absorption
    # of Beermann1976 (70 %)
    FitParameter(
        pid="GU__HCTZABS_k",
        lower_bound=1e-4,
        start_value=0.02,
        upper_bound=10,
        unit="1/min",
    ),
]

parameters_pk_iv: list[FitParameter] = [
    # tissue distribution
    FitParameter(
        pid="ftissue_hctz",
        lower_bound=0.01,
        start_value=0.1,
        upper_bound=10,
        unit="l/min",
    ),
    FitParameter(
        pid="Kp_hctz",
        # HCTZ has a large volume of distribution, partly by an uptake into
        # the erythrocytes which the model does not have; the fits stopped at
        # an upper bound of 3 (a profile open upwards, draws truncated at the
        # bound)
        lower_bound=0.25,
        start_value=0.85,
        upper_bound=10.0,
        unit="dimensionless",
    ),
    # renal excretion
    FitParameter(
        pid="KI__HCTZEX_f",
        lower_bound=0.1,
        start_value=2.5,
        upper_bound=10,
        unit="dimensionless",
    ),
    # FitParameter(
    #     pid="KI__HCTZEX_Vmax",
    #     lower_bound=1e-10,
    #     start_value=1e-5,
    #     upper_bound=1e-3,
    #     unit="mmole/l/ml",
    # ),
    # FitParameter(
    #     pid="KI__HCTZEX_Km",
    #     lower_bound=1e-7,
    #     start_value=1E-5,
    #     upper_bound=1E-2,   # 0.1 µm
    #     unit="mM",
    # ),
]
#: the parameters of the pharmacodynamics. The bounds keep the states
#: physiological: an Emax above 5 or a k_na outside of an intake of 50 to 300
#: mmol a day gave a sodium of 88 or 648 mM in the extracellular fluid; the
#: chloride is bounded by an intake of 1000 mmol a day
parameters_pd: list[FitParameter] = [
    # FitParameter(
    #     pid="vin_nacl",
    #     lower_bound=0.01,
    #     start_value=0.023766,
    #     upper_bound=0.2,
    #     unit="mmole/min",
    # ),
    FitParameter(
        pid="E50_hctz_nacl",
        lower_bound=1e-6,
        start_value=1e-4,
        upper_bound=1e-2,
        unit="mM",
    ),
    FitParameter(
        pid="Emax_hctz_na",
        lower_bound=0.1,
        start_value=2,
        upper_bound=5,
        unit="dimensionless",
    ),
    FitParameter(
        pid="Emax_hctz_cl",
        lower_bound=0.1,
        start_value=2,
        upper_bound=5,
        unit="dimensionless",
    ),
    # the intake is k_na * na_ref (140 mM): the bounds are an intake
    # of 50 to 300 mmol a day
    FitParameter(
        pid="k_na",
        lower_bound=2.5e-4,
        start_value=7e-4,
        upper_bound=1.5e-3,
        unit="l/min",
    ),
    # the intake is k_cl * cl_ref (102 mM): the bounds are an intake of 50 to
    # 1000 mmol a day; Williams1982 reports 20-34 mmol chloride an hour before
    # the dose (the fit stopped at an upper bound of 300 mmol a day)
    FitParameter(
        pid="k_cl",
        lower_bound=3.4e-4,
        start_value=2e-3,
        upper_bound=7e-3,
        unit="l/min",
    ),
]
parameters_pk: list[FitParameter] = parameters_pk_iv + parameters_pk_po
parameters_all: list[FitParameter] = parameters_pk + parameters_pd
