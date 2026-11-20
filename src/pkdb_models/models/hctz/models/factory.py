"""HCTZ model factory.

Builds the model of the definition with the PBPK library and writes its files
and the COMBINE archive (`pkpdsim.pbpk.create_archive`): the comp model, the
flattened model which is simulated, the ODEs and the antimony of the flat
model, the license texts and, as an extra model, the fluid model on its own
(the blood pressure experiments). The flat model carries the annotation of the
interactive panels of the model (`panels.py`), so the model and its panels are
rebuilt together and the archive holds the model with its panels.
"""

from pathlib import Path
from typing import Any

from pkpdsim.pbpk import create_archive
from sbmlutils.factory import create_model

from pkdb_models.models.hctz import MODEL_BASE_PATH
from pkdb_models.models.hctz.models.definition import DEFINITION
from pkdb_models.models.hctz.models.model_fluid import model_fluid
from pkdb_models.models.hctz.panels import PANELS


def create_hctz_models(model_output_dir: Path) -> dict[str, dict[str, Any]]:
    """Build the HCTZ model.

    Args:
        model_output_dir: directory of the models, the COMBINE archive and the
            license texts are written into its parent.

    Returns:
        The files of the model with their entries in the COMBINE archive.
    """
    model_output_dir.mkdir(parents=True, exist_ok=True)

    # the fluid model on its own, its inputs at the values of the reference
    # individual (the blood pressure experiments)
    fluid = create_model(
        model=model_fluid,
        filepath=model_output_dir / "hctz_fluid.xml",
        sbml_level=3,
        sbml_version=2,
        create_markdown=False,
        create_antimony=False,
    ).sbml_path

    return create_archive(
        DEFINITION,
        model_output_dir,
        model="hctz",
        copyright="2024-2026 Matthias König",
        readme=MODEL_BASE_PATH.parent / "README.md",
        extra_models=[fluid],
        panels=list(PANELS.values()),
    )


if __name__ == "__main__":
    create_hctz_models(MODEL_BASE_PATH)
