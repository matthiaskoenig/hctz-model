"""The interactive panels of the HCTZ model.

The panels are declared as data, which the factory writes into the SBML of the
model (`pkpdsim.pbpk.create_archive(..., panels=)`, `models/factory.py`), and
the service reads them from the SBML (`Project.panels_of`). The module imports
only `sbmlsim.panel`, no model and no simulator, so the package imports it at
once.

The panels `impairment` (the plasma concentration) and `excretion` (the
cumulative amount in the urine) answer one question: how does the renal function
change the exposure to hydrochlorothiazide after an oral tablet? HCTZ is
eliminated by the kidney alone, so the renal function `f_renal_function` (the
GFR relative to the healthy GFR of the model, 125 ml/min of the reference
individual) is the knob of the impairment. The model has no class of
impairment of its own; its experiments take the classes of renal impairment
from `pkpdsim.impairment` (`RENAL_FUNCTION`, the midpoints of the GFR classes
relative to a healthy 101 ml/min) at the healthy GFR of the model
(`ScaledRenalMap`, `HCTZSimulationExperiment.renal_map`). The knob also offers
the reference (f = 1), which its experiments run the healthy subjects at, and
the creatinine clearances of two patients of the study data. Every choice is
labelled by its class or its patient and the GFR the model runs at, `GFR_base`
of the model times its fraction, e.g. `mild, 69.5 ml/min`;
`tests/models/test_panels.py` recomputes every value. The panels have no
pre-initialization, so they run the reference individual of the model, 73 kg
and a GFR of 125 ml/min, which their subtitles name. A number and its unit in a
label or a subtitle are joined by a no-break space, so a line never breaks
between them.

The study data is the data the fits of the model use, delivered in the unit of
the curve it is drawn under: the plasma concentrations of Barbhaiya1982 (50 mg,
eight healthy subjects) and Niemeyer1983 (50 mg, a patient of a creatinine
clearance of 10 ml/min) under the plasma curve and the cumulative urinary
excretion of Beermann1976 (50 mg, two patients of normal and one of impaired
renal function) under the urine curve. The data is of one dose and one renal
function each and is drawn only while the knobs are at the condition it was
measured under (`PanelData.at`); the scenarios of the page
(`STUDY_CONDITIONS`) set the knobs to the condition of every series. The panel
at the state of a series peaks within 2 % of the simulation of the series in
its own experiment, the plasma within 0.1 % and the urine, which the experiment
collects over 180 hr and the panel over 96 hr, within 1.8 %, which
`tests/models/test_panels.py` checks.
"""

import json
import logging
from collections.abc import Mapping
from pathlib import Path

from sbmlsim.panel import (
    AppPage,
    Choice,
    Knob,
    Panel,
    PanelCurve,
    PanelData,
    PanelSimulation,
    PanelUncertainty,
    Scenario,
)
from sbmlsim.panel_figure import panels_from_figure, restrict_to_model

#: the id of the panel of the plasma concentration over the renal function
IMPAIRMENT = "impairment"
#: the id of the panel of the urinary excretion over the renal function
EXCRETION = "excretion"

#: the no-break space which joins a number and its unit in a label or a
#: subtitle, so that a line never breaks between them
NBSP = "\u00a0"

#: the healthy GFR of the reference individual of the model [ml/min],
#: `GFR_base`, which the renal function is a fraction of
GFR = 125.0
#: the body weight of the reference individual of the model [kg], `BW`
BODYWEIGHT = 73.0

#: the molecular weight of hydrochlorothiazide as the model has it (`Mr_hctz`),
#: with which the mass of a study is the substance the model carries, as the
#: experiments of the model convert it
MR_HCTZ = "1/(297.7 g/mole)"

#: the end of the simulation in the time unit of the model, minutes: four
#: days, the last time of the urinary excretion of the study data
END = 96 * 60.0

