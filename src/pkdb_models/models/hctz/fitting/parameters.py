"""FitParameters for hydrochlorothiazide fitting."""

from sbmlsim.fit import FitParameter

parameters_pk = [
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

    # absorption
    FitParameter(
        pid="Ka_dis_hctz",
        start_value=1.0,
        lower_bound=1e-4,
        upper_bound=10,
        unit="1/hr",
    ),
    # FitParameter(
    #     pid="GU__F_hctz_abs",
    #     lower_bound=0.6,
    #     start_value=0.75,
    #     upper_bound=0.8,
    #     unit="dimensionless",
    # ),
    FitParameter(
        pid="GU__HCTZABS_k",
        lower_bound=1e-4,
        start_value=0.02,
        upper_bound=10,
        unit="1/min",
    ),
    # renal excretion
    # FitParameter(
    #     pid="KI__HCTZEX_k",
    #     start_value=1.0,
    #     lower_bound=1e-1,
    #     upper_bound=10,
    #     unit="1/min",
    # ),
    FitParameter(
        pid="KI__HCTZEX_Vmax",
        start_value=1.0,
        lower_bound=1e-4,
        upper_bound=10,
        unit="mmole/min/l",
    ),
    FitParameter(
        pid="KI__HCTZEX_Km",
        start_value=1E-3,
        lower_bound=1e-6,
        upper_bound=1E-2,
        unit="mM",
    ),


]
parameters_pd = [
    FitParameter(
        pid="vin_nacl",
        start_value=0.023766,
        lower_bound=0.01,
        upper_bound=0.2,
        unit="mmole/min",
    ),
    FitParameter(
        pid="E50_hctz_na",
        start_value=1E-4, # 0.1µm
        lower_bound=1e-6,
        upper_bound=1e-2,
        unit="mM",
    ),
    FitParameter(
        pid="E50_hctz_cl",
        start_value=1E-4,  # 0.1µm
        lower_bound=1e-6,
        upper_bound=1e-2,
        unit="mM",
    ),
    FitParameter(
        pid="E50_hctz_h2o",
        start_value=1E-4,  # 0.1µm
        lower_bound=1e-6,
        upper_bound=1e-2,
        unit="mM",
    ),
]

parameters_all = parameters_pk + parameters_pd
