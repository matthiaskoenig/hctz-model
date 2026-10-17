"""HCTZ: PBPK/PD model of hydrochlorothiazide.

The paths of the model and its model object `MODEL`, which the commands
`run_simulation`, `run_fit`, `run_report` and `run_identifiability` of pkpdsim
run by its package `pkdb_models.models.hctz`.
"""

from pathlib import Path

from pkpdsim.model import CheckSettings, FigureSettings, PKPDModel, SimulatorSettings
from pkpdsim.release.settings import Author, ReleaseSettings

HCTZ_PATH = Path(__file__).parent

MODEL_BASE_PATH = HCTZ_PATH / "models" / "output" / "models"
MODEL_PATH = MODEL_BASE_PATH / "hctz_body_flat.xml"

# the subset of the PK-DB studies the model uses, see `data/collect_data.py`
DATA_PATH_BASE = HCTZ_PATH / "data"

DATA_PATH_HCTZ = DATA_PATH_BASE / "hydrochlorothiazide"
DATA_PATH_ENALAPRIL = DATA_PATH_BASE / "enalapril"
DATA_PATH_LISINOPRIL = DATA_PATH_BASE / "lisinopril"
DATA_PATH_ALISKIREN = DATA_PATH_BASE / "aliskiren"
DATA_PATH_CANAGLIFLOZIN = DATA_PATH_BASE / "canagliflozin"

DATA_PATHS = [
    DATA_PATH_HCTZ,
    DATA_PATH_LISINOPRIL,
    DATA_PATH_ENALAPRIL,
    DATA_PATH_ALISKIREN,
    DATA_PATH_CANAGLIFLOZIN,
]

MODEL = PKPDModel(
    name="hctz",
    package=__name__,
    title="HCTZ PBPK/PD model",
    path=HCTZ_PATH,
    model_path=MODEL_PATH,
    data_paths=tuple(DATA_PATHS),
    archive_path=MODEL_BASE_PATH.parent / "hctz_model.omex",
    factory=".models.factory:create_hctz_models",
    experiments=".simulations:EXPERIMENTS",
    fit_definitions=".fitting.fitting:FIT_DEFINITIONS",
    simulator=SimulatorSettings(absolute_tolerance=1e-10, relative_tolerance=1e-10),
    figures=FigureSettings(formats=("svg",), fig_dpi=300, legend_fontsize=10),
    fit_identifiability=True,
    # the adopted fits in `models/output/fits`, whose values and uncertainty the
    # factory takes (`models/fits.py`)
    fits=("PK_20261017_025702__4167a", "PD_20261017_030352__10c1d"),
    # the studies left out of the experiments and of the adopted fits
    checks=CheckSettings(
        not_registered={
            "Dussol2005": "left out of the experiments and the fits",
            "Ernst2006": "left out of the experiments and the fits",
            "Januszewicz1959": "left out of the experiments and the fits",
        },
    ),
    release=ReleaseSettings(
        title=(
            "Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model"
            " of hydrochlorothiazide"
        ),
        repository="matthiaskoenig/hctz-model",
        doi="10.5281/zenodo.15427418",
        authors=(
            Author(
                "Schwaiger, Amanda",
                "0000-0002-8993-8569",
                "Charité University Hospital Berlin, Berlin",
            ),
            Author(
                "König, Matthias",
                "0000-0003-1725-179X",
                (
                    "Humboldt-Universität zu Berlin, Faculty of Life Sciences, Department of Biology, Institute of Theoretical Biology, Systems Medicine of the Liver; University of Stuttgart, Institute of Structural Mechanics and Dynamics in Aerospace Engineering; University of Southern Denmark, Clinical Pharmacology, Pharmacy and Environmental Medicine, Department of Public Health; University Hospital Schleswig-Holstein, Campus Lübeck, First Department of Medicine, Lübeck, Germany"
                ),
            ),
        ),
        keywords=(
            "model",
            "hctz",
            "hydrochlorothiazide",
            "pharmacokinetics",
            "pharmacodynamics",
            "PBPK/PD",
            "physiologically based pharmacokinetic/ pharmacodynamic model",
            "SBML",
        ),
        docker_image="matthiaskoenig/hctz",
        funding=(
            "Matthias König was supported by the Federal Ministry of Research, Technology and Space (BMFTR, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA). This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B)."
        ),
        description=(
            "This repository provides the hydrochlorothiazide (hctz) "
            "physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model."
        ),
        first_year=2024,
    ),
)
"""The HCTZ model: its commands, see `pkpdsim.model`."""

RESULTS_PATH_PETAB = MODEL.results_dir / "petab"
