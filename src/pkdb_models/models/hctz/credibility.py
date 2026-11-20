"""The contexts of use of the HCTZ model and the evidence of its credibility.

Every context of use (COU) answers one question with the adopted fits `PK` and
`PD` (`MODEL.adopted_fits()`) and draws its evidence from the validation data of
`fitting/mapping_collections.py`, which is split by the question it answers:
the doses (`DOSE_VALIDATION`), the interactions (`INTERACTION_VALIDATION`), the
held-out subjects (`validation_individuals`, selected here as the validation
data which no other evidence claims) and the limitations
(`LIMITATION_VALIDATION`, data the model does not describe, subtracted from
every COU). See `docs/credibility.md` of pkpdsim for the vocabulary.

The impaired arms of HCTZ are training data of both fits, by the decision of
the maintainer (2026-11-10): the model is calibrated on them instead of holding
them out. The consequence is declared, not hidden: the COU `renal` carries them
as `EvidenceRole.CALIBRATION`, its only validation datum is the held-out patient
of Niemeyer1983, and it therefore reaches no verdict
(`insufficient_evidence`). No minimum is lowered and no claim narrowed to repair
that.

The questions, levels and domains follow the data. The influence, the
consequence and the rationale of every COU are a draft for the review of the
modeller.
"""

from pkpdsim.fit import metadata_filter
from pkpdsim.metadata import Coadministration, Dosing, Health, Route
from sbmlsim.credibility import (
    ContextOfUse,
    CouLevel,
    Credibility,
    Domain,
    Evidence,
    EvidenceRole,
    Level,
    QuantityOfInterest,
    Unclaimed,
)
from sbmlsim.fit.filters import named_filter
from sbmlsim.fit.variability import Variability
from sbmlsim.simulation.sampling import LogNormal

from pkdb_models.models.hctz.fitting.mapping_collections import (
    DOSE_VALIDATION,
    INTERACTION_VALIDATION,
    LIMITATION_VALIDATION,
)

#: the observables of the PK fit (`PK_OBSERVABLES`)
_PLASMA = QuantityOfInterest("Carm_hctz", "the plasma concentration of HCTZ")
_URINE = QuantityOfInterest("Aurine_hctz", "the cumulative amount of HCTZ in urine")
_FECES = QuantityOfInterest("Afeces_hctz", "the cumulative amount of HCTZ in feces")
_PK = (
    _PLASMA,
    _URINE,
    QuantityOfInterest("Rurine_hctz", "the urinary excretion rate of HCTZ"),
    _FECES,
)
#: the observables of the PK fit with validation data of single oral doses, the
#: excretion rate is training data only (Beermann1976)
_PK_VALIDATED = (_PLASMA, _URINE, _FECES)

#: the observables of the PD fit (`filter_pd`, the fluid and electrolyte model)
_SODIUM = QuantityOfInterest(
    "FLUID__na_urine", "the cumulative amount of sodium in urine"
)
_CHLORIDE = QuantityOfInterest(
    "FLUID__cl_urine", "the cumulative amount of chloride in urine"
)
_PD = (
    _SODIUM,
    _CHLORIDE,
    QuantityOfInterest("FLUID__Vurine", "the cumulative urine volume"),
    QuantityOfInterest("FLUID__bp_systolic", "the systolic blood pressure"),
    QuantityOfInterest("FLUID__bp_diastolic", "the diastolic blood pressure"),
)

#: single oral doses in healthy adults without a coadministered drug, the
#: domain of the doses and of the PD
_HEALTHY_PO = {
    "route": (Route.PO,),
    "health": (Health.HEALTHY,),
    "coadministration": (Coadministration.NONE,),
    "dosing": (Dosing.SINGLE,),
}

#: the fit mappings of the domain `_HEALTHY_PO`
_HEALTHY_PO_FILTER = metadata_filter(
    route={Route.PO},
    health={Health.HEALTHY},
    coadministration={Coadministration.NONE},
    dosing={Dosing.SINGLE},
)

