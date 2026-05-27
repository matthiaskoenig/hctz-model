"""FitParameters for hydrochlorothiazide fitting."""

from sbmlsim.fit import FitParameter

parameters_pk_po = [
    # absorption
    FitParameter(
        pid="Ka_dis_hctz",
        start_value=1.0,
        lower_bound=1e-4,
        upper_bound=10,
        unit="1/hr",
    ),
    FitParameter(
        pid="GU__F_hctz_abs",
        lower_bound=0.6,
        start_value=0.75,
        upper_bound=0.8,
        unit="dimensionless",
    ),
    FitParameter(
        pid="GU__HCTZABS_k",
        lower_bound=1e-4,
        start_value=0.02,
        upper_bound=10,
        unit="1/min",
    ),
]

parameters_pk_iv = [
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
        lower_bound=0.25,
        start_value=0.85,
        upper_bound=1.0,
        unit="dimensionless",
    ),

    # renal excretion
    FitParameter(
        pid="KI__HCTZEX_k",
        lower_bound=1e-10,
        start_value=1e-6,
        upper_bound=1,
        unit="1/ml",
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
parameters_pd = [
    # FitParameter(
    #     pid="vin_nacl",
    #     lower_bound=0.01,
    #     start_value=0.023766,
    #     upper_bound=0.2,
    #     unit="mmole/min",
    # ),
    FitParameter(
        pid="gamma_hctz_nacl",
        lower_bound=1,
        start_value=5,
        upper_bound=10,
        unit="dimensionless",
    ),
    FitParameter(
        pid="E50_hctz_nacl",
        lower_bound=1e-6,
        start_value=1E-4,
        upper_bound=1e-2,
        unit="mM",
    ),
    FitParameter(
        pid="Emax_hctz_na",
        lower_bound=1,
        start_value=5,
        upper_bound=20,
        unit="dimensionless",
    ),
    FitParameter(
        pid="Emax_hctz_cl",
        lower_bound=1,
        start_value=5,
        upper_bound=20,
        unit="dimensionless",
    ),
    FitParameter(
        pid="k_na",
        lower_bound=1E-10,
        start_value=1E-2,
        upper_bound=1E3,
        unit="l/min",
    ),
    FitParameter(
        pid="k_cl",
        lower_bound=1E-10,
        start_value=1E-2,
        upper_bound=1E3,
        unit="l/min",
    ),
]
parameters_pk = parameters_pk_iv + parameters_pk_po
parameters_all = parameters_pk + parameters_pd