#: the end of the time axis of the plasma panel [hr]: two days, the last sample
#: of its study data (Niemeyer1983, 48 hr); the urine panel keeps the four days
#: of its collection, so the peak of the plasma in the first hours is not drawn
#: into the left tenth of an axis of four days
PLASMA_X_MAX = 48.0

#: the renal function the model runs at in the studies of the panel and in the
#: clinical classes, `f_renal_function`, the GFR relative to the healthy GFR of
#: the model, rounded to three digits. `1.0` is the reference individual of the
#: model, which its experiments run the healthy subjects at; the classes are
#: `renal_map` of the experiments (the midpoint of the class of
#: `pkpdsim.impairment.RENAL_FUNCTION` in ml/min over the healthy 125 ml/min of
#: the model); the two creatinine clearances are the ones of the patients of the
#: study data, `renal_function(crcl)` of the experiments. `tests/models/
#: test_panels.py` recomputes every value
REFERENCE = 1.0
NORMAL = 0.808
MILD = 0.556
CRCL_63 = 0.505
MODERATE = 0.26
SEVERE = 0.156
CRCL_10 = 0.08


def renal_choice(name: str, value: float) -> Choice:
    """Get the choice of a renal function, labelled by its name and its GFR.

    Args:
        name: the clinical class or the patient of the renal function.
        value: the renal function, `f_renal_function`.

    Returns:
        The choice, whose label is the name and the GFR the model runs at, to
        three digits, which are the midpoints of the classes.
    """
    return Choice(label=f"{name}, {GFR * value:.3g}{NBSP}ml/min", value=value)


#: the choices of the renal function, from the best to the worst
RENAL_CLASSES: tuple[Choice, ...] = tuple(
    renal_choice(name, value)
    for name, value in (
        ("reference", REFERENCE),
        ("normal", NORMAL),
        ("mild", MILD),
        ("Beermann 1976 II", CRCL_63),
        ("moderate", MODERATE),
        ("severe", SEVERE),
        ("Niemeyer 1983 W", CRCL_10),
    )
)

#: the clearance of a renal function, the value of the knob which the fraction
#: of the model is derived from: a condition of the study data and of a
#: scenario is the clearance the individual was measured at, `f * GFR` in
#: ml/min, rounded like the knob writes it
CLEARANCE: dict[float, float] = {
    fraction: round(fraction * GFR, 3)
    for fraction in (REFERENCE, NORMAL, MILD, CRCL_63, MODERATE, SEVERE, CRCL_10)
}

#: the knob of the renal function, which is the impairment of the panel: the
#: GFR of the individual in ml/min, from anuria to above the healthy GFR of the
#: reference individual, with the classes of the impairment and the two
#: patients of the study data as its stops. It carries no target: the fraction
#: the model takes, `f_renal_function`, is derived from it (`SIMULATION`), so a
#: reader moves a clearance and not a fraction of one. Its grid is every
#: 5 ml/min over the 125 ml/min of the reference individual
RENAL_FUNCTION = Knob(
    id="impairment",
    label="renal function (GFR)",
    unit="ml/min",
    kind="range",
    min=0.0,
    max=150.0,
    steps=31,
    choices=tuple(
        Choice(label=choice.label, value=round(choice.value * GFR, 3))
        for choice in RENAL_CLASSES
    ),
    default=GFR,
)

#: the body weight of the individual, the slider of the app from 40 to 170 kg,
#: starting at the reference individual of the model; its grid is every 5 kg.
#: The dose of a tablet is the same whatever the individual weighs, so the
#: weight is the volume of distribution of the body it is taken into
BODYWEIGHT_KNOB = Knob(
    id="bw",
    label="body weight",
    target="BW",
    unit="kg",
    kind="range",
    min=40.0,
    max=170.0,
    steps=27,
    default=BODYWEIGHT,
)

