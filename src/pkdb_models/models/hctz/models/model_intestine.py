"""Intestine model for the diuretic hydrochlorothiazide."""

import numpy as np
from sbmlutils.factory import (
    AssignmentRule,
    Compartment,
    Model,
    Parameter,
    RateRule,
    Reaction,
    Species,
    UnitDefinition,
    create_model,
)
from sbmlutils.metadata import BQB, SBO

from pkdb_models.models.hctz.models import annotations, templates
from pkdb_models.models.hctz.models.fits import FITS


class U(templates.U):
    """Units of the intestine model."""

    per_hr = UnitDefinition("per_hr", "1/hr")
    mg_per_min = UnitDefinition("mg_per_min", "mg/min")
    min_per_hr = UnitDefinition("min_per_hr", "min/hr")


_m = Model(
    "hctz_intestine",
    name="Model for hydrochlorothiazide absorption in the small intestine",
    notes="""
    # Model for hydrochlorothiazide absorption

    """
    + templates.terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
    annotations=[
        *annotations.model,
        # tissue
        (BQB.OCCURS_IN, "bto/BTO:0000545"),  # gut
        (BQB.OCCURS_IN, "NCIT:C12736"),  # intestine
        (BQB.OCCURS_IN, "fma/FMA:7199"),  # intestine
        (BQB.OCCURS_IN, "bto/BTO:0000648"),  # intestine
        (BQB.HAS_PROPERTY, "NCIT:C79369"),  # Pharmacokinetics: Absorption
        # (BQB.HAS_PROPERTY, "NCIT:C79372"),  # Pharmacokinetics: Excretion
    ],
)

_m.compartments = [
    Compartment(
        "Vext",
        1.0,
        name="plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["plasma"],
    ),
    Compartment(
        "Vgu",
        1.2825,  # 0.0171 [l/kg] * 75 kg
        name="intestine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["gu"],
    ),
    Compartment(
        "Vlumen",
        1.2825,  # 0.0171 [l/kg] * 75 kg
        name="intestinal lumen",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
        port=True,
        annotations=annotations.compartments["gu_lumen"],
        notes="""
        The volume the concentration of hydrochlorothiazide in the lumen of
        the intestine refers to; it is the volume of the intestine `Vgu`, the
        model has no volume of the lumen of its own.
        """,
    ),
    Compartment(
        "Vfeces",
        metaId="meta_Vfeces",
        value=1,
        unit=U.liter,
        constant=True,
        name="feces",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        port=True,
        annotations=annotations.compartments["feces"],
    ),
]


_m.species = [
    Species(
        "hctz_lumen",
        initialConcentration=0.0,
        name="hydrochlorothiazide (intestinal lumen)",
        compartment="Vlumen",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["hctz"],
        port=True,
    ),
    Species(
        "hctz_ext",
        initialConcentration=0.0,
        name="hydrochlorothiazide (plasma)",
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["hctz"],
        port=True,
    ),
    Species(
        "hctz_feces",
        initialConcentration=0.0,
        name="hydrochlorothiazide (feces)",
        compartment="Vfeces",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["hctz"],
        port=True,
    ),
]

_m.parameters = [
    Parameter(
        "F_hctz_abs",
        # the absorption of 14C-HCTZ in healthy subjects, 60-80 % (mean 70 %)
        # of the oral dose by the urinary excretion of the label [Beermann1976];
        # the PK fit PK_20261015_230510__951c0 gave 0.675 (0.64 to 0.70)
        0.70,
        U.dimensionless,
        constant=True,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        name="fraction absorbed hydrochlorothiazide",
        notes="""
        Fraction absorbed, i.e., only a fraction of the hydrochlorothiazide in the intestinal lumen
        is absorbed. This parameter determines how much of the hydrochlorothiazide is excreted.

        `F_hctz_abs` of dose is absorbed. `(1-F_hctz_abs)` is excreted in feces.

        around 11-25% of dose recovered in feces {Beermann1976}
        around 60-70 percent urinary recovery of oral dose
        ~70-80 percent urinary recovery of oral dose [Barbhaiya1982]
        ~70 percent after oral dose, ~93% IV dose [Beermann1976]

        """,
    ),
    Parameter(
        "HCTZABS_k",
        **FITS.parameter("GU__HCTZABS_k", unit=U.per_min),
        name="rate of hydrochlorothiazide absorption",
        sboTerm=SBO.KINETIC_CONSTANT,
    ),
]

_m.rules.append(
    AssignmentRule(
        "absorption",
        value="HCTZABS_k * Vlumen * hctz_lumen",
        unit=U.mmole_per_min,
        name="absorption hydrochlorothiazide",
    ),
)

