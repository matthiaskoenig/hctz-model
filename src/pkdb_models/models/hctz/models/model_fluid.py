"""Simple model for the blood pressure regulation based on fluid volums and ions."""
import numpy as np
from sbmlutils.converters import odefac
from sbmlutils.cytoscape import visualize_sbml
from sbmlutils.factory import *
from sbmlutils.metadata import *

from pkdb_models.models.hctz.models import templates
from pkdb_models.models.hctz.models import annotations


class U(templates.U):
    """UnitDefinitions"""

    kg = UnitDefinition("kg")
    ml = UnitDefinition("ml", "ml")
    per_hr = UnitDefinition("per_hr", "1/hr")
    mg_per_min = UnitDefinition("mg_per_min", "mg/min")
    l_per_kg = UnitDefinition("l_per_kg", "l/kg")
    mmHg = UnitDefinition("mmHg", "133.32239 N/m^2")


_m = Model(
    "hctz_fluid",
    name="Model for renal body fluid system for blood pressure regulation.",
    notes="""
    # Model for blood pressure regulation based on extracellular fluid (ECF) volume and ion balance.

    """
    + templates.terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
    annotations=annotations.model + [

    ]
)

_m.parameters.extend([
    Parameter(
        "BW",
        75,
        U.kg,
        name="body weight [kg]",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    # Parameter(
    #     "sex",
    #     0,
    #     U.dimensionless,
    #     name="sex (0=male, 1=female)",
    #     sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    # ),
    Parameter(
        "f_TBW",
        0.55,
        U.l_per_kg,
        name="Total body water (TBW) fraction of bodyweight (male)",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        male: 0.6 l/kg
        female: 0.5 l/kg
        """
    ),
    Parameter(
        "f_ECF",
        0.33,
        U.dimensionless,
        name="ECF fraction of TBW",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""Around 1/3 of total body water (TBW) is extracellular fluid (ECF)."""
    ),
    Parameter(
        "ECF_ref",
        np.nan,
        U.liter,
        constant=False,
        name="Reference extracellular fluid volume (ECF)",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="ECF value is calculated based on body weight and sex."
    ),
    Parameter(
        "Psys_ref",
        120,
        U.mmHg,
        name="Reference systolic blood pressure",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""Psys value is dependent on sex and age.
        
        Young Adult Men (18-39 years): Average=120/80 mmHg
        Middle-aged Men (40-59 years): Average=125−130/80−85 mmHg
        Older Men (60+ years): Average=135−140/85−90 mmHg
        
        Young Adult Women (18-39 years): Average=110−120/70−80mmHg
        Middle-aged Women (40-59 years): Average=120−130/80−85mmHg
        Older Women (60+ years): Average=135−140/85−90mmHg
        """
    ),
    Parameter(
        "Pdia_ref",
        80,
        U.mmHg,
        name="Reference diastolic blood pressure",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""Psys value is dependent on sex and age.
        
        Young Adult Men (18-39 years): Average=120/80 mmHg
        Middle-aged Men (40-59 years): Average=125−130/80−85 mmHg
        Older Men (60+ years): Average=135−140/85−90 mmHg
        
        Young Adult Women (18-39 years): Average=110−120/70−80mmHg
        Middle-aged Women (40-59 years): Average=120−130/80−85mmHg
        Older Women (60+ years): Average=135−140/85−90mmHg
        """
    ),
    Parameter(
        "bp_systolic",
        120,
        U.mmHg,
        constant=False,
        name="Systolic blood pressure",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "bp_diastolic",
        80,
        U.mmHg,
        constant=False,
        name="Diastolic blood pressure",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
])

ECF_ref = 0.55 * 0.33 * 75  # [l] ~14 l
_m.rules.extend([
    AssignmentRule("ECF_ref", "f_ECF * f_TBW * BW", U.liter),
    AssignmentRule(
        "bp_systolic", "Psys_ref * ECF/ECF_ref", U.mmHg,
        notes="""
        Simplified calculation of blood pressure based on change relative to reference ECF volume.
        
        Regulation is more complicated probably via: Increased ECF volume → Increased blood volume → 
        Increased venous return → Increased cardiac output → Increased blood pressure.
        """
    ),
    AssignmentRule(
        "bp_diastolic", "Pdia_ref * ECF/ECF_ref", U.mmHg,
        notes="""
        Simplified calculation of blood pressure based on change relative to reference ECF volume.
    
        Regulation is more complicated probably via: Increased ECF volume → Increased blood volume → 
        Increased venous return → Increased cardiac output → Increased blood pressure.
        """
    ),
])


_m.compartments.extend([
    Compartment(
        "ECF",
        ECF_ref,
        name="extracellular fluid (ECF)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
        annotations=annotations.compartments["plasma"],
    ),
    Compartment(
        "Vurine",
        1E-12,
        name="urine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
        annotations=annotations.compartments["urine"],
    ),
    Compartment(
        "Vki",
        value=np.nan,
        unit=U.liter,
        name="kidney",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["ki"],
    ),
])

# 2 g/day ; 1440 min/day; 1000 mmole/mole; 2/1440/58.44*1000
vin_nacl = 0.023766  # [mmole/min] Sodium chloride uptake
# 2.3 l/day = 2.3/1440 l/min
vin_h2o = 2.3/1440  # [l/min]
na_init = 140.0  # [mM] = [mEq/l]
cl_init = 102.0  # [mM] = [mEq/l]

_m.species.extend([

    Species(
        "hctz",
        name="hydrochlorothiazide",
        initialConcentration=0,
        compartment="ECF",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        boundaryCondition=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["hctz"],
        port=True,
        notes="""This should be the concentration in the kidney, but no kidney compartment in the fluid model."""
    ),
    Species(
        "na",
        initialConcentration=na_init,
        name="Sodium (Na+) (ECF)",
        compartment="ECF",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        # annotations=annotations.species["na"],
        notes="""Concentration in mM corresponding to mEq/l."""
    ),
    Species(
        "na_urine",
        initialAmount=0.0,
        name="Sodium (Na+) (urine)",
        compartment="Vurine",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        # annotations=annotations.species["na"],
        notes="""Concentration in mM corresponding to mEq/l."""
    ),
    Species(
        "cl",
        initialConcentration=cl_init,
        name="Chloride (Cl-) (ECF)",
        compartment="ECF",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        # annotations=annotations.species["cl"],
        notes="""Concentration in mM corresponding to mEq/l."""
    ),
    Species(
        "cl_urine",
        initialAmount=0.0,
        name="Chloride (Cl-) (urine)",
        compartment="Vurine",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        # annotations=annotations.species["cl"],
        notes="""Concentration in mM corresponding to mEq/l."""
    ),
])

_m.parameters.extend([
    Parameter(
        "Mr_nacl",
        58.44,
        U.g_per_mole,
        name="Molecular weight sodium chloride",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "Mr_na",
        22.99,
        U.g_per_mole,
        name="Molecular weight sodium",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "Mr_cl",
        35.45,
        U.g_per_mole,
        name="Molecular weight chloride",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "vin_nacl",
        vin_nacl,
        U.mmole_per_min,
        constant=True,
        name="NaCl uptake via food",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "vin_h2o",
        vin_h2o,
        U.l_per_min,
        constant=True,
        name="H2O uptake via food",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),

    # FIXME: how are these rates connected? ions take water?
    Parameter(
        "k_na", np.nan, U.l_per_min,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        constant=False,
        notes="""Excretion rate sodium urine."""
    ),
    Parameter(
        "k_cl", np.nan, U.l_per_min,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        constant=False,
        notes="""Excretion rate chloride urine."""
    ),
    Parameter(
        "k_h2o", vin_h2o / ECF_ref, U.per_min,
        constant=True,
        notes="""Excretion rate water urine."""
    ),
    Parameter(
        "diuresis", NaN, U.l_per_min,
        constant=False,
        notes="""Excretion rate water urine."""
    ),
    Parameter(
        "E50_hctz_na", 0.1E-3, U.mM,
        notes="""E50 for HCTZ effect on sodium excretion rate."""
    ),
    Parameter(
        "E50_hctz_cl", 0.1E-3, U.mM,
        notes="""E50 for HCTZ effect on chloride excretion rate."""
    ),
    Parameter(
        "E50_hctz_h2o", 0.1E-3, U.mM,
        notes="""E50 for HCTZ effect on diuresis."""
    ),
    Parameter(
        "na_ref", na_init, U.mM,
        constant=True,
        notes="""reference sodium concentration."""
    ),
    Parameter(
        "cl_ref", cl_init, U.mM,
        constant=True,
        notes="""reference chloride concentration."""
    )
])

_m.assignments.extend([
    InitialAssignment("na", "na_ref", unit=U.mM),
    InitialAssignment("cl", "cl_ref", unit=U.mM),
])

_m.rules.extend([
    AssignmentRule("k_na", "vin_nacl/na_ref", unit=U.l_per_min),
    AssignmentRule("k_cl", "vin_nacl/cl_ref", unit=U.l_per_min),

    AssignmentRule("vin_na", "NACL_UPTAKE * Mr_nacl", unit=U.mg_per_min,
                   notes="""Uptake sodium."""),
    AssignmentRule("vin_cl", "NACL_UPTAKE * Mr_nacl", unit=U.mg_per_min,
                   notes="""Uptake chloride."""),

    # calculated observables
    AssignmentRule("vout_na", "NA_EXCRETION * Mr_na ", unit=U.mg_per_min,
                   notes="""Excretion sodium."""),
    AssignmentRule("vout_cl", "CL_EXCRETION * Mr_cl", unit=U.mg_per_min,
                   notes="""Excretion chloride."""),

    AssignmentRule("diuresis", "k_h2o * ECF * (1 dimensionless + hctz/E50_hctz_h2o)", unit=U.l_per_min,
                   notes="""Excretion rate water urine."""),
])

_m.reactions.extend([
    Reaction(
        sid="NACL_UPTAKE",
        name=f"Na/Cl uptake via food",
        compartment="ECF",
        equation=f" -> na + cl",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=("vin_nacl", U.mmole_per_min),
    ),
    Reaction(
        sid="NA_EXCRETION",
        name=f"Na excretion urine",
        compartment="Vki",
        equation=f"na -> na_urine [hctz]",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=("k_na * na * (1 dimensionless + hctz/E50_hctz_na)", U.mmole_per_min),
    ),
    Reaction(
        sid="CL_EXCRETION",
        name=f"Cl excretion urine",
        compartment="Vki",
        equation=f"cl -> cl_urine [hctz]",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=("k_cl * cl * (1 dimensionless + hctz/E50_hctz_cl)", U.mmole_per_min),
    ),
])

_m.rate_rules.extend([
    RateRule("ECF", "vin_h2o - diuresis",
             notes="""Rate rule for calculation of water change ECF."""),
    RateRule("Vurine", "diuresis",
            notes="""Rate rule for calculation of water change urine."""),
])

_m.events.append(
    Event("event_time_0", trigger="time>=0", assignments={
        "ECF": "ECF_ref",
    }
))


model_fluid = _m


if __name__ == "__main__":
    from pkdb_models.models.hctz import MODEL_BASE_PATH

    results: FactoryResult = create_model(
        model=model_fluid,
        filepath=MODEL_BASE_PATH / f"{model_fluid.sid}.xml",
        sbml_level=3,
        sbml_version=2,
    )

    # create differential equations
    md_path = MODEL_BASE_PATH / f"{model_fluid.sid}.md"
    ode_factory = odefac.SBML2ODE.from_file(sbml_file=results.sbml_path)
    ode_factory.to_markdown(md_file=md_path)

    # visualization
    visualize_sbml(sbml_path=results.sbml_path, delete_session=True)
