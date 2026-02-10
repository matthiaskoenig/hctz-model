"""Model of RAAS blood pressure regulation."""
from dataclasses import dataclass

import numpy as np

from sbmlutils import cytoscape as cyviz
from sbmlutils.converters import odefac
from sbmlutils.factory import *
from sbmlutils.metadata import *

from pkdb_models.models.hctz.models import annotations
from pkdb_models.models.hctz.models import templates


class U(templates.U):
    """UnitDefinitions"""
    mmHg = UnitDefinition("mmHg", "133.32239 N/m^2")


mid = "hctz_raas"
version = 2

_m = Model(
    sid=mid,
    name="Model for RAAS system of blood pressure regulation.",
    notes=f"""
    Model for RAAS system of blood pressure regulation.

    **version** {version}

    ## Changelog
    **version 2**

    - better handling of baselines and scaling

    **version 1**

    - initial model

    """ + templates.terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
    annotations=annotations.model + [
        (BQB.HAS_PROPERTY, "NCIT:C15720"),  # pharmacodynamics
        (BQB.HAS_PROPERTY, "NCIT:C91434"),  # Renin-Angiotensin Pathway
    ]
)

_m.compartments = [
    Compartment(
        "Vplasma",
        value=5.0,
        unit=U.liter,
        name="plasma",
        constant=True,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["plasma"],
        port=True
    ),
]


@dataclass
class Substance:
    sid: str
    name: str
    init: float
    unit: str
    boundary: bool = False
    port: bool = False


# ---------------------------------------------------------------------------------------------------------------------
# Pharmacodynamics
# ---------------------------------------------------------------------------------------------------------------------
ald_ref = 250E-9  # [mM]
ren_ref = 1E-9  # [mM]
anggen_ref = 10E-9  # [mM]
ang1_ref = 10E-9  # [mM]
ang2_ref = 8E-9  # [mM]

substances: list[Substance] = [

    # Mr: 360.444 [g/mole]
    # 100 pg/ml {ramipril/Bussien1985} = 100/360.444*1000 [pmol/l] = 277.4 [pmol/l]
    # 80-90 pg/ml {losartan/Christen1991a} = 221.9 - 249.7 [pmol/l]
    # 80-100 pg/ml {losartan/Ohtawa1993} = 221.9 - 277.4 [pmol/l]
    # 600-800 pg/ml {losartan/Doig1993} FIXME: check unit = 1942.0 - 2219.5 [pmol/l]  #
    Substance("ald", "aldosterone", init=ald_ref, unit="mmole"),

    # Mr: 45057 [g/mole]
    # ~ 50-65 pg/ml {losartan/Azizi1999} = 50-65/45.057 [pmol/l] = 1.11 - 1.44 [pmol/l]
    # ~ 45-75 pg/ml {losartan/Doig1993}
    # 1 ng/mL/h PRA ≈ 7.6 pg/ml (5.5 - 9.7)?
    # ~2 ng/ml/hr {losartan/Goldberg1995} = 15.2 pg/ml = 0.337 [pmol/l]
    # ~2 ng/ml/hr {losartan/Tsuruoka2005} = 0.337 [pmol/l]
    # 1-2 ng/ml/hr {losartan/Ohtawa1993} = 0.169 - 0.337 [pmol/l]
    # 1-2 ng/ml/hr renin activity {losartan/Christen1991a} = 0.169 - 0.337 [pmol/l]
    # 5-6 ng/ml/hr renin activity {losartan/Doig1993} FIXME: check unit = 0.843 - 1.01 [pmol/l]
    Substance("ren", "renin", init=ren_ref, unit="mmole"),

    # Mr: 52670 [g/mole]
    Substance("anggen", "angiotensinogen", init=anggen_ref, unit="mmole", boundary=True),

    # Mr: 1296.5 [g/mole]
    # ~ 11-13 [pg/ml] {losartan/Azizi1999} = 11-13 / 1.2965 [pmol/l] = 8.5 - 10.0 [pmol/l]
    # 10 [pmol/l] {ramipril/Manhem1985}
    Substance("ang1", "angiotensin I", init=ang1_ref, unit="mmole"),

    # Mr: 1046.2 [g/mole]
    # ~ 6-10 [pg/ml] {losartan/Azizi1999} = 6-10 / 1.0462 [pmol/l] = 5.7 - 9.6 [pmol/l]
    # 10 [pmol/l] {ramipril/Manhem1985}
    # 5-6 [fmol/ml] {losartan/Christen1991a} = 5-6 [pmol/l]
    # 4-8 [pg/ml] {losartan/Ohtawa1993} = 4-8 / 1.0462 [pmol/l] = 3.8 - 9.2 [pmol/l]
    Substance("ang2", "angiotensin II", init=ang2_ref, unit="mmole"),
]

