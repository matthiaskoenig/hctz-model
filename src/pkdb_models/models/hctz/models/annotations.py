from sbmlutils.metadata import *

model = [
    # taxonomy
    (BQB.HAS_TAXON, "taxonomy/9606"),  # human
    (BQB.HAS_TAXON, "snomedct/337915000"),  # human

    # modelling approach
    (BQB.HAS_PROPERTY, "mamo/MAMO_0000046"),  # ordinary differential equation model

    # biological process explained by model (GO/NCIT)
    (BQB.IS, "NCIT:C29098"),  # hydrochlorothiazide
    (BQB.HAS_PROPERTY, "NCIT:C49184"),  # Loop diuretic
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
    ],
    "anggen": [
        (BQB.IS, "chebi/CHEBI:2720"),
        (BQB.IS, "ncit/C136723"),
        (BQB.IS, "uniprot/Q3UTR7"),
    ],
    "ang1": [
        (BQB.IS, "chebi/CHEBI:147350"),
        (BQB.IS, "ncit/C248"),
    ],
    "ang2": [
        (BQB.IS, "chebi/CHEBI:58506"),
        (BQB.IS, "ncit/C107562"),
    ],
    "ald": [
        (BQB.IS, "chebi/CHEBI:27584"),
        (BQB.IS, "ncit/C219"),
    ],
    "ren": [
        (BQB.IS, "uniprot/P00797"),
        (BQB.IS, "ncit/C113591"),
    ],
}

