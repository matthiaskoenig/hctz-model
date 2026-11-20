"""The definition of the HCTZ model on the PBPK library `pkpdsim.pbpk`.

Hydrochlorothiazide (HCTZ) is a thiazide diuretic which is not metabolized:
it is filtered in the glomeruli and secreted into the urine by the proximal
tubule, taken up from the blood by the organic anion transporter OAT1. The
library builds the whole body, the segmented intestine with the dissolution
of the tablet and the absorption, and the kidney with the filtration and the
tubular transport; the fluid and electrolyte model of the package is the PD
component `FLUID`, which reads the HCTZ leaving the kidney and the urinary
excretion of HCTZ. The fitted values and their uncertainty are taken from the
records of the adopted fits (`models/fits.py`).
"""

from pkpdsim.pbpk import (
    Direction,
    Erythrocytes,
    Excretion,
    FirstOrder,
    FirstOrderDissolution,
    Kp,
    Membrane,
    ModelParameter,
    Organ,
    PBPKDefinition,
    PDComponent,
    Route,
    SegmentedIntestine,
    Substance,
    Transport,
    U,
    Value,
    Variants,
    fitted,
)

from pkdb_models.models.hctz.models import annotations, templates
from pkdb_models.models.hctz.models.fits import FITS
from pkdb_models.models.hctz.models.model_fluid import model_fluid

HCTZ = Substance(
    "hctz",
    name="hydrochlorothiazide",
    mr=297.7,
    annotations=annotations.species["hctz"],
    # no verified human value of the plasma protein binding (fu 1), see TODO.md
    binding=None,
    # HCTZ enters the erythrocytes; the rate of the exchange was not
    # identifiable in a fit with kinetic erythrocytes, they are in equilibrium
    erythrocytes=Erythrocytes(
        "equilibrium",
        bp=Value(
            1.7,
            U.dimensionless,
            notes=(
                "HCTZ accumulates in the erythrocytes, whole blood levels are 1.6 "
                "to 1.8 times those of the plasma (hydrochlorothiazide prescribing "
                "information, Clinical Pharmacology; https://www.guidelinecentral.com/"
                "drug/e31bd548-29ae-419a-831a-80ebb26e042f), the middle of the range."
            ),
        ),
    ),
    # the exchange of the tissues (`ftissue`) and the exchange of muscle of its
    # own: two time scales of the distribution, the early decline and the
    # terminal phase of the plasma
    distribution=Kp(
        value=fitted(FITS.parameter("Kp_hctz", unit=U.dimensionless)),
        ftissue=fitted(FITS.parameter("ftissue_hctz", unit=U.l_per_min)),
        ps={
            # per litre of muscle (`MU__kps_hctz`, the organ has `kps*Vmu`)
            Organ.MUSCLE: fitted(FITS.parameter("MU__kps_hctz", unit=U.per_min)),
        },
    ),
    excretion=Excretion(urine=True),
)
"""Hydrochlorothiazide."""

CHEMISTRY = [
    Transport(
        "HCTZUP",
        Organ.KIDNEY,
        "hctz",
        Direction.INFLUX,
        Membrane.BASOLATERAL,
        FirstOrder(
            k=fitted(
                FITS.parameter("KI__HCTZUP_k", unit=U.per_min),
                notes=(
                    "The uptake of HCTZ "
                    "from the blood into the proximal tubule cells by OAT1 "
                    "(SLC22A6): Uwai 2000 (rat OAT1, J Pharmacol Exp Ther 295, "
                    "261-265) and the human renal transporter experiments of "
                    "https://pmc.ncbi.nlm.nih.gov/articles/PMC6843032/ (TODO.md)."
                ),
            ),
            per_volume=True,
        ),
        protein="SLC22A6",
    ),
    Transport(
        "HCTZSEC",
        Organ.KIDNEY,
        "hctz",
        Direction.EFFLUX,
        Membrane.APICAL,
        FirstOrder(
            k=Value(
                10.0,
                U.l_per_min,
                notes=(
                    "The efflux of HCTZ from the proximal tubule cells into the "
                    "urine by MRP4 (ABCC4), fast so that the uptake by OAT1 "
                    "limits the secretion."
                ),
            ),
            per_volume=False,
        ),
        protein="ABCC4",
    ),
]
"""The tubular secretion of HCTZ: basolateral uptake (OAT1) and apical efflux (MRP4)."""


def fluid_component() -> PDComponent:
    """Get the fluid and electrolyte model as PD component of the body.

    The model reads the HCTZ concentration of the plasma leaving the kidney
    (the driver of its effect on the excretion of sodium and chloride), the
    urinary excretion rate of HCTZ (the HCTZ concentration of the urine), the
    body weight, the renal function, the GFR, the GFR at renal function 1 and
    the kidney volume of the body; it changes no parameter of the body.
    """
    return PDComponent(
        model=model_fluid,
        inputs={
            "C_hctz": "Cout_ki_hctz",
            "R_hctz": "Rurine_hctz",
            "BW": "BW",
            "f_renal_function": "f_renal_function",
            "GFR_body": "GFR",
            "GFR_base_body": "GFR_base",
            "Vki_body": "Vki",
        },
        outputs={},
    )


DEFINITION = PBPKDefinition(
    sid="hctz_body",
    substances=[HCTZ],
    chemistry=CHEMISTRY,
    variants=Variants(
        organs={
            Organ.SMALL_INTESTINE: SegmentedIntestine(
                ka=fitted(FITS.parameter("ka_hctz", unit=U.per_hr))
            )
        }
    ),
    routes=[
        Route.iv("hctz"),
        Route.oral(
            "hctz",
            FirstOrderDissolution(
                k=fitted(FITS.parameter("Ka_dis_hctz", unit=U.per_hr))
            ),
        ),
        Route.oral_solution("hctz"),
    ],
    pd=[fluid_component()],
    parameters=[
        ModelParameter(
            "Mr_ren",
            Value(
                45057,
                U.g_per_mole,
                notes=(
                    "The molecular weight of renin, the conversion of the plasma "
                    "renin of Giudicelli1987 (the value of the hand-written model)."
                ),
            ),
            U.g_per_mole,
            name="molecular weight renin",
        )
    ],
    name="Hydrochlorothiazide (HCTZ) body model",
    notes="""
    # Hydrochlorothiazide (HCTZ) body model

    Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model of
    hydrochlorothiazide, built with the PBPK library `pkpdsim.pbpk`: the whole
    body with the absorption of HCTZ in the intestine, its distribution into
    the tissues and its renal excretion by filtration and tubular secretion,
    and the fluid and electrolyte model of the PD (`FLUID`) with the effect of
    HCTZ on the excretion of sodium and chloride and the blood pressure.
    """
    + templates.terms_of_use,
    creators=templates.creators,
)
"""The HCTZ model."""
