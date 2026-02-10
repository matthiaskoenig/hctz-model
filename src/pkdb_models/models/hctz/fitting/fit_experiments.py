"""Parameter fit problems for HCTZ."""
from typing import Dict, List
from sbmlutils.log import get_logger
from sbmlutils.console import console
from sbmlsim.fit import FitExperiment, FitMapping
from sbmlsim.fit.helpers import f_fitexp, filter_empty

from pkdb_models.models.hctz import HCTZ_PATH, DATA_PATHS
from pkdb_models.models.hctz.experiments.studies import *
from pkdb_models.models.hctz.experiments.metadata import (
    Health, Tissue, ApplicationForm,
    Dosing, Route, Fasting, Coadministration,
    HCTZMappingMetaData,
)

logger = get_logger(__name__)


f_fitexp_kwargs = dict(
    experiment_classes  = [
        Anderson1961,
        Azumaya1990,
        Barbhaiya1982,
        Barbhaiya1982a,
        Beerman1976,
        Beermann1977a,
        Beermann1979,
        Devineni2014,
        Giudicelli1987,
        Heise2015,
        Howes1991,
        Hsiao2015,
        Hunninghake1986,
        # Januszewicz1959, excluded
        Jeon2012,
        Jordo1979,
        Koytchev2004,
        Niemeyer1983,
        Nilsen1989,
        Niopas2011,
        Patel1984,
        Ripley2000,
        Vaidyanathan2006,
        Weir1998,
        Williams1982,
    ],
    base_path=HCTZ_PATH,
    data_path=DATA_PATHS,
)


def filter_control(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Return control experiments/mappings."""

    metadata: HCTZMappingMetaData = fit_mapping.metadata

    # only PO and IV (no SL, MU, RE)
    if metadata.route not in {Route.PO, Route.IV}:
        return False

    # filter multiple dosing (only single dosing)
    # if metadata.application_protocol == ApplicationProtocol.MULTI:
    #     return False

    # filter health (no renal, cardiac impairment, cirrhosis...)
    # # FIXME: check
    # if metadata.health not in {Health.HEALTHY, Health.HYPERTENSION, Health.RENAL_IMPAIRMENT}:
    #     return False

    # remove not fasted
    if metadata.fasting not in {Fasting.NR, Fasting.FASTED}:
        return False

    # remove coadministration
    if metadata.coadministration not in {Coadministration.NONE}:
        return False

    # remove outliers
    if metadata.outlier is True:
        return False

    return True

def filter_hctz(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Only HCTZ PK data."""
    yid = "__".join(fit_mapping.observable.y.sid.split("__")[1:])
    if yid not in {"Afeces_hctz", "Aurine_hctz", "Cve_hctz", "KI__HCTZEX"}:
        return False
    return True

def filter_pd(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Only dap data."""
    yid = "__".join(fit_mapping.observable.y.sid.split("__")[1:])
    if yid in {"Afeces_hctz", "Aurine_hctz", "Cve_hctz", "KI__HCTZEX"}:
        return False
    return True


# --- Experiment classes ---
def f_fitexp_all():
    """All data."""
    return f_fitexp(metadata_filters=filter_empty, **f_fitexp_kwargs)

def f_fitexp_control() -> Dict[str, List[FitExperiment]]:
    """Control data."""
    return f_fitexp(metadata_filters=[filter_control], **f_fitexp_kwargs)

def f_fitexp_pk() -> Dict[str, List[FitExperiment]]:
    """HCTZ pharmacokinetics data."""
    return f_fitexp(metadata_filters=[filter_control, filter_hctz], **f_fitexp_kwargs)

def f_fitexp_pd() -> Dict[str, List[FitExperiment]]:
    """HCTZ pharmacodynamics data."""
    return f_fitexp(metadata_filters=[filter_control, filter_pd], **f_fitexp_kwargs)


if __name__ == "__main__":
    """Test construction of FitExperiments."""

    for f in [
        f_fitexp_all,
        # f_fitexp_control,
        f_fitexp_pk,
        f_fitexp_pd,
    ]:
        console.rule(style="white")
        console.print(f"{f.__name__}")
        fitexp = f()

