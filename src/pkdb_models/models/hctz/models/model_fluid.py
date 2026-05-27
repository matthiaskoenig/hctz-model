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
    ml_per_min = UnitDefinition("ml_per_min", "ml/min")
    mmole_per_l_ml = UnitDefinition("mmole_per_l_ml", "mmole/l/ml")
    l_per_ml = UnitDefinition("l_per_ml", "l/ml")


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
        name="body weight",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        port=True,
    ),
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
        NaN,
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
        NaN,
        name="extracellular fluid (ECF)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
        annotations=annotations.compartments["plasma"],
    ),
    Compartment(
        "Vloop",
        0.5,
        name="loop of Henle",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
        annotations=annotations.compartments["loop"],
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
        value=NaN,
        unit=U.liter,
        name="kidney",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["ki"],
    ),
])

# 2 g/day ; 1440 min/day; 1000 mmole/mole; 2/1440/58.44*1000
# vin_nacl = 0.09218491502645276  # [mmole/min] Sodium chloride uptake
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
        annotations=annotations.species["na"],
        notes="""Concentration in mM corresponding to mEq/l."""
    ),
    Species(
        "na_loop",
        initialConcentration=na_init,
        name="Sodium (Na+) (Loop of Henle)",
        compartment="Vloop",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["na"],
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
        annotations=annotations.species["na"],
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
        annotations=annotations.species["cl"],
        notes="""Concentration in mM corresponding to mEq/l."""
    ),
    Species(
        "cl_loop",
        initialConcentration=cl_init,
        name="Chloride (Cl-) (Loop of Henle)",
        compartment="Vloop",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["cl"],
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
        annotations=annotations.species["cl"],
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
    # Parameter(
    #     "vin_nacl_ref",
    #     vin_nacl,
    #     U.mmole_per_min,
    #     constant=True,
    #     name="reference NaCl uptake via food",
    #     sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    # ),
    Parameter(
        "vin_na",
        NaN,
        U.mmole_per_min,
        constant=True,
        name="Na uptake via food",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "vin_cl",
        NaN,
        U.mmole_per_min,
        constant=True,
        name="Cl uptake via food",
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
    Parameter(
        "k_na", 0.0006459968399240859, U.l_per_min,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        constant=True,
        notes="""Excretion rate sodium urine."""
    ),
    Parameter(
        "k_cl", 0.003002476234054992, U.l_per_min,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        constant=True,
        notes="""Excretion rate chloride urine."""
    ),
    Parameter(
        "k_h2o", NaN, U.l_per_ml,
        constant=False,
        notes="""Excretion rate water urine."""
    ),
    Parameter(
        "h2o_reabsorption",
        NaN,
        U.l_per_min,
        constant=False,
        name="H2O reabsorption from loop of Henle",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "diuresis", NaN, U.l_per_min,
        constant=False,
        notes="""Excretion rate water urine."""
    ),
    Parameter(
        "counter_gamma", 5, U.dimensionless,
        constant=True,
        notes="""Counter-regulation feedback."""
    ),
    Parameter(
        "E50_hctz_nacl", 0.00015768610209207848, U.mM,
        notes="""E50 for HCTZ effect on sodium and chloride excretion."""
    ),
    Parameter(
        "gamma_hctz_nacl", 3.139520154586461, U.dimensionless,
        notes="""gamma for HCTZ effect on sodium and chloride excretion."""
    ),
    Parameter(
        "Emax_hctz_na", 1.8546129025527704, U.dimensionless,
        notes="""Emax for HCTZ effect on sodium excretion."""
    ),
    Parameter(
        "Emax_hctz_cl", 1.0072984331883104, U.dimensionless,
        notes="""Emax for HCTZ effect on chloride excretion."""
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
    # InitialAssignment("vin_nacl", "vin_nacl_ref", U.mmole_per_min),
    InitialAssignment("ECF", "ECF_ref", U.liter),
    InitialAssignment("Vloop", "0.05 dimensionless * ECF_ref", U.liter),
    InitialAssignment("na", "na_ref", unit=U.mM),
    InitialAssignment("cl", "cl_ref", unit=U.mM),
    InitialAssignment("k_h2o", "vin_h2o / GFR_base", unit=U.l_per_ml),

])

_m.rules.extend([
    AssignmentRule("vin_na", "k_na * na_ref", unit=U.l_per_min),
    AssignmentRule("vin_cl", "k_cl * cl_ref", unit=U.l_per_min),
    AssignmentRule(
        variable="GFR",
        value="f_renal_function * GFR_base",
        unit=U.ml_per_min,
        name="glomerular filtration rate",
    ),
    # AssignmentRule("k_na", "vin_nacl/na_ref", unit=U.l_per_min),
    # AssignmentRule("k_cl", "vin_nacl/cl_ref", unit=U.l_per_min),
    # AssignmentRule("k_h2o", "vin_h2o / GFR_base", unit=U.l_per_ml),

    # AssignmentRule("vin_na", "NA_UPTAKE * Mr_nacl", unit=U.mg_per_min,
    #                notes="""Uptake sodium."""),
    # AssignmentRule("vin_cl", "CL_UPTAKE * Mr_nacl", unit=U.mg_per_min,
    #                notes="""Uptake chloride."""),

    # calculated observables
    AssignmentRule("vout_na", "NA_EXCRETION * Mr_na ", unit=U.mg_per_min,
                   notes="""Excretion sodium."""),
    AssignmentRule("vout_cl", "CL_EXCRETION * Mr_cl", unit=U.mg_per_min,
                   notes="""Excretion chloride."""),
])

_m.reactions.extend([

    Reaction(
        sid="NA_UPTAKE",
        name=f"Na uptake via food",
        compartment="ECF",
        equation=f" -> na",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=("vin_na * power(na_ref, counter_gamma)/power(na, counter_gamma)", U.mmole_per_min),
        notes="""Na uptake increased when concentrations too low."""
    ),
    Reaction(
        sid="CL_UPTAKE",
        name=f"Cl uptake via food",
        compartment="ECF",
        equation=f" -> cl",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=(
            "vin_cl * power(cl_ref, counter_gamma)/power(cl, counter_gamma)", U.mmole_per_min),
        notes="""Cl uptake increased when concentrations too low."""
    ),

    Reaction(
        sid="NA_FILTRATION",
        name=f"Na filtration kidney",
        compartment="Vki",
        equation=f"na -> na_loop",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=("GFR * 0.001 l_per_ml * na", U.mmole_per_min),
    ),
    Reaction(
        sid="NA_EXCRETION",
        name=f"Na excretion urine",
        compartment="Vki",
        equation=f"na_loop -> na_urine [hctz]",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=("k_na * na_loop * (1 dimensionless + Emax_hctz_na * power(hctz, gamma_hctz_nacl)/(power(hctz, gamma_hctz_nacl) + power(E50_hctz_nacl, gamma_hctz_nacl)))", U.mmole_per_min),
    ),
    Reaction(
        sid="NA_REABSORPTION",
        name=f"Na reabsorption kidney",
        compartment="Vki",
        equation=f"na_loop -> na",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=("h2o_reabsorption * na_loop", U.mmole_per_min),
    ),
    Reaction(
        sid="CL_FILTRATION",
        name=f"Cl filtration kidney",
        compartment="Vki",
        equation=f"cl -> cl_loop",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=("GFR * 0.001 l_per_ml * cl", U.mmole_per_min),
    ),
    Reaction(
        sid="CL_EXCRETION",
        name=f"Cl excretion urine",
        compartment="Vki",
        equation=f"cl_loop -> cl_urine [hctz]",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=("k_cl * cl_loop * (1 dimensionless + Emax_hctz_cl * power(hctz, gamma_hctz_nacl)/(power(hctz, gamma_hctz_nacl) + power(E50_hctz_nacl, gamma_hctz_nacl)))", U.mmole_per_min),
    ),
    Reaction(
        sid="CL_REABSORPTION",
        name=f"Cl reabsorption kidney",
        compartment="Vki",
        equation=f"cl_loop -> cl",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=("h2o_reabsorption * cl_loop", U.mmole_per_min),
    ),
])

# water balance
_m.rules.extend([
    AssignmentRule(
        "H2O_UPTAKE", "vin_h2o * power(ECF_ref, counter_gamma)/power(ECF, counter_gamma)",
        unit=U.l_per_min,
        notes="""Water uptake."""
    ),
    AssignmentRule(
        "diuresis",
        "k_h2o * GFR * power(ECF, counter_gamma)/power(ECF_ref, counter_gamma) * NA_EXCRETION/vin_na", unit=U.l_per_min,
        # FIXME: diuresis depends on Cl- and Na excretion
        # "* (NA_EXCRETION + CL_EXCRETION)/(vin_na + vin_cl)", unit=U.l_per_min,
        # "* (NA_EXCRETION/(k_na * na) + CL_EXCRETION/(k_cl * cl))/2 dimensionless", unit=U.l_per_min,
        notes="""Excretion rate water urine."""
    ),
    AssignmentRule(
        "h2o_reabsorption",
        "GFR * 0.001 l_per_ml - diuresis", unit=U.l_per_min,
        notes="""Reabsoption rate water Loop of Henle."""
    ),
])

_m.rate_rules.extend([
    RateRule("ECF", "H2O_UPTAKE - GFR * 0.001 l_per_ml + h2o_reabsorption",
             notes="""Rate rule for calculation of water change ECF."""),
    RateRule("Vloop", "GFR * 0.001 l_per_ml - diuresis - h2o_reabsorption",
             notes="""Rate rule for calculation of water change urine."""),
    RateRule("Vurine", "diuresis",
            notes="""Rate rule for calculation of water change urine."""),
])


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
