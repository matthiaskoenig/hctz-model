from pathlib import Path

HCTZ_PATH = Path(__file__).parent

RESULTS_PATH = HCTZ_PATH / "results"
RESULTS_PATH_SIMULATION = RESULTS_PATH / "simulation"
RESULTS_PATH_FIT = RESULTS_PATH / "fit"

MODEL_BASE_PATH = HCTZ_PATH / "models" / "results" / "models"
MODEL_PATH = MODEL_BASE_PATH / "hctz_body_flat.xml"

# DATA_PATH_BASE = HCTZ_PATH.parents[3] / "pkdb_data" / "studies"
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
    DATA_PATH_CANAGLIFLOZIN
]