for s in substances:
    _m.species.append(
        Species(
            s.sid,
            name=s.name,
            initialConcentration=s.init,
            compartment="Vplasma",
            substanceUnit=U.mmole,
            hasOnlySubstanceUnits=False,
            boundaryCondition=s.boundary,
            sboTerm=SBO.SIMPLE_CHEMICAL,
            annotations=annotations.species[s.sid],
            port=s.port,
        )
    )

    _m.assignments.append(
        # FIXME: better handling of initial concentrations
        InitialAssignment(s.sid, f"{s.sid}_ref", unit=U.mM)
    )

    # changes in variables
    if s.sid in ["ang1", "ang2", "ren", "ald"]:
        # absolute change
        _m.parameters.append(
            Parameter(
                f"{s.sid}_change",
                name=f"{s.name} change",
                value=np.nan,
                unit=U.mM,
                annotations=annotations.species[s.sid],
                constant=False,
                notes=f"Absolute change to baseline {s.name}",
            )
        )
        _m.rules.append(
            AssignmentRule(
                f"{s.sid}_change", f"{s.sid}-{s.sid}_ref", unit=U.mM
            )
        )
        # ratio to baseline
        _m.parameters.append(
            Parameter(
                f"{s.sid}_ratio",
                name=f"{s.name} ratio",
                value=np.nan,
                unit=U.dimensionless,
                annotations=annotations.species[s.sid],
                constant=False,
                notes=f"Ratio relative to baseline {s.name}",
            )
        )
        _m.rules.append(
            AssignmentRule(
                f"{s.sid}_ratio", f"{s.sid}/{s.sid}_ref", unit=U.dimensionless
            )
        )

_m.parameters.extend([
    Parameter(
        "anggen_ref",
        anggen_ref,
        U.mM,
        name="reference concentration of angiotensinogen",
        sboTerm=SBO.KINETIC_CONSTANT,
    ),
    Parameter(
        "ang1_ref",
        ang1_ref,
        U.mM,
        name="reference concentration of angiotensin I",
        sboTerm=SBO.KINETIC_CONSTANT,
    ),
    Parameter(
        "ang2_ref",
        ang2_ref,
        U.mM,
        name="reference concentration of angiotensin II",
        sboTerm=SBO.KINETIC_CONSTANT,
    ),
    Parameter(
        "ren_ref",
        ren_ref,
        U.mM,
        name="reference concentration of renin",
        sboTerm=SBO.KINETIC_CONSTANT,
    ),
    Parameter(
        "ald_ref",
        ald_ref,
        U.mM,
        name="reference concentration of aldosterone",
        sboTerm=SBO.KINETIC_CONSTANT,
    ),
])