compartments = {
    # liver
    "li": [
        (BQB.IS, "fma/FMA:7197"),
        (BQB.IS, "bto/BTO:0000759"),
        (BQB.IS, "NCIT:C12392"),
    ],
    "lyso": [
        (BQB.IS, "fma/FMA:63836"),
        (BQB.IS, "NCIT:C13253"),
    ],
    # basolateral membrane
    "basolateral": [
        (BQB.IS, "fma/FMA:84669"),  # Basolateral plasma membrane
        (BQB.IS, "go/GO:0016323"),  # basolateral plasma membrane
    ],
    # apical membrane
    "apical": [
        (BQB.IS, "fma/FMA:84666"),  # Apical plasma membrane
        (BQB.IS, "go/GO:0016324"),  # apical plasma membrane
    ],
    "bi": [
        (BQB.IS, "fma/FMA:62971"),
        (BQB.IS, "NCIT:C13192"),
    ],
    # rest
    # FIXME: rest compartment is not the organism
    "re": [
        (BQB.IS_VERSION_OF, "fma/FMA:62955"),  # anatomical entity
        (BQB.IS_PART_OF, "NCIT:C14250"),  # Organism
    ],
    # gastrointestinal tract
    "gi": [
        (BQB.IS, "fma/FMA:71132"),
        (BQB.IS, "bto/BTO:0000511"),
        (BQB.IS, "NCIT:C34082"),
    ],
    # gut/intestine
    "gu": [
        (BQB.IS, "fma/FMA:45615"),  # gut
        (BQB.IS, "bto/BTO:0000545"),  # gut
        (BQB.IS, "NCIT:C12736"),  # intestine
        (BQB.IS, "fma/FMA:7199"),  # intestine
        (BQB.IS, "bto/BTO:0000648"),  # intestine
    ],
    "gu_lumen": [
        (BQB.IS, "fma/FMA:14586"),  # Lumen of intestine
        (BQB.IS, "uberon/UBERON:0018543"),  # lumen of intestine
    ],
    "duodenum": [
        (BQB.IS, "fma/FMA:7206"),
        (BQB.IS, "uberon/UBERON:0002114"),
    ],
    "jejunum": [
        (BQB.IS, "fma/FMA:7207"),
        (BQB.IS, "uberon/UBERON:0002115"),
    ],
    "ileum": [
        (BQB.IS, "fma/FMA:7208"),
        (BQB.IS, "uberon/UBERON:0002116"),
    ],
    "colon": [
        (BQB.IS, "fma/FMA:14543"),
        (BQB.IS, "uberon/UBERON:000115"),
    ],
    # heart
    "he": [
        (BQB.IS, "NCIT:C12727"),  # heart
        (BQB.IS, "fma/FMA:7088"),  # heart
        (BQB.IS, "bto/BTO:0000562"),  # heart
    ],
    # kidneys
    "ki": [
        (BQB.IS, "fma/FMA:7203"),
        (BQB.IS, "bto/BTO:0000671"),
        (BQB.IS, "NCIT:C12415"),
    ],
    #lung
    "lu": [
        (BQB.IS, "fma/FMA:7195"),
        (BQB.IS, "bto/BTO:0000763"),
        (BQB.IS, "NCIT:C12468"),
    ],
    "ve": [
        (BQB.IS, "bto/BTO:0000131"),  # plasma
        (BQB.IS, "NCIT:C13356"),  # plasma
        (BQB.IS_PART_OF, "fma/FMA:50723"),  # vein
    ],
    'ar': [
        (BQB.IS, "bto/BTO:0000131"),  # plasma
        (BQB.IS, "NCIT:C13356"),  # plasma
        (BQB.IS_PART_OF, "fma/FMA:50720"),  # artery
    ],
    'po': [
        (BQB.IS, "bto/BTO:0000131"),  # plasma
        (BQB.IS, "NCIT:C13356"),  # plasma
        (BQB.IS_PART_OF, "fma/FMA:66645"),  # portal vein
    ],
    # hepatic vein
    "hv": [
        (BQB.IS, "bto/BTO:0000131"),  # plasma
        (BQB.IS, "NCIT:C13356"),  # plasma
        (BQB.IS_PART_OF, "fma/FMA:14337"),  # hepatic vein
    ],
    # rest vein
    "rev": [
        (BQB.IS, "bto/BTO:0000131"),  # plasma
        (BQB.IS, "NCIT:C13356"),  # plasma
        # fixme: be more specific
    ],
    # hepatic vein
    "kiv": [
        (BQB.IS, "bto/BTO:0000131"),  # plasma
        (BQB.IS, "NCIT:C13356"),  # plasma
        # fixme: be more specific
    ],
    "stomach": [
        (BQB.IS, "fma/FMA:7148"),
        (BQB.IS, "NCIT:C12391"),
        (BQB.IS, "uberon/UBERON:0000945"),
        (BQB.IS, "bto/BTO:0001307"),
    ],
    # spleen
    "sp": [
        (BQB.IS, "fma/FMA:7196"),
        (BQB.IS, "NCIT:C12432"),
        (BQB.IS, "uberon/UBERON:0002106"),
        (BQB.IS, "bto/BTO:0001281"),
    ],
    # muscle
    "mu": [
        (BQB.IS, "fma/FMA:30316"),
        (BQB.IS, "bto/BTO:0000511"),
        (BQB.IS, "NCIT:C13056"),
    ],
    "fo": [
        (BQB.IS, "NCIT:C32628"),  # forearm
        (BQB.IS, "fma/FMA:9663"),  # forearm
    ],
    # hepatic vein
    "fov": [
        (BQB.IS, "bto/BTO:0000131"),  # plasma
        (BQB.IS, "NCIT:C13356"),  # plasma
        # fixme: be more specific
    ],
    # pancreas
    "pa": [
        (BQB.IS, "fma/FMA:7198"),
        (BQB.IS, "NCIT:C12393"),
        (BQB.IS, "uberon/UBERON:0001264"),
        (BQB.IS, "bto/BTO:0000988"),
    ],
    "feces": [
        (BQB.IS, "fma/FMA:64183"),
        (BQB.IS, "NCIT:C13234"),
        (BQB.IS, "bto/BTO:0000440"),
    ],
    "plasma": [
        (BQB.IS, "NCIT:C13356"),
        (BQB.IS, "bto/BTO:0000131"),
    ],
    "blood": [
        (BQB.IS, "fma/FMA:62970"),
        (BQB.IS, "NCIT:C12434"),
        (BQB.IS, "bto/BTO:0000089"),
    ],
    "urine": [
        (BQB.IS, "fma/FMA:12274"),
        (BQB.IS, "NCIT:C13283"),
        (BQB.IS, "bto/BTO:0001419"),
    ],
    "parenchyma": [
        (BQB.IS, "fma/FMA:45732"),
        (BQB.IS, "NCIT:C74601"),
        (BQB.IS, "bto/BTO:0001539"),
    ],
    "parietal cell": [
        (BQB.IS, "NCIT:C12594"),
        (BQB.IS, "http://snomed.info/id/57041003"),
    ],
    "gastric acid": [
        (BQB.IS, "fma/FMA:62972"),  # gastric juice
        (BQB.IS, "NCIT:C94192"),
        (BQB.IS, "omit/0006944"),  # gastric acid
    ],
    "plasma membrane": [
        (BQB.IS, "NCIT:C13735"),  # Plasma membrane
        (BQB.IS, "fma/FMA:63841"),  # Plasma membrane
        (BQB.IS, "GO:0005886"),  # plasma membrane
    ],
}