#: the oral doses of hydrochlorothiazide as a tablet [mg]; the study data of the
#: panel is of 50 mg
DOSE = Knob(
    id="dose",
    label="dose",
    target="PODOSE_hctz",
    unit="mg",
    kind="range",
    min=0.0,
    max=100.0,
    steps=21,
    choices=(
        Choice(label=f"12.5{NBSP}mg", value=12.5),
        Choice(label=f"25{NBSP}mg", value=25.0),
        Choice(label=f"50{NBSP}mg", value=50.0),
        Choice(label=f"100{NBSP}mg", value=100.0),
    ),
    default=50.0,
)

#: the concentration of hydrochlorothiazide in the plasma of an arm vein, the
#: observable of the plasma data of the fits
PLASMA = PanelCurve(id="Carm_hctz", label="plasma", unit="µM", scale="linear")

#: the cumulative amount of hydrochlorothiazide in the urine, the observable of
#: the urinary excretion of the fits: the renal clearance integrated over the
#: time, which is what the renal function changes
URINE = PanelCurve(id="Aurine_hctz", label="urinary amount", unit="µmol")

#: the plasma concentrations of the 50 mg tablet in `ng/ml` in the data and in
#: `µM` as the curve: the mean and the standard deviation of eight healthy
#: subjects who fasted (Barbhaiya1982, Fig1), and the patient W of Niemeyer1983
#: (Fig1), a creatinine clearance of 10 ml/min; both are training data of the PK
#: fit. The patients C and S of Niemeyer1983 are left out: each has a sample
#: which was not quantified and which the table has as a concentration of 0,
#: which the experiment drops and a series of a panel cannot
PLASMA_DATA: tuple[PanelData, ...] = (
    PanelData(
        id="barbhaiya1982_fasted",
        label="Barbhaiya 1982",
        curve="Carm_hctz",
        dataset="Barbhaiya1982_Fig1",
        x="time",
        y="mean",
        yerr="mean_sd",
        sel={"label": "hctz50_fast250"},
        at={"impairment": CLEARANCE[REFERENCE], "dose": 50.0},
        conversion=MR_HCTZ,
    ),
    PanelData(
        id="niemeyer1983_W",
        label="Niemeyer 1983, W",
        curve="Carm_hctz",
        dataset="Niemeyer1983_Fig1",
        x="time",
        y="value",
        sel={"label": "hctz50_W"},
        at={"impairment": CLEARANCE[CRCL_10], "dose": 50.0},
        conversion=MR_HCTZ,
    ),
)

#: the cumulative urinary excretion of the 50 mg capsule of three patients of
#: Beermann1976 (Tab1), in `mg` in the data and in `µmol` as the curve: the
#: patients I and III have a normal renal function, the patient II a serum
#: creatinine of 1.6 mg/dl; the patient III is training data of the PK fit, the
#: patients I and II are validation data
URINE_DATA: tuple[PanelData, ...] = tuple(
    PanelData(
        id=f"beermann1976_{patient}",
        label=f"Beermann 1976, {patient}",
        curve="Aurine_hctz",
        dataset="Beermann1976_Tab1",
        x="time",
        y="value",
        sel={"label": f"amount_urine_hctz50po_{patient}"},
        at={"impairment": CLEARANCE[renal], "dose": 50.0},
        conversion=MR_HCTZ,
    )
    for patient, renal in (("I", REFERENCE), ("II", CRCL_63), ("III", REFERENCE))
)

#: the simulation of both panels, the same oral dose and the same time
#: the band of every curve: the draws of the eleven parameters the fits of the
#: model estimated, which the SBML carries as their distributions, 16 of them
#: by default and 64 at most, which a reader of the page moves. A draw is one
#: run of the model, so the page runs 16 or 64 times the work of its curves and
#: shows the band of the individual it just moved; the sample is the same on
#: every machine (`seed`). It is the uncertainty of the fits and no variability
#: of a population: the knobs stay where the reader put them, every draw is the
#: same individual with the parameters of one draw of the fits
UNCERTAINTY = PanelUncertainty(draws=16, max_draws=64, level=0.9, seed=0)