#: patients with an impaired renal function, the domain of `renal`. The
#: comedication is not restricted: the patients of Niemeyer1983 stayed on their
#: usual therapy, which the study does not report (`STABLE_COMEDICATION`)
_RENAL = {
    "route": (Route.PO,),
    "health": (Health.RENAL_IMPAIRMENT,),
}

#: the fit mappings of the domain `_RENAL`
_RENAL_FILTER = metadata_filter(route={Route.PO}, health={Health.RENAL_IMPAIRMENT})

#: the drugs of the interaction arms of `INTERACTION_VALIDATION`
_COADMINISTRATIONS = (
    Coadministration.ALISKIREN,
    Coadministration.DILTIAZEM,
    Coadministration.ENALAPRIL,
    Coadministration.LISINOPRIL,
)

#: the variability between the subjects and between the studies, the input of the
#: visual predictive check (`run_credibility --variability`). The coefficients of
#: variation are a draft for the review of the modeller, typical values of the
#: between-subject variability of population PK analyses, not estimated: the
#: renal uptake (the clearance), the absorption, the body weight and the effect
#: on the sodium excretion of a subject, and the clearance and absorption of a
#: study (its population, formulation and assay)
VARIABILITY = Variability(
    {
        "KI__HCTZUP_k": LogNormal(cv=0.3),
        "ka_hctz": LogNormal(cv=0.4),
        "BW": LogNormal(cv=0.15),
        "FLUID__Emax_hctz_na": LogNormal(cv=0.3),
    },
    between=Variability(
        {"KI__HCTZUP_k": LogNormal(cv=0.3), "ka_hctz": LogNormal(cv=0.3)}
    ),
)

