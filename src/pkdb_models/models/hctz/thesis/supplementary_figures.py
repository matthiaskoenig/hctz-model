from collections import defaultdict
from pathlib import Path

import typst
from sbmlutils.console import console


def create_supplement_typ(path_typ: Path, figures_dir: Path, format: str="svg") -> None:
    """Create typst document from folder with figures."""

    # get all the sorted figures in dictionary
    figure_paths = sorted([f for f in figures_dir.glob(f"**/*.{format}")])
    study_figures: dict[str, list] = defaultdict(list)
    for f in figure_paths:
        tokens = f.name.split("_")
        if len(tokens) < 2:
            continue
        study_id = tokens[0]
        study_figures[study_id].append(f)

    # console.print(study_figures)

    # create text
    text_parts: list[str] = []
    for study_id, paths in study_figures.items():
        text_parts.append(f"#heading(level: 2, outlined: false)[{study_id}]\n")
        for f in paths:
            figure_name = f.name
            part = f"""#figure(
    image("_figures/{figure_name}", width:50%),
    caption: [Simulation {study_id}. Data from @{study_id}.]
)
"""
            text_parts.append(part)

    # serialize
    with path_typ.open("w", encoding="utf-8") as f:
        f.write("".join(text_parts))


if __name__ == "__main__":
    from pkdb_models.models.hctz import RESULTS_PATH_SIMULATION
    selected: str = "studies"
    figures_dir = RESULTS_PATH_SIMULATION / selected / "_figures"

    path_typ = RESULTS_PATH_SIMULATION / selected / "supplement.typ"
    path_pdf = RESULTS_PATH_SIMULATION / selected / "supplement.pdf"
    create_supplement_typ(path_typ=path_typ, figures_dir=figures_dir)

    # compilation to pdf
    typst.compile(input=str(path_typ), output=str(path_pdf))