#: the simulation of every panel: the four days of the app, the time delivered
#: in hours, the fraction of the renal function derived from the clearance the
#: reader sets, and the band of the fits around every curve
SIMULATION = PanelSimulation(
    end=END,
    points=576,
    x_unit="hr",
    derived={"f_renal_function": f"impairment / {GFR}"},
    uncertainty=UNCERTAINTY,
)

#: the reference individual the panels run, which their subtitles name
REFERENCE_INDIVIDUAL = (
    f"the reference individual, {BODYWEIGHT:g}{NBSP}kg and GFR {GFR:g}{NBSP}ml/min"
)

#: the plasma concentration over the renal function and the dose
IMPAIRMENT_PANEL = Panel(
    id=IMPAIRMENT,
    title="Plasma concentration in renal impairment",
    subtitle=(
        "hydrochlorothiazide in an arm vein after a single oral tablet to "
        f"{REFERENCE_INDIVIDUAL}"
    ),
    y_label="plasma conc.",
    x_max=PLASMA_X_MAX,
    knobs=(DOSE, BODYWEIGHT_KNOB, RENAL_FUNCTION),
    curves=(PLASMA,),
    data=PLASMA_DATA,
    simulation=SIMULATION,
)

#: the urinary excretion over the renal function and the dose, a panel of its
#: own since the amount in the urine and the concentration in plasma are of
#: other units and scales, which one axis cannot show
EXCRETION_PANEL = Panel(
    id=EXCRETION,
    title="Urinary excretion in renal impairment",
    subtitle=(
        "the cumulative amount of hydrochlorothiazide in the urine after a "
        f"single oral tablet to {REFERENCE_INDIVIDUAL}"
    ),
    y_label="urinary amount",
    knobs=(DOSE, BODYWEIGHT_KNOB, RENAL_FUNCTION),
    curves=(URINE,),
    data=URINE_DATA,
    simulation=SIMULATION,
)

#: the panels of the model, by their ids
#: the substance as the sidecar of the figure labels the readouts of a place,
#: the prefix of every one of them
SUBSTANCE = "hydrochlorothiazide"

#: the body figure of the model and the readouts of its places, which the
#: factory writes beside the models it builds (`pkpdsim.pbpk.create_archive`,
#: `models/factory.py`) and the package carries: the drawing of the organs,
#: the routes and the processes of the build, and the sidecar
#: (`figurereadouts/1`) which names the timecourses of every place of it
FIGURE_DIR = Path(__file__).parent / "models" / "output" / "models"
FIGURE_SVG = FIGURE_DIR / "hctz_body_body.svg"
FIGURE_READOUTS = FIGURE_DIR / "hctz_body_body.readouts.json"

#: the panels of the figure and the figure of the app: one panel per place of
#: the drawing and per unit, which a click on an organ, a sample site or a
#: process opens (`sbmlsim.panel_figure.panels_from_figure`). They run the
#: simulation of the page, so the dose, the body weight and the renal function
#: of the reader are the ones of the curve, and they carry the band of the
#: fits. The ids are the ones of the sidecar, which pkpdsim writes without
#: compiling the model; `tests/models/test_panels.py` checks every one of them
#: against the compiled model, so that nothing the service would refuse is
#: declared
#: the readouts of the drawing which this build does not carry. The sidecar is
#: written from the definition of the library, which names the places of every
#: PBPK build, and hydrochlorothiazide is given as a tablet and leaves the body
#: through the kidney: the model has no tissue of the large intestine and no
#: faecal route, so the places `la`, `lumen` and `feces` of the drawing select
#: nothing. The ids are declared here because the panels are declared before a
#: model is compiled, and `tests/models/test_panels.py` recomputes them against
#: the compiled model, so a build which gains one of them fails the test
ABSENT_READOUTS: frozenset[str] = frozenset(
    {
        "[LA__Cpl_hctz]",
        "[LA__Cti_hctz]",
        "LA__Cu_ti_hctz",
        "Alumen_hctz",
        "Rfeces_hctz",
    }
)

