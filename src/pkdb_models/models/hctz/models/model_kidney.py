"""Kidney model for the diuretic Hydrochlorothiazide."""

import numpy as np
from sbmlutils.factory import (
    AssignmentRule,
    Compartment,
    FactoryResult,
    Model,
    Parameter,
    Reaction,
    Species,
    UnitDefinition,
    create_model,
)
from sbmlutils.metadata import BQB, SBO

from pkdb_models.models.hctz.models import annotations, templates
from pkdb_models.models.hctz.models.fits import FITS


class U(templates.U):
    """Units of the kidney model."""

    ml = UnitDefinition("ml", "ml")
    per_hr = UnitDefinition("per_hr", "1/hr")
    per_ml = UnitDefinition("per_ml", "1/ml")
    l_per_ml = UnitDefinition("l_per_ml", "l/ml")
    mg_per_min = UnitDefinition("mg_per_min", "mg/min")
    ml_per_min = UnitDefinition("ml_per_min", "ml/min")
    mmole_per_l_ml = UnitDefinition("mmole_per_l_ml", "mmole/l/ml")


_m = Model(
    "hctz_kidney",
    name="Model for hydrochlorothiazide excretion into the urine",
    notes="""
    # Model for hydrochlorothiazide renal excretion

    - "Renal dysfunction in patients with heart failure (HF) has traditionally been attributed to declining cardiac
      output and renal hypoperfusion. However, other central haemodynamic aberrations may contribute to impaired
      kidney function."[Bobbio2022]

    - "Diuresis (urine output) is closely linked to sodium (Na+) and chloride (Cl-) excretion, as these ions drive
       osmotic water reabsorption in the nephron; higher electrolyte excretion reduces reabsorption,
       increasing urine volume."

    """
    + templates.terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
    annotations=[
        *annotations.model,
        # tissue
        (BQB.OCCURS_IN, "fma/FMA:7203"),  # kidney
        (BQB.OCCURS_IN, "bto/BTO:0000671"),  # kidney
        (BQB.OCCURS_IN, "NCIT:C12415"),  # kidney
        (BQB.HAS_PROPERTY, "NCIT:C79372"),  # Pharmacokinetics: Excretion
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
        "Vki",
        value=0.3,  # 0.4 % of bodyweight
        unit=U.liter,
        name="kidney",
        constant=True,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["ki"],
        port=True,
    ),
    Compartment(
        "Vurine",
        1.0,
        name="urine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["urine"],
    ),
]

_m.species = [
    Species(
        "hctz_ext",
        name="hydrochlorothiazide (plasma)",
        initialConcentration=0.0,
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["hctz"],
        port=True,
    ),
    Species(
        "hctz_urine",
        name="hydrochlorothiazide (urine)",
        initialConcentration=0.0,
        compartment="Vurine",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["hctz"],
        port=True,
    ),
]

_m.parameters = [
    Parameter(
        "f_renal_function",
        1.0,
        U.dimensionless,
        name="renal function",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
           >1.0: increased kidney function
           1.0: normal kidney function (healthy control)
           <1.0: decreased kidney function
        """,
        port=True,
    ),
    Parameter(
        "GFR_base",
        100,
        U.ml_per_min,
        name="glomerular filtration rate (base)",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        port=True,
    ),
]
_m.parameters.extend(
    [
        Parameter(
            "HCTZEX_f",
            **FITS.parameter("KI__HCTZEX_f", unit=U.dimensionless),
            name="intrinsic renal clearance of hydrochlorothiazide relative to the GFR",
            sboTerm=SBO.KINETIC_CONSTANT,
            notes="""
            The intrinsic renal clearance of HCTZ is HCTZEX_f times the GFR
            (filtration and secretion), acting on the renal venous plasma of a
            well-stirred kidney: the systemic renal clearance is
            Qki * CLint/(Qki + CLint), limited by the renal blood flow (2.26
            GFR at renal function 1 with HCTZEX_f 2.68, 2.63 at 0.1 and 1.96
            at 2). It scales with the body weight as the GFR does (linearly).
            """,
        ),
        # Parameter(
        #     "HCTZEX_Vmax",
        #     0.002521976126922892,
        #     U.mmole_per_l_ml,
        #     name="rate urinary excretion of hydrochlorothiazide",
        #     sboTerm=SBO.KINETIC_CONSTANT,
        # ),
        # Parameter(
        #     "HCTZEX_Km",
        #     0.0028843086768038048,
        #     U.mM,
        #     name="Michaelis constant excretion of hydrochlorothiazide",
        #     sboTerm=SBO.MICHAELIS_CONSTANT,
        # ),
        Parameter(
            "v_HCTZEX",
            np.nan,
            U.mmole_per_min,
            name="rate of HCTZ excretion",
            constant=False,
            port=True,
        ),
    ]
)
_m.rules.extend(
    [
        AssignmentRule(
            variable="GFR",
            value="f_renal_function * GFR_base",
            unit=U.ml_per_min,
            name="glomerular filtration rate",
        ),
        AssignmentRule(
            # [ml/min] * [l/ml] * [-] * [mmole/l]
            "v_HCTZEX",
            "GFR * 0.001 l_per_ml * HCTZEX_f * hctz_ext",
            unit=U.mmole_per_min,
        ),
    ]
)
_m.reactions = [
    Reaction(
        "HCTZEX",
        name="hydrochlorothiazide renal excretion",
        equation="hctz_ext -> hctz_urine",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=("v_HCTZEX", U.mmole_per_min),
    ),
]


model_kidney = _m


if __name__ == "__main__":
    from pkdb_models.models.hctz import MODEL_BASE_PATH

    results: FactoryResult = create_model(
        model=model_kidney,
        filepath=MODEL_BASE_PATH / f"{model_kidney.sid}.xml",
        sbml_level=3,
        sbml_version=2,
        create_antimony=False,
        create_markdown=True,
    )
