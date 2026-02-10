from dataclasses import dataclass
from enum import Enum

from sbmlsim.fit.objects import MappingMetaData


class Health(str, Enum):
    HEALTHY = "healthy"
    HYPERTENSION = "hypertension"
    RENAL_IMPAIRMENT = "renal impairment"
    CIRRHOSIS = "cirrhosis"
    CARDIAC_IMPAIRMENT = "cardiac impairment"
    CARDIAC_RENAL_IMPAIRMENT = "cardiac renal impairment"


class Tissue(str, Enum):
    PLASMA = "plasma"
    URINE = "urine"
    FECES = "feces"


class ApplicationForm(str, Enum):
    NR = "not reported"
    TABLET = "tablet"
    CAPSULE = "capsule"
    SOLUTION = "solution"
    SUSPENSION = "suspension"


class Dosing(str, Enum):
    SINGLE = "single dose"
    NR = "not reported"
    MULTI = "multi dose"


class Route(str, Enum):
    PO = "PO"
    IV = "IV"

class Fasting(str, Enum):
    NR = "not reported"
    FASTED = "fasted"
    FED = "fed"


class Coadministration(str, Enum):
    NONE = "none"  # only hctz
    ALISKIREN = "aliskiren"
    CANAGLIFLOZIN = "canagliflozin"
    CAPTOPRIL = "captopril"
    CHOLESTYRAMINE = "cholestyramine"
    CILAZAPRIL = "cilazapril"
    DILTIAZEM = "diltiazem"
    EMPAGLIFLOZIN = "empagliflozin"
    ENALAPRIL = "enalapril"
    FIMASARTAN = "fimasartan"
    INDOMETACIN = "indometacin"
    LISINOPRIL = "lisinopril"
    LCZ696 = "lcz696"

@dataclass
class HCTZMappingMetaData(MappingMetaData):
    tissue: Tissue
    route: Route
    application_form: ApplicationForm
    dosing: Dosing
    health: Health
    fasting: Fasting
    coadministration: Coadministration = Coadministration.NONE
    outlier: bool = False

    def to_dict(self):
        return {
            "tissue": self.tissue.name,
            "route": self.route.name,
            "application_form": self.application_form.name,
            "dosing": self.dosing.name,
            "health": self.health.name,
            "fasting": self.fasting.name,
            "coadministration": self.coadministration.name,
            "outlier": self.outlier,
        }
