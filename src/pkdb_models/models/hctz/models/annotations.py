"""Annotations of the HCTZ models: the model, its compartments and species."""

from pkpdsim.annotations import compartments as shared_compartments
from sbmlutils.metadata import BQB, PBPKO

model = [
    # taxonomy
    (BQB.HAS_TAXON, "taxonomy/9606"),  # human
    (BQB.HAS_TAXON, "snomedct/337915000"),  # human
    # modelling approach
    (BQB.HAS_PROPERTY, "mamo/MAMO_0000046"),  # ordinary differential equation model
    (
        BQB.IS,
        PBPKO.PHYSIOLOGICALLY_BASED_PHARMACOKINETIC_MODEL,
    ),  # physiologically based pharmacokinetic model
    # biological process explained by model (GO/NCIT)
    (BQB.IS, "NCIT:C29098"),  # hydrochlorothiazide
    (BQB.HAS_PROPERTY, "NCIT:C49185"),  # thiazide diuretic
    (BQB.HAS_PROPERTY, "NCIT:C15299"),  # pharmacokinetics
    # model relevance to a particular area
    (BQB.HAS_PROPERTY, "NCIT:C3117"),  # Hypertension
    # model reference
    (BQB.IS_DESCRIBED_BY, "doi/10.5281/zenodo.15427418"),
    # model
    # (BQM.IS, "biomodels.db/MODEL2510140001"),
]

species = {
    "hctz": [
        # hydrochlorothiazide
        (BQB.IS, "NCIT:C29098"),
        (BQB.IS, "CHEBI:5778"),
        (BQB.IS, "pubchem.compound/3639"),
        (BQB.IS, "inchikey/JZUFKLXOESDKRF-UHFFFAOYSA-N"),
        (BQB.IS, "SNOMEDCT:387525002"),
        (BQB.IS, PBPKO.MOLECULE),
    ],
    "na": [
        (BQB.IS, "CHEBI:29101"),
        (BQB.IS, PBPKO.MOLECULE),
    ],
    "cl": [
        (BQB.IS, "CHEBI:17996"),
        (BQB.IS, PBPKO.MOLECULE),
    ],
}


# the shared compartments, the liver and the bile with the terms of the PBPK
# ontology, the extracellular fluid and the renal tubule
compartments: dict[str, list] = {
    **shared_compartments,
    "li": [*shared_compartments["li"], (BQB.IS, PBPKO.LIVER_COMPARTMENT)],
    "bi": [*shared_compartments["bi"], (BQB.IS, PBPKO.BILE_COMPARTMENT)],
    # the extracellular fluid, the plasma and the interstitial fluid
    "ecf": [
        (BQB.IS, "mesh/D045604"),  # extracellular fluid
        (BQB.IS, "snomedct/55450009"),  # extracellular fluid
        (BQB.HAS_PART, "ncit/C13356"),  # plasma
        (BQB.HAS_PART, "uberon/UBERON:0000913"),  # interstitial fluid
    ],
    # the fluid of the renal tubule, lumped from the glomerulus to the urine:
    # the reabsorption of the filtrate and the excretion of sodium and
    # chloride on which HCTZ acts in the distal convoluted tubule
    "tubule": [
        (BQB.IS, "uberon/UBERON:0009773"),  # renal tubule
        (BQB.IS, "fma/FMA:15627"),  # renal tubule
        (BQB.IS, "ncit/C49274"),  # renal tubule
        (BQB.IS, "bto/BTO:0000343"),  # renal tubule
        (BQB.HAS_PART, "uberon/UBERON:0001292"),  # distal convoluted tubule
        (BQB.HAS_PART, "fma/FMA:17721"),  # distal convoluted tubule
        (BQB.HAS_PART, "ncit/C32469"),  # distal convoluted tubule
    ],
}
