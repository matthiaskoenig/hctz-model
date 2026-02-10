"""Intestine model for the diuretic hydrochlorothiazide."""

import numpy as np
from sbmlutils.converters import odefac

from sbmlutils.cytoscape import visualize_sbml
from sbmlutils.factory import *
from sbmlutils.metadata import *

from pkdb_models.models.hctz.models import templates
from pkdb_models.models.hctz.models import annotations


class U(templates.U):
    """UnitDefinitions"""

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
    annotations=annotations.model + [
        # tissue
        (BQB.OCCURS_IN, "fma/FMA:45615"),  # gut
        (BQB.OCCURS_IN, "bto/BTO:0000545"),  # gut
        (BQB.OCCURS_IN, "NCIT:C12736"),  # intestine
        (BQB.OCCURS_IN, "fma/FMA:7199"),  # intestine
        (BQB.OCCURS_IN, "bto/BTO:0000648"),  # intestine

        (BQB.HAS_PROPERTY, "NCIT:C79369"),  # Pharmacokinetics: Absorption
        # (BQB.HAS_PROPERTY, "NCIT:C79372"),  # Pharmacokinetics: Excretion
    ]
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
        1.2825 * 0.9,  # 0.0171 [l/kg] * 75 kg * 0.9, #
        name="intestinal lumen (inner part of intestine)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
        port=True,
        annotations=annotations.compartments["gu_lumen"],
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
    Compartment(
        "Ventero",
        np.nan,
        name="intestinal lining (enterocytes)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
    ),
    Compartment(
        "Vapical",
        np.nan,
        name="apical membrane (intestinal membrane enterocytes)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.m2,
        annotations=annotations.compartments["apical"],
        spatialDimensions=2,
    ),
    Compartment(
        "Vbaso",
        np.nan,
        name="basolateral membrane (intestinal membrane enterocytes)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.m2,
        annotations=annotations.compartments["basolateral"],
        spatialDimensions=2,
    ),
    Compartment(
        "Vstomach",
        metaId="meta_Vstomach",
        value=1,
        unit=U.liter,
        constant=True,
        name="stomach",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        port=True,
        annotations=annotations.compartments["stomach"],
    ),
]


_m.species = [
    Species(
        f"hctz_stomach",
        metaId=f"meta_hctz_stomach",
        initialConcentration=0.0,
        compartment="Vstomach",
        substanceUnit=U.mmole,
        name=f"hydrochlorothiazide (stomach)",
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["hctz"],
        boundaryCondition=True,
    ),
    Species(
        "hctz_lumen",
        initialConcentration=0.0,
        name="hydrochlorothiazide (intestinal volume)",
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
        f"F_hctz_abs",
        0.75,
        U.dimensionless,
        constant=True,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        name=f"fraction absorbed hydrochlorothiazide",
        notes="""
        Fraction absorbed, i.e., only a fraction of the hydrochlorothiazide in the intestinal lumen
        is absorbed. This parameter determines how much of the hydrochlorothiazide is excreted.
        
        `F_hctz_abs` of dose is absorbed. `(1-F_hctz_abs)` is excreted in feces.
        
        around 11-25% of dose recovered in feces {Beerman1976}
        around 60-70 percent urinary recovery of oral dose
        ~70-80 percent urinary recovery of oral dose [Barbhaiya1982]
        ~70 percent after oral dose, ~93% IV dose [Beerman1976]

        """,
    ),
    Parameter(
        "HCTZABS_k",
        0.002434587832023862,
        unit=U.per_min,
        name="rate of hydrochlorothiazide absorption",
        sboTerm=SBO.KINETIC_CONSTANT,
    ),
]

_m.rules.append(
    AssignmentRule(
        "absorption",
        value="HCTZABS_k * Vgu * hctz_lumen",
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
        compartment="Vapical",
        formula=("F_hctz_abs * absorption", U.mmole_per_min),
    ),
    Reaction(
        sid="HCTZEXC",
        name=f"excretion hydrochlorothiazide (feces)",
        compartment="Vlumen",
        equation=f"hctz_lumen -> hctz_feces",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=(
            f"(1 dimensionless - F_hctz_abs) * absorption",
            U.mmole_per_min,
        ),
    ),
]


_m.parameters.extend(
    [
        Parameter(
            f"PODOSE_hctz",
            0,
            U.mg,
            constant=False,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name=f"oral dose hydrochlorothiazide [mg]",
            port=True,
        ),
        Parameter(
            f"POSTOMACH_hctz",
            0,
            U.mg,
            constant=False,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name=f"oral dose in stomach hydrochlorothiazide [mg]",
        ),
        Parameter(
            f"Ka_application_hctz",
            1000,
            U.per_hr,
            constant=True,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name=f"Ka [1/hr] application hydrochlorothiazide",
            notes="""Fast application to shift applied dose in the stomach.""",
        ),
        Parameter(
            f"Ka_dis_hctz",
            2.0,
            U.per_hr,
            constant=True,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name=f"Ka_dis [1/hr] dissolution hydrochlorothiazide",
            port=True,
        ),
        Parameter(
            f"Mr_hctz",
            297.7,
            U.g_per_mole,
            constant=True,
            name=f"Molecular weight hydrochlorothiazide [g/mole]",
            sboTerm=SBO.MOLECULAR_MASS,
            port=True,
        ),
    ]
)

# -------------------------------------
# Dissolution of tablet/dose in stomach
# -------------------------------------
_m.reactions.extend(
    [
        # fraction dose available for absorption from stomach
        Reaction(
            sid=f"application_hctz",
            name=f"PO application hydrochlorothiazide",
            formula=(
                f"Ka_application_hctz/60 min_per_hr * PODOSE_hctz/Mr_hctz",
                U.mmole_per_min,
            ),
            equation=f" -> hctz_stomach",
            compartment="Vgu",
        ),
        # fraction dose available for absorption from stomach
        Reaction(
            sid=f"dissolution_hctz",
            name=f"dissolution hydrochlorothiazide",
            formula=(
                f"Ka_dis_hctz/60 min_per_hr * POSTOMACH_hctz/Mr_hctz",
                U.mmole_per_min,
            ),
            equation=f"hctz_stomach -> hctz_lumen",
            compartment="Vgu",
        ),
    ]
)
_m.rate_rules.extend(
    [
        RateRule(f"PODOSE_hctz", f"-application_hctz * Mr_hctz", U.mg_per_min),
        RateRule(
            f"POSTOMACH_hctz",
            f"(application_hctz - dissolution_hctz) * Mr_hctz",
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
    )
    # create differential equations
    md_path = MODEL_BASE_PATH / f"{model_intestine.sid}.md"
    ode_factory = odefac.SBML2ODE.from_file(sbml_file=results.sbml_path)
    ode_factory.to_markdown(md_file=md_path)

    visualize_sbml(results.sbml_path, delete_session=False)
