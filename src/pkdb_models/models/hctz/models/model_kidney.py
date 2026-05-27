"""Kidney model for the diuretic Hydrochlorothiazide."""
import numpy as np
from sbmlutils.converters import odefac
from sbmlutils.cytoscape import visualize_sbml
from sbmlutils.factory import *
from sbmlutils.metadata import *

from pkdb_models.models.hctz.models import templates
from pkdb_models.models.hctz.models import annotations


class U(templates.U):
    """UnitDefinitions"""

    ml = UnitDefinition("ml", "ml")
    per_hr = UnitDefinition("per_hr", "1/hr")
    per_ml = UnitDefinition("per_ml", "1/ml")
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
    annotations=annotations.model + [
        # tissue
        (BQB.OCCURS_IN, "fma/FMA:7203"),  # kidney
        (BQB.OCCURS_IN, "bto/BTO:0000671"),  # kidney
        (BQB.OCCURS_IN, "NCIT:C12415"),  # kidney

        (BQB.HAS_PROPERTY, "NCIT:C79372"),  # Pharmacokinetics: Excretion
        (BQB.HAS_PROPERTY, "NCIT:C79371"),  # Pharmacokinetics: Metabolism
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
        sboTerm=SBO.KINETIC_CONSTANT,
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
        name=f"glomerular filtration rate (base)",
        port=True,
    ),

    Parameter(
        "urine_volume",
        1.0,
        U.ml,
        name="urine volume",
        sboTerm=SBO.KINETIC_CONSTANT,
    ),
]
_m.parameters.extend([
    Parameter(
        "HCTZEX_k",
        0.0037108904792554284,
        U.per_ml,
        name="rate urinary excretion of hydrochlorothiazide",
        sboTerm=SBO.KINETIC_CONSTANT,
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
_m.rules.extend([
    AssignmentRule(
        variable="GFR",
        value="f_renal_function * GFR_base",
        unit=U.ml_per_min,
        name="glomerular filtration rate",
    ),
    AssignmentRule(
        # [ml/min] * [l] * [mmole_per_l_ml]
        # "v_HCTZEX", "GFR * Vki * HCTZEX_Vmax * hctz_ext/(hctz_ext + HCTZEX_Km)", unit=U.mmole_per_min
        "v_HCTZEX", "GFR * Vki * HCTZEX_k * hctz_ext", unit=U.mmole_per_min    # [ml/min * mmole/l * l]
    )
])
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
    )
    # create differential equations
    md_path = MODEL_BASE_PATH / f"{model_kidney.sid}.md"
    ode_factory = odefac.SBML2ODE.from_file(sbml_file=results.sbml_path)
    ode_factory.to_markdown(md_file=md_path)

    visualize_sbml(sbml_path=results.sbml_path)