CREDIBILITY = Credibility(
    contexts=(
        ContextOfUse(
            id="describe",
            title="Describe the data of the fits",
            question=(
                "Does the model describe the pharmacokinetic and pharmacodynamic "
                "data of HCTZ it was fitted to?"
            ),
            level=CouLevel.C1,
            influence=Level.LOW,
            consequence=Level.LOW,
            quantities=(*_PK, *_PD),
            domain=Domain(
                metadata={
                    "route": (Route.PO, Route.IV),
                    "health": (
                        Health.HEALTHY,
                        Health.HYPERTENSION,
                        Health.RENAL_IMPAIRMENT,
                        Health.T2DM,
                    ),
                },
                statement=(
                    "the training data of the fits PK and PD: oral doses of 5 to "
                    "200 mg and intravenous doses of 1 to 65 mg, single and "
                    "multiple dosing; type 2 diabetes is PK data only. The "
                    "patients with an impaired renal function are training data "
                    "as well, by decision, so the renal behaviour of the model "
                    "(the GFR and the activity of SLC22A6, both scaled by "
                    "`f_renal_function`) is calibrated here and validated "
                    "nowhere, see `renal`"
                ),
            ),
            evidence=(
                Evidence(
                    "pharmacokinetics",
                    EvidenceRole.CALIBRATION,
                    metadata_filter(route={Route.PO, Route.IV}),
                    "the fitted plasma, urine and feces of HCTZ",
                    fit="PK",
                ),
                Evidence(
                    "pharmacodynamics",
                    EvidenceRole.CALIBRATION,
                    metadata_filter(route={Route.PO, Route.IV}),
                    "the fitted electrolytes, urine volume and blood pressure",
                    fit="PD",
                ),
            ),
            rationale=(
                "The figures of the HCTZ studies draw the fitted simulation over "
                "the plasma, the urine and the electrolytes it was fitted to, so "
                "a reader judges the description against its data (influence "
                "low); the description itself fixes no dose of HCTZ, the doses, "
                "the interactions and the natriuresis have held-out data of "
                "their own (consequence low). The PK fit describes 92 % of its "
                "training points within 2-fold (GMFE 1.30, AFE 0.98). The PD fit "
                "describes 89 % within 2-fold with a GMFE of 1.74 and a bias, an "
                "AFE of 0.68: the fluid and electrolyte model predicts about 30 % "
                "less than its data, the bias which `pd` carries."
            ),
        ),
        ContextOfUse(
            id="dose",
            title="Oral doses in healthy adults",
            question=(
                "Which plasma concentration and cumulative urinary and fecal "
                "excretion of HCTZ follow from a single oral dose within the range "
                "of the data in healthy adults?"
            ),
            level=CouLevel.C2,
            influence=Level.MEDIUM,
            consequence=Level.LOW,
            quantities=_PK_VALIDATED,
            domain=Domain(
                metadata=_HEALTHY_PO,
                statement=(
                    "single oral doses of 5 to 200 mg as tablet, capsule or "
                    "solution, fasted or not reported; validated on 5, 12.5, 50 "
                    "and 65 mg (5 to 65 mg), the doses of 75 to 200 mg are "
                    "calibration only; the urinary excretion rate is not claimed, "
                    "it has training data only (`describe`)"
                ),
            ),
            evidence=(
                Evidence(
                    "doses",
                    EvidenceRole.VALIDATION,
                    named_filter(DOSE_VALIDATION),
                    "a dose between the fitted doses of a study: the 50 mg tablet of "
                    "Patel1984 (25 and 100 mg fitted) and 12.5 mg of Jordo1979 (25 mg "
                    "fitted)",
                    fit="PK",
                ),
                Evidence(
                    "subjects",
                    EvidenceRole.VALIDATION,
                    Unclaimed(within=_HEALTHY_PO_FILTER),
                    "the held-out healthy subjects (`validation_individuals`): "
                    "Anderson1961 cases 1, 3 and 4, Azumaya1990 and Beermann1976 "
                    "subjects 1 and 2",
                    fit="PK",
                ),
                Evidence(
                    "fitted",
                    EvidenceRole.CALIBRATION,
                    _HEALTHY_PO_FILTER,
                    "the fitted single oral doses in healthy adults, shown with the "
                    "validation, which decides",
                    fit="PK",
                ),
            ),
            rationale=(
                "C2: the doses and subjects are inside the range of the training "
                "data. A dose within 5 to 200 mg which no study gave has its "
                "profile from the interpolation of the model, the two held-out "
                "doses and the held-out subjects are the check "
                "(influence medium); HCTZ has a wide therapeutic range and is "
                "titrated on the blood pressure, the exposure of a healthy adult "
                "sets no dose of a patient (consequence low)."
            ),
        ),
        ContextOfUse(
            id="renal",
            title="Impaired renal function",
            question=(
                "Which plasma concentration and urinary excretion of HCTZ, and "
                "which urinary excretion of sodium, follow from an oral dose in "
                "patients with an impaired renal function?"
            ),
            level=CouLevel.C3,
            influence=Level.MEDIUM,
            consequence=Level.MEDIUM,
            quantities=(_PLASMA, _URINE, _SODIUM),
            domain=Domain(
                metadata=_RENAL,
                statement=(
                    "single oral doses of 25 mg (Knauf1995, 19 patients with a "
                    "chronic renal insufficiency, creatinine clearance 1 to 153 "
                    "ml/min with the controls) and 50 mg (Niemeyer1983, patients "
                    "S and W, creatinine clearance 30 and 10 ml/min); the renal "
                    "function enters a simulation as `f_renal_function`, which "
                    "scales the GFR and, since the PBPK library of pkpdsim 0.21, "
                    "the activity of the tubular transporter SLC22A6 as well "
                    "(`fimp_ki_slc22a6`)"
                ),
            ),
            evidence=(
                Evidence(
                    "subjects",
                    EvidenceRole.VALIDATION,
                    Unclaimed(within=_RENAL_FILTER),
                    "the held-out patient of Niemeyer1983, the only data of an "
                    "impaired kidney which no fit sees",
                    fit="PK",
                ),
                Evidence(
                    "pharmacokinetics",
                    EvidenceRole.CALIBRATION,
                    _RENAL_FILTER,
                    "the fitted plasma of the renal patients of Niemeyer1983",
                    fit="PK",
                ),
                Evidence(
                    "pharmacodynamics",
                    EvidenceRole.CALIBRATION,
                    _RENAL_FILTER,
                    "the fitted sodium, chloride and urine of the patients with a "
                    "chronic renal insufficiency of Knauf1995",
                    fit="PD",
                ),
            ),
            rationale=(
                "C3: the renal function of a patient scales the GFR and the "
                "activity of SLC22A6, so the model extrapolates the exposure of "
                "an impaired kidney from the healthy one; a creatinine clearance "
                "which no study gave rests on that extrapolation (influence "
                "medium), and HCTZ loses its diuretic effect below a creatinine "
                "clearance of about 30 ml/min, which the natriuresis has to "
                "reproduce for the statement to carry (consequence medium). The "
                "impaired arms are training data by decision: the renal patients "
                "of Niemeyer1983 in the PK fit and the patients of Knauf1995 in "
                "the PD fit are calibration, not validation, so this COU rests on "
                "the fits it is assessed against. Its only independent datum is "
                "the held-out patient of Niemeyer1983, far below the minimum of a "
                "medium risk, so the verdict is `insufficient_evidence` by "
                "construction and is kept: the minimum is not lowered and the "
                "claim is not narrowed. The COU needs data of an impaired kidney "
                "which the fits do not use; the impaired patients of Anderson1961 "
                "cannot serve, they are a limitation (no measured creatinine "
                "clearance or cardiac output)."
            ),
        ),
        ContextOfUse(
            id="interaction",
            title="Coadministration without an interaction",
            question=(
                "Does the model predict the pharmacokinetics of HCTZ with "
                "coadministered aliskiren, diltiazem, enalapril or lisinopril "
                "without an interaction?"
            ),
            level=CouLevel.C3,
            influence=Level.MEDIUM,
            consequence=Level.MEDIUM,
            quantities=(
                _PLASMA,
                _URINE,
                QuantityOfInterest(
                    "hctz_auc_ratio",
                    "the AUC of HCTZ with the coadministered drug over the AUC "
                    "without it",
                    ratio=True,
                ),
            ),
            domain=Domain(
                metadata={
                    "route": (Route.PO,),
                    "health": (Health.HEALTHY,),
                    "coadministration": _COADMINISTRATIONS,
                },
                statement=(
                    "12.5 and 25 mg of HCTZ with the doses of the coadministered "
                    "drugs of the arms, single and multiple dosing, as separate "
                    "tablets and as combination tablets"
                ),
            ),
            evidence=(
                Evidence(
                    "interactions",
                    EvidenceRole.VALIDATION,
                    named_filter(INTERACTION_VALIDATION),
                    "the coadministration arms of Howes1991, Koytchev2004, "
                    "Niopas2004, Vaidyanathan2006 and Weir1998, which no fit sees",
                    fit="PK",
                ),
            ),
            rationale=(
                "C3: aliskiren, diltiazem, enalapril and lisinopril act on no "
                "process of HCTZ in the model, so every arm is HCTZ simulated as "
                "if given alone, the hypothesis that HCTZ needs no change with "
                "them. A combination tablet or a dose of the partner of no study "
                "rests on that simulation, the five studies are the check "
                "(influence medium); HCTZ is combined with these drugs in the "
                "treatment of hypertension and a prescriber keeps its dose on "
                "this statement (consequence medium). Step 3 of the assessment "
                "takes `hctz_auc_ratio`, the AUC ratio which states the absence "
                "of the interaction directly."
            ),
        ),
        ContextOfUse(
            id="pd",
            title="Natriuresis and chloruresis in healthy adults",
            question=(
                "Which urinary excretion of sodium and chloride follows from a "
                "single oral dose of HCTZ within the range of the data in healthy "
                "adults?"
            ),
            level=CouLevel.C5,
            influence=Level.MEDIUM,
            consequence=Level.LOW,
            quantities=(_SODIUM, _CHLORIDE),
            domain=Domain(
                metadata=_HEALTHY_PO,
                statement=(
                    "single oral doses of 12.5 to 100 mg, the cumulative excretion "
                    "after the dose; validated on the 50 mg tablet of Patel1984 "
                    "only (2 points, one sodium and one chloride value), the other "
                    "doses are calibration only; the urine volume and the blood "
                    "pressure are not claimed"
                ),
            ),
            evidence=(
                Evidence(
                    "doses",
                    EvidenceRole.VALIDATION,
                    named_filter(DOSE_VALIDATION),
                    "the sodium and chloride of the 50 mg tablet of Patel1984 (25 "
                    "and 100 mg fitted)",
                    fit="PD",
                ),
                Evidence(
                    "fitted",
                    EvidenceRole.CALIBRATION,
                    _HEALTHY_PO_FILTER,
                    "the fitted sodium and chloride of single oral doses in "
                    "healthy adults, shown with the validation",
                    fit="PD",
                ),
            ),
            rationale=(
                "C5: the PD of the fluid and electrolyte model, driven by the "
                "simulated PK. The sodium and chloride of a dose without PD data "
                "come from the model, the dose-response of the fitted studies is "
                "the check (influence medium); the natriuresis explains why HCTZ "
                "is a diuretic, its dose is titrated on the blood pressure "
                "(consequence low). Only sodium and "
                "chloride are claimed: the validation data of the urine volume "
                "(Beermann1977a, a water load) is a limitation and the blood "
                "pressure has no validation data (Jeon2012 is training data). The "
                "evidence is too thin for a verdict: two evaluable points, the "
                "sodium and the chloride of one dose of one study, below the "
                "minimum of 5 points of a low risk, so the COU is "
                "`insufficient_evidence` although both points are within 2-fold; "
                "the calibration has a bias besides, an AFE of 0.68 (0.72 in "
                "healthy adults), i.e. the model predicts about 30 % less "
                "electrolyte excretion than the data it was fitted to. The risk "
                "stays low, since it follows from the decision the answer informs "
                "and not from the evidence, and the minimum is not lowered: the "
                "COU needs PD validation data of further doses or studies."
            ),
        ),
    ),
    limitations=(
        Evidence(
            "limitations",
            EvidenceRole.LIMITATION,
            named_filter(LIMITATION_VALIDATION),
            "HCTZ data of processes which the model lacks: the patients with an "
            "impairment of Anderson1961 (no measured cardiac output or creatinine "
            "clearance, cirrhosis has no effect in the model, case 13 has lupus), "
            "the feces after intravenous doses of Beermann1976 (no non-renal "
            "elimination), the urine volumes of the water load of Beermann1977a "
            "(no water diuresis) and the single subject of Knauf1995 Fig1 (no "
            "variability between subjects)",
        ),
    ),
    notes=(
        "Renal impairment is claimed (`renal`) and calibrated: the impaired "
        "arms are training data by the decision of the maintainer, so the COU "
        "has one independent datum and reaches no verdict. Not claimed: "
        "hepatic and cardiac impairment (the "
        "impaired patients "
        "of Anderson1961 are a limitation, the single subjects of Beermann1979 are "
        "not described), the held-out hypertensive patients of Beermann1976 "
        "(50 mg, multiple dosing), multiple dosing without a coadministration, the "
        "terminal phase of the plasma beyond 24 hr, the urine volume and the blood "
        "pressure. The open points of HCTZ are in its TODO.md."
    ),
    variability=VARIABILITY,
)
