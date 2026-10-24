"""Collect the data of the HCTZ studies from the PK-DB study folders.

The studies are copied from a `pkdb_data` checkout (`PKDB_DATA`, else
`../pkdb_data`, see `pkpdsim.data.studies_dir`) into the data folders of the
model, see `pkpdsim.data.collect_tsv_files`:
all hydrochlorothiazide studies and the studies of the coadministered drugs
which report hydrochlorothiazide.
"""

from pathlib import Path

from pkpdsim.data import collect_tsv_files
from pkpdsim.data import studies_dir as pkdb_studies_dir

from pkdb_models.models.hctz import DATA_PATH_BASE

#: the studies of other substances which report hydrochlorothiazide
COADMINISTRATION_STUDIES: dict[str, str] = {
    "canagliflozin": "Devineni2014",
    "lisinopril": "Koytchev2004",
    "enalapril": "Niopas2004",
    "aliskiren": "Vaidyanathan2006",
}


def collect_hctz_data(studies_dir: Path | None = None) -> None:
    """Copy the data of the HCTZ studies into the data folders of the model.

    Args:
        studies_dir: the `studies` folder of pkdb_data, by default the one of
            the checkout `pkpdsim.data.studies_dir` finds.
    """
    if studies_dir is None:
        studies_dir = pkdb_studies_dir()

    collect_tsv_files(
        source_dir=studies_dir / "hydrochlorothiazide",
        target_dir=DATA_PATH_BASE / "hydrochlorothiazide",
    )
    for substance, study in COADMINISTRATION_STUDIES.items():
        collect_tsv_files(
            source_dir=studies_dir / substance,
            target_dir=DATA_PATH_BASE / substance,
            filter_study=lambda name, study=study: name == study,
        )


if __name__ == "__main__":
    collect_hctz_data()