_m.reactions = [
    Reaction(
        "HCTZABS",
        name="absorption hydrochlorothiazide",
        equation="hctz_lumen -> hctz_ext",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vgu",
        formula=("F_hctz_abs * absorption", U.mmole_per_min),
    ),
    Reaction(
        sid="HCTZEXC",
        name="excretion hydrochlorothiazide (feces)",
        compartment="Vlumen",
        equation="hctz_lumen -> hctz_feces",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=(
            "(1 dimensionless - F_hctz_abs) * absorption",
            U.mmole_per_min,
        ),
    ),
]


_m.parameters.extend(
    [
        Parameter(
            "PODOSE_hctz",
            0,
            U.mg,
            constant=False,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name="oral dose hydrochlorothiazide [mg]",
            port=True,
        ),
        Parameter(
            "POSOLUTION_hctz",
            0,
            U.mg,
            constant=False,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name="oral dose as solution hydrochlorothiazide [mg]",
            notes="""
            An oral dose given dissolved (a solution) enters the lumen of the
            intestine without the dissolution of `PODOSE_hctz`; the passage
            of the solution from the stomach is lumped into the absorption.
            """,
            port=True,
        ),
        Parameter(
            "POSTOMACH_hctz",
            0,
            U.mg,
            constant=False,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name="oral dose in stomach hydrochlorothiazide [mg]",
        ),
        Parameter(
            "Ka_application_hctz",
            1000,
            U.per_hr,
            constant=True,
            sboTerm=SBO.KINETIC_CONSTANT,
            name="Ka [1/hr] application hydrochlorothiazide",
            notes="""Fast application to shift applied dose in the stomach.""",
        ),
        Parameter(
            "application_hctz",
            np.nan,
            U.mmole_per_min,
            constant=False,
            sboTerm=SBO.RATE_OF_REACTION,
            name="PO application hydrochlorothiazide",
            notes="""
            The rate at which the oral dose `PODOSE_hctz` enters the stomach
            (`POSTOMACH_hctz`).
            """,
        ),
        Parameter(
            "Ka_dis_hctz",
            2.0,
            U.per_hr,
            constant=True,
            sboTerm=SBO.KINETIC_CONSTANT,
            name="Ka_dis [1/hr] dissolution hydrochlorothiazide",
            port=True,
        ),
        Parameter(
            "Mr_hctz",
            297.7,
            U.g_per_mole,
            constant=True,
            name="Molecular weight hydrochlorothiazide [g/mole]",
            sboTerm=SBO.MOLECULAR_MASS,
            port=True,
        ),
    ]
)

# -------------------------------------
# Dissolution of tablet/dose in stomach
# -------------------------------------
# the oral dose enters the stomach (`POSTOMACH_hctz`), from which it dissolves
# into the lumen of the intestine; the dose in the stomach is a parameter, no
# species
_m.rules.append(
    AssignmentRule(
        "application_hctz",
        "Ka_application_hctz/60 min_per_hr * PODOSE_hctz/Mr_hctz",
        unit=U.mmole_per_min,
    ),
)
_m.reactions.append(
    Reaction(
        sid="dissolution_hctz",
        name="dissolution hydrochlorothiazide",
        formula=(
            "Ka_dis_hctz/60 min_per_hr * POSTOMACH_hctz/Mr_hctz",
            U.mmole_per_min,
        ),
        equation="-> hctz_lumen",
        compartment="Vlumen",
        sboTerm=SBO.TRANSPORT_REACTION,
        notes="""
        Dissolution of the dose in the stomach and its passage into the
        lumen of the intestine.
        """,
    ),
)
_m.reactions.append(
    Reaction(
        sid="application_solution_hctz",
        name="application of the solution hydrochlorothiazide",
        formula=(
            "Ka_application_hctz/60 min_per_hr * POSOLUTION_hctz/Mr_hctz",
            U.mmole_per_min,
        ),
        equation="-> hctz_lumen",
        compartment="Vlumen",
        sboTerm=SBO.TRANSPORT_REACTION,
        notes="""
        The oral dose given as a solution enters the lumen of the intestine
        without dissolution.
        """,
    ),
)
_m.rate_rules.extend(
    [
        RateRule("PODOSE_hctz", "-application_hctz * Mr_hctz", U.mg_per_min),
        RateRule(
            "POSOLUTION_hctz",
            "-application_solution_hctz * Mr_hctz",
            U.mg_per_min,
        ),
        RateRule(
            "POSTOMACH_hctz",
            "(application_hctz - dissolution_hctz) * Mr_hctz",
            U.mg_per_min,
        ),
    ]
)

model_intestine = _m


if __name__ == "__main__":
    from pkdb_models.models.hctz import MODEL_BASE_PATH

    results = create_model(
        filepath=MODEL_BASE_PATH / f"{model_intestine.sid}.xml",
        model=model_intestine,
        sbml_level=3,
        sbml_version=2,
        create_antimony=False,
        create_markdown=True,
    )