_m.reactions = [
    # renin turnover
    Reaction(
        sid="RENSEC",
        name="renin secretion (RENSEC)",
        equation="-> ren",
        compartment="Vplasma",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "RENSEC_k",
                0.1,
                U.mmole_per_min,
                name="rate renin secretion",
                sboTerm=SBO.KINETIC_CONSTANT,
            )
        ],
        formula=("RENSEC_k", U.mmole_per_min)
    ),
    Reaction(
        sid="RENDEG",
        name="renin degradation (RENDEG)",
        equation="ren ->",
        compartment="Vplasma",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        pars=[
            # in steady state: kd = ks/ren0
            Parameter(
                "RENDEG_k",
                f"RENSEC_k/ren_ref",
                U.l_per_min,
                name="rate renin degradation",
                sboTerm=SBO.KINETIC_CONSTANT,
                constant=False,
            )
        ],
        formula=("RENDEG_k * ren", U.mmole_per_min)
    ),

    # aldosterone turnover
    Reaction(
        sid="ALDSEC",
        name="aldosterone secretion (ALDSEC)",
        equation="-> ald",
        compartment="Vplasma",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "ALDSEC_k",
                1.0105027952685962e-06,
                U.mmole_per_min,
                name="rate aldosterone secretion",
                sboTerm=SBO.KINETIC_CONSTANT,
            )
        ],

        formula=("ALDSEC_k", U.mmole_per_min),
    ),
    Reaction(
        sid="ALDDEG",
        name="aldosterone degradation (ALDDEG)",
        equation="ald ->",
        compartment="Vplasma",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        # in steady state: kd = ks/ren0
        pars=[
            Parameter(
                "ALDDEG_k",
                f"ALDSEC_k/ald_ref",
                U.l_per_min,
                name="rate aldosterone degradation",
                sboTerm=SBO.KINETIC_CONSTANT,
                constant=False,
            )
        ],
        formula=("ALDDEG_k * ald", U.mmole_per_min)
    ),

    # anggen -> ang1 -> ang2 ->
    Reaction(
        sid="ANGGEN2ANG1",
        name="angiotensinogen to angiotensin I (renin)",
        equation="anggen -> ang1 [ren]",
        compartment="Vplasma",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        pars=[
            Parameter(
                "ANGGEN2ANG1_k",  # k1
                0.10030014354408065,
                U.l_per_min,
                name="rate angen to ang1 conversion",
                sboTerm=SBO.KINETIC_CONSTANT,
            ),
        ],
        formula=("ANGGEN2ANG1_k * anggen * ren/ren_ref", U.mmole_per_min)
    ),
    Reaction(
        sid="ANG1ANG2",
        name="angiotensin I to angiotensin II (ACE)",
        equation="ang1 -> ang2",
        compartment="Vplasma",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        pars=[
            Parameter(
                "ANG1ANG2_k",  # k2
                "ANGGEN2ANG1_k * anggen_ref/ang1_ref",
                U.l_per_min,
                name="rate ang1 to ang2 conversion",
                sboTerm=SBO.KINETIC_CONSTANT,
                constant=False,
            ),
        ],
        formula=("ANG1ANG2_k * ang1", U.mmole_per_min)
    ),
    Reaction(
        sid="ANG2DEG",
        name="angiotensin II degradation (ANG2DEG)",
        equation="ang2 ->",
        compartment="Vplasma",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        pars=[
            Parameter(
                "ANG2DEG_k",  # k3
                "ANGGEN2ANG1_k * anggen_ref/ang2_ref",
                U.l_per_min,
                name="rate aldosterone degradation",
                sboTerm=SBO.KINETIC_CONSTANT,
                constant=False,
            )
        ],
        formula=("ANG2DEG_k * ang2", U.mmole_per_min)
    ),
]


model_raas = _m



if __name__ == "__main__":
    from pkdb_models.models.hctz import MODEL_BASE_PATH

    results: FactoryResult = create_model(
        model=model_raas,
        filepath=MODEL_BASE_PATH / f"{model_raas.sid}.xml",
        sbml_level=3, sbml_version=2,
        validation_options=ValidationOptions(units_consistency=True)
    )
    # create differential equations
    md_path = MODEL_BASE_PATH / f"{model_raas.sid}.md"
    ode_factory = odefac.SBML2ODE.from_file(sbml_file=results.sbml_path)
    ode_factory.to_markdown(md_file=md_path)

    cyviz.visualize_sbml(results.sbml_path, delete_session=True)
