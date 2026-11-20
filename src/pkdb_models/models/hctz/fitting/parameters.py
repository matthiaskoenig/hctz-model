"""Parameters to optimize in the HCTZ fits."""

from pkpdsim.pbpk import Organ, Sex, reference_individual
from sbmlsim.fit import FitParameter

#: the muscle of the reference individual of the library (organ with its blood)
#: [l], 29.742 l
V_MUSCLE = reference_individual(Sex.MALE).volumes[Organ.MUSCLE]

#: the PK start values are the bootstrap of the model on the PBPK library: the
#: values of the fit PK_20261017_025702__4167a of the hand-written model,
#: converted to the library where the equation changed (the port of the
#: model to `pkpdsim.pbpk`, `models/definition.py`); the bounds of a converted
#: parameter are its old bounds converted alike
parameters_pk_po: list[FitParameter] = [
    # absorption: the dissolution of the tablet and the absorption of the
    # dissolved drug in the intestine; the fraction absorbed is not a
    # parameter, it is the dose which is absorbed before the feces
    FitParameter(
        pid="Ka_dis_hctz",
        start_value=1.301410953539714,
        lower_bound=1e-4,
        upper_bound=10,
        unit="1/hr",
    ),
    # the absorption of the small intestine, the old rate in 1/min times 60
    FitParameter(
        pid="ka_hctz",
        lower_bound=6e-3,
        start_value=0.005071664631885059 * 60,
        upper_bound=600,
        unit="1/hr",
    ),
]

parameters_pk_iv: list[FitParameter] = [
    # tissue distribution: the exchange of the tissues but muscle;
    # the start value is the old exchange `ftissue*(Cp*Kp - Ct)` as the
    # library's `ftissue*fu*(Cp - Ct/Kp)` (fu 1), the old bounds times the old
    # Kp, the lower bound ten times lower (a fit reached the old one)
    FitParameter(
        pid="ftissue_hctz",
        lower_bound=0.0024,
        start_value=0.06371609687911314 * 2.364260595086214,
        upper_bound=24,
        unit="l/min",
    ),
    # the exchange of muscle per litre of muscle; the bounds 1e-4 to 10 l/min
    # over the muscle of the reference individual (`V_MUSCLE`), rounded to the
    # digits which the PEtab files keep
    FitParameter(
        pid="MU__kps_hctz",
        lower_bound=round(1e-4 / V_MUSCLE, 12),
        start_value=0.02279820792615332 / V_MUSCLE,
        upper_bound=round(10.0 / V_MUSCLE, 9),
        unit="1/min",
    ),
    FitParameter(
        pid="Kp_hctz",
        # the whole-tissue (interstitial and intracellular) to plasma
        # coefficient; the volume of distribution of HCTZ is 0.83 to 4.19 l/kg
        # (tests/models/test_hctz.py)
        lower_bound=0.25,
        start_value=2.364260595086214,
        upper_bound=10.0,
        unit="dimensionless",
    ),
    # renal excretion: the basolateral uptake by OAT1 (per litre of kidney)
    # which gives the renal clearance of the fitted hand-written model, the
    # old bounds of its factor [0.1, 10] times 0.6846/3.2377
    FitParameter(
        pid="KI__HCTZUP_k",
        lower_bound=0.0211459,
        start_value=0.6846452231454097,
        upper_bound=2.11459,
        unit="1/min",
    ),
]
#: the parameters of the pharmacodynamics, which start at the values of the
#: fit of the hand-written model (PD_20261017_030352__10c1d). The bounds keep
#: the states physiological: an Emax above 5 or a k_na outside of an intake of
#: 50 to 300 mmol a day gave a sodium of 88 or 648 mM in the extracellular
#: fluid; the chloride is bounded by an intake of 1000 mmol a day
parameters_pd: list[FitParameter] = [
    # FitParameter(
    #     pid="vin_nacl",
    #     lower_bound=0.01,
    #     start_value=0.023766,
    #     upper_bound=0.2,
    #     unit="mmole/min",
    # ),
    FitParameter(
        pid="FLUID__E50_hctz_nacl",
        lower_bound=1e-6,
        start_value=8.618253509248731e-05,
        upper_bound=1e-2,
        unit="mM",
    ),
    FitParameter(
        pid="FLUID__Emax_hctz_na",
        lower_bound=0.1,
        start_value=1.7254462780979103,
        upper_bound=5,
        unit="dimensionless",
    ),
    FitParameter(
        pid="FLUID__Emax_hctz_cl",
        lower_bound=0.1,
        start_value=0.4574899986773869,
        upper_bound=5,
        unit="dimensionless",
    ),
    # the intake is k_na * na_ref (140 mM): the bounds are an intake
    # of 50 to 300 mmol a day
    FitParameter(
        pid="FLUID__k_na",
        lower_bound=2.5e-4,
        start_value=0.0006766497411866952,
        upper_bound=1.5e-3,
        unit="l/min",
    ),
    # the intake is k_cl * cl_ref (102 mM): the bounds are an intake of 50 to
    # 1000 mmol a day; Williams1982 reports 20-34 mmol chloride an hour before
    # the dose (the fit stopped at an upper bound of 300 mmol a day)
    FitParameter(
        pid="FLUID__k_cl",
        lower_bound=3.4e-4,
        start_value=0.003707165531622856,
        upper_bound=7e-3,
        unit="l/min",
    ),
]
parameters_pk: list[FitParameter] = parameters_pk_iv + parameters_pk_po
parameters_all: list[FitParameter] = parameters_pk + parameters_pd