#: the label of every place of the drawing by its key path, which the sidecar
#: carries beside the readouts of the place
PLACE_LABELS: dict[str, str] = {
    key: str(place.get("label") or "")
    for key, place in json.loads(FIGURE_READOUTS.read_text(encoding="utf-8"))[
        "keys"
    ].items()
}


def _curve_of(key: str, readout: Mapping[str, str]) -> tuple[str, str]:
    """Get the group of a readout of the drawing and the label of its curve.

    The sidecar labels a readout with the substance and the place it is read
    at, `hydrochlorothiazide, adipose tissue tissue`. A panel of the figure is
    one place and its title names both, so the legend carries what is left of
    the label: the compartment, the site or the process (`tissue`,
    `interstitium unbound`, `amount`). A label which names neither the
    substance nor the place, e.g. `plasma (sample)` of the blood sample, is
    kept as it is. The group is the same for every readout of a key, so a key
    is one panel per unit, which is the split of the library.

    Args:
        key: the key path of the place of the drawing.
        readout: the readout of the sidecar, its id, label, unit and kind.

    Returns:
        The group, empty, and the label of the curve.
    """
    label = (readout.get("label") or readout["id"]).removeprefix(f"{SUBSTANCE}, ")
    place = PLACE_LABELS.get(key, "").removeprefix(f"{SUBSTANCE}, ")
    return "", label.removeprefix(f"{place} ") if place else label


_proposed, _figure = panels_from_figure(
    FIGURE_SVG,
    FIGURE_READOUTS,
    simulation=SIMULATION,
    knobs=(DOSE, BODYWEIGHT_KNOB, RENAL_FUNCTION),
    title="Whole-body model",
    group=_curve_of,
)
# the drop is the declaration of `ABSENT_READOUTS` above, so the report of the
# library would repeat what the package states; the logger of the module is
# quiet for the one call
_figure_logger = logging.getLogger("sbmlsim.panel_figure")
_level = _figure_logger.level
_figure_logger.setLevel(logging.ERROR)
try:
    FIGURE_PANELS, FIGURE, DROPPED_READOUTS = restrict_to_model(
        _proposed, _figure, lambda sid: sid not in ABSENT_READOUTS
    )
finally:
    _figure_logger.setLevel(_level)

PANELS: dict[str, Panel] = {
    **{panel.id: panel for panel in (IMPAIRMENT_PANEL, EXCRETION_PANEL)},
    **FIGURE_PANELS,
}

#: the study conditions of the page, the renal function and the dose of the
#: series of the study data, so that a reader reaches every series in one
#: click: the healthy subjects of Barbhaiya1982 and the patients I and III of
#: Beermann1976 at the reference individual, which is where the knobs start,
#: and the two patients of an impaired renal function
STUDY_CONDITIONS: tuple[Scenario, ...] = (
    Scenario(
        id="healthy_50",
        label=f"Barbhaiya 1982, Beermann 1976 I, III, 50{NBSP}mg",
        values={"impairment": CLEARANCE[REFERENCE], "dose": 50.0},
    ),
    Scenario(
        id="beermann1976_II",
        label=f"Beermann 1976 II, 50{NBSP}mg",
        values={"impairment": CLEARANCE[CRCL_63], "dose": 50.0},
    ),
    Scenario(
        id="niemeyer1983_W",
        label=f"Niemeyer 1983 W, 50{NBSP}mg",
        values={"impairment": CLEARANCE[CRCL_10], "dose": 50.0},
    ),
)

#: the pages of the app of the model: the question of the model under its
#: study data, and the body figure, where a reader picks the timecourse of an
#: organ, of a sample site or of a process by clicking the place of the drawing
#: it belongs to
PAGES: tuple[AppPage, ...] = (
    AppPage(
        id="impairment",
        title="Renal impairment",
        panels=(IMPAIRMENT, EXCRETION),
        scenarios=STUDY_CONDITIONS,
    ),
    AppPage(
        id="body",
        title="Whole-body model",
        panels=tuple(FIGURE_PANELS),
        figure=True,
        size="small",
    ),
)
