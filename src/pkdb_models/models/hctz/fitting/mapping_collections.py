"""Parameter fit problems for HCTZ.

The data of a fit is selected from the fit mappings of the studies in three
steps, see `sbmlsim.fit.helpers`: the filters on the metadata of the mappings
select the training data of the fit and exclude the rest, the outliers are
named once for all mappings and are the training data which is not usable, and
the validation data is the part of the training data a fit is evaluated on but
not fitted to. The metadata of a mapping describes its curve, what a fit does
with the curve is decided here.

The validation data has four parts, each a different question: the
interactions (`INTERACTION_VALIDATION`, the arms with a coadministered drug
which the model has no interaction for), the doses (`DOSE_VALIDATION`, a dose
between the fitted doses of a study), the limitations (`LIMITATION_VALIDATION`,
data of a process the model does not describe) and the subjects
(`validation_individuals`, half of the subjects of every study whose data are
all data of single subjects, with all their data). The arms of an interaction
or a dose come from the subjects of the fitted arms (crossover studies), only
the subjects are validation data independent of the training. The summaries of
data which is fitted one by one are excluded (`AGGREGATE_MAPPINGS`): a mean of
subjects would count the training subjects twice and carry the held-out
subjects into the training, a total of urine collections would count the same
urine twice.
"""

from pkpdsim.fit import (
    mapping_metadata,
    metadata_filter,
    observable_filter,
    observable_id,
)
from pkpdsim.metadata import Coadministration, Fasting, Route
from sbmlsim.console import console
from sbmlsim.experiment import SimulationExperiment
from sbmlsim.fit import FitMapping, FitMappingCollection, MappingKind
from sbmlsim.fit.helpers import FitMappings, MappingFilter

from pkdb_models.models.hctz import DATA_PATHS, HCTZ_PATH
from pkdb_models.models.hctz.experiments.studies import (
    Anderson1961,
    Azumaya1990,
    Barbhaiya1982,
    Barbhaiya1982a,
    Beermann1976,
    Beermann1977a,
    Beermann1979,
    Devineni2014,
    # Dussol2005,
    # Ernst2006,
    Giudicelli1987,
    Heise2015,
    Howes1991,
    Hsiao2015,
    Hunninghake1986,
    # Januszewicz1959,
    Jeon2012,
    Jordo1979,
    Knauf1995,
    Koytchev2004,
    Niemeyer1983,
    Nilsen1989,
    Niopas2004,
    Patel1984,
    Ripley2000,
    Vaidyanathan2006,
    Weir1998,
    Williams1982,
)

#: the keys of fit mappings by study: the keys of the mappings are SIds of their
#: experiment, which two studies can share (e.g. `fm_Fig3_hctz25` of Heise2015
#: and Jeon2012), so a named mapping is named with its study
type NamedMappings = dict[str, set[str]]

# observables of the pharmacokinetics
PK_OBSERVABLES = {"Afeces_hctz", "Aurine_hctz", "Cve_hctz", "KI__HCTZEX"}

EXPERIMENT_CLASSES: list[type[SimulationExperiment]] = [
    Anderson1961,
    Azumaya1990,
    Barbhaiya1982,
    Barbhaiya1982a,
    Beermann1976,
    Beermann1977a,
    Beermann1979,
    Devineni2014,
    # Dussol2005,
    # Ernst2006,
    Giudicelli1987,
    Heise2015,
    Howes1991,
    Hsiao2015,
    Hunninghake1986,
    # Januszewicz1959,
    Jeon2012,
    Jordo1979,
    Knauf1995,
    Koytchev2004,
    Niemeyer1983,
    Nilsen1989,
    Niopas2004,
    Patel1984,
    Ripley2000,
    Vaidyanathan2006,
    Weir1998,
    Williams1982,
]

#: mappings which are not fitted, the data is not usable. Beermann1976 Fig2 was
#: one until its conversion from the radioactivity of 14C-HCTZ was corrected
OUTLIER_MAPPINGS: NamedMappings = {}

#: the validation of the interactions: the coadministration arms of
#: Vaidyanathan2006 (aliskiren), Weir1998 (diltiazem) and Howes1991 (enalapril,
#: as a separate tablet and in a combination tablet). The model has no
#: interaction for these drugs, so the arms are the prediction that none is
#: needed to describe the hydrochlorothiazide pharmacokinetics.
#: `filter_coadministration` lets them through for this reason, every other
#: coadministration stays out of the selection altogether
INTERACTION_VALIDATION: NamedMappings = {
    "Vaidyanathan2006": {"fm_Fig3_hctz_HCTZ25_ALI300HCTZ"},
    "Weir1998": {"fm_Fig2_hctz25_kombi", "fm_Fig3_amount_cumulative_hctz25_kombi"},
    "Howes1991": {
        "fm_Fig1_HCTZ25__ENA10_multi_hydrochlorothiazide",
        "fm_Fig1_HCTZ25_combi_hydrochlorothiazide",
        "fm_Tab2_ENA10__HCTZ25multi_cumulative_amount_hydrochlorothiazide",
        "fm_Tab2_ENA10__HCTZ25combi_cumulative_amount_hydrochlorothiazide",
    },
    # the combination tablets of 12.5 mg with enalapril and lisinopril
    "Niopas2004": {
        "fm_Fig2_hydrochlorothiazide_ENA20",
        "fm_Fig2_hydrochlorothiazide_REF20",
    },
    "Koytchev2004": {"fm_Fig2_test_hydro", "fm_Fig2_reference_hydro"},
}

#: the studies whose patients kept their usual medication, before and during
#: the study: it is a part of their baseline, the change of the study is the
#: change by HCTZ. Dussol2005 (antihypertensives, not washed out) and
#: Niemeyer1983 (the usual therapy of patients with renal failure).
#: `filter_coadministration` lets them through. Beermann1979 is not one of
#: them: ethacrynic acid, a loop diuretic, was given within the collection of
#: the urine
STABLE_COMEDICATION: set[str] = {"Dussol2005", "Niemeyer1983"}

#: the validation of the dose dependency: a dose between the doses of a study
#: which the fit sees
DOSE_VALIDATION: NamedMappings = {
    # the 50 mg tablet arm of Patel1984, in every observable it was measured
    # in. The fit sees the 25 mg and the 100 mg tablets of the same study
    "Patel1984": {
        "fm_50_tab",
        "fm_50_tab_urine",
        "fm_Naurine_50_tab",
        "fm_Clurine_50_tab",
    },
    # the 12.5 mg arm of Jordo1979, the plasma of the group and the
    # cumulative urine of the six subjects (the mean of the subjects is in
    # `AGGREGATE_MAPPINGS`). The fit sees the 25 mg arm of the same study, so
    # the lower dose is a prediction
    "Jordo1979": {
        "fm_Fig1_12p5_hctz",
        *(f"fm_Tab2_{k}_12p5_amount_cumulative" for k in range(1, 7)),
    },
}

#: the validation of the limitations of the model: valid data of a process the
#: model does not describe, which would distort the fitted parameters of the
#: processes it does describe
LIMITATION_VALIDATION: NamedMappings = {
    # the urinary sodium of the last of 30 days of HCTZ in chronic kidney
    # disease (and of the basal state, the same dataset). The model has no
    # sodium balance under chronic HCTZ: only the intake, which rises as the
    # plasma sodium falls, balances the excretion, 318 mmol a day against 68
    # mmol. The mean arterial pressure and the urine volume of the study are
    # fitted
    # "Dussol2005": {"fm_Tab3_amount_na_hctz"},
    # the systolic pressure of the HCTZ period after a period of
    # chlorthalidone and a washout of 4 weeks: its baseline, 4.4 mmHg below
    # the one of the chlorthalidone period, carries an effect of
    # chlorthalidone, which the model does not have. The HCTZ period of the
    # patients who took HCTZ first is fitted
    # "Ernst2006": {"fm_Fig1_sbp_hctz_cltdfirst"},
    # the patients with an impairment: no measured cardiac output or creatinine
    # clearance, cirrhosis has no effect in the model (ascites and edema in all
    # patients of the hepatic group), case 13 has lupus; only the controls
    # (cases 1 to 5) are fitted
    "Anderson1961": {
        f"fm_{key}_HCTZ{route}_{case}"
        for key in ["amount", "cmax"]
        for route, case in [
            *(("po", case) for case in ["6", "7", "8", "9", "12"]),
            *(
                ("iv", case)
                for case in ["8A", "8B", "10", "11", "12", "13A", "13B", "14", "15"]
            ),
        ]
    },
    # the feces after IV (1.0 and 4.3 % of the dose): the model has no
    # non-renal elimination, nothing reaches the feces after IV; a secretion
    # into the feces fitted with them was not identifiable (its profile
    # reaches 0)
    "Beermann1976": {"fm_hctz_iv1_5_feces", "fm_hctz_iv35_4_feces"},
    # the urine volumes of the water load (150 ml every hour): the model
    # excretes a water load only through the expansion of the extracellular
    # fluid. The sodium is fitted
    "Beermann1977a": {
        f"fm_Fig5tc_{dose}_urinvol" for dose in ["0", "12_5", "25", "50", "75"]
    },
    # the single subject of Fig1, a net sodium of about 195 mmol in 0-12 hr
    # against 81 +- 11 mmol of the five healthy subjects of Table 2: the model
    # has no variability between subjects, the subjects of Fig3 are fitted
    "Knauf1995": {"fm_hctz25_Fig1_na_urine_healthy"},
    # the urine of water diuresis (5.6 to 16.3 ml/min before the dose): the
    # model has no water diuresis, its urine flow is 1.0 ml/min. And the
    # sodium and chloride of case 5, on a low-sodium diet: the intake of a
    # study is not a parameter of the model
    # "Januszewicz1959": {
    #     *(f"fm_Tab1_case{case}_urinary_volume_rate" for case in range(1, 11)),
    #     "fm_Tab1_case5_excretion_rate_sodium",
    #     "fm_Tab1_case5_excretion_rate_chloride",
    # },
}

#: the validation data which is named, the subjects come on top, see
#: `validation_individuals`
VALIDATION_MAPPINGS: NamedMappings = {
    study: set().union(
        *(
            mappings.get(study, set())
            for mappings in [
                INTERACTION_VALIDATION,
                DOSE_VALIDATION,
                LIMITATION_VALIDATION,
            ]
        )
    )
    for study in INTERACTION_VALIDATION | DOSE_VALIDATION | LIMITATION_VALIDATION
}

#: the summaries of data which the fits use one by one, excluded from every
#: fit: the means of subjects (the training would see a training subject twice
#: and the held-out subjects through the mean) and the totals of urine
#: collections (the same urine twice)
AGGREGATE_MAPPINGS: NamedMappings = {
    # Tab1A, the urinary recovery of the groups of Tab1
    "Anderson1961": {
        f"fm_amount_HCTZ{route}_{group}"
        for route in ["po", "iv"]
        for group in ["control", "cardiac", "hepatic", "renal"]
    },
    "Beermann1977a": {
        # Tab4, the urinary recovery of the 8 subjects
        *(f"fm_Tab4_amount_HCTZ{dose}_mean" for dose in ["12p5", "25", "50", "75"]),
        # Tab4, the 48 hr recovery of 25 mg of HD and MLL, the sum of their
        # collections of Fig1_2
        "fm_Tab4_amount_HCTZ25_HD",
        "fm_Tab4_amount_HCTZ25_MLL",
    },
    # Tab2, the net sodium and chloride of the five subjects of Fig3 with a
    # creatinine clearance of 100 ml/min and more
    "Knauf1995": {"fm_Tab2_na_net", "fm_Tab2_cl_net"},
    # Tab2, the cumulative urine of the 6 subjects
    "Jordo1979": {
        "fm_Tab2_0_12p5_amount_cumulative",
        "fm_Tab2_0_25_amount_cumulative",
    },
}


def study(fit_mapping: FitMapping) -> str:
    """Get the study of a fit mapping, the id of its experiment."""
    return fit_mapping.reference.experiment.sid


def named(
    mappings: NamedMappings, fit_mapping_key: str, fit_mapping: FitMapping
) -> bool:
    """Check whether a fit mapping is one of the named mappings of its study."""
    return fit_mapping_key in mappings.get(study(fit_mapping), set())


def check_named(mappings: NamedMappings, fit_mappings: FitMappings) -> None:
    """Check that the named mappings are fit mappings of their studies.

    Raises:
        ValueError: for a study which is no experiment, or a key which is no fit
            mapping of its study.
    """
    for sid, keys in mappings.items():
        experiment = fit_mappings.experiments.get(sid)
        if experiment is None:
            raise ValueError(f"'{sid}' is no experiment of the fits.")
        if unknown := sorted(keys - set(experiment._fit_mappings)):
            raise ValueError(f"'{unknown}' are no fit mappings of '{sid}'.")


def filter_aggregates(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """No summaries of data which is fitted one by one, see `AGGREGATE_MAPPINGS`."""
    return not named(AGGREGATE_MAPPINGS, fit_mapping_key, fit_mapping)


def individual(fit_mapping: FitMapping) -> str | None:
    """Get the individual of a fit mapping, `None` for group data.

    The datasets of PK-DB carry the subject in the `individual` column, which
    is empty for the data of a group. A number is the same subject whether the
    table has it as an integer or a float (`20` and `20.0`).
    """
    reference = fit_mapping.reference
    dataset = reference.experiment._datasets.get(reference.dset_id)
    if dataset is None or "individual" not in dataset.columns:
        return None
    individuals = set()
    for value in dataset["individual"].dropna().unique():
        name = str(value)
        try:
            number = float(name)
        except ValueError:
            individuals.add(name)
        else:
            individuals.add(f"{number:g}")
    return individuals.pop() if len(individuals) == 1 else None


def _condition(fit_mapping: FitMapping) -> tuple:
    """Get the condition of a fit mapping: its observable and its metadata."""
    return (
        observable_id(fit_mapping),
        *sorted(mapping_metadata(fit_mapping).to_dict().items()),
    )


def _natural(name: str) -> tuple:
    """Sort key of an individual: numbers by value (`2` before `10`)."""
    try:
        return (0, float(name), "")
    except ValueError:
        return (1, 0.0, name)


def validation_individuals(fit_mappings: FitMappings) -> NamedMappings:
    """Get the mappings of the held-out subjects.

    A subject is held out with all its data, so that no subject is in the
    training and in the validation. Only a study whose data are all data of
    single subjects (the excluded summaries of `AGGREGATE_MAPPINGS` aside) holds
    out subjects: the data of a group, e.g. the plasma of Jordo1979 or the
    urine volume of Beermann1977a, contains every subject of the study, so
    none of them is independent of its training. In such a study the subjects
    are taken in their order (numbers by value, names alphabetically), and a
    subject is held out if every condition it was measured in (observable and
    metadata of a curve) keeps a subject in the training, until half of the
    subjects are held out. A condition with one subject therefore stays
    training data.

    Args:
        fit_mappings: the complete list of the fit mappings.

    Returns:
        The keys of the validation mappings by study.
    """
    keys: NamedMappings = {}
    for sid, experiment in fit_mappings.experiments.items():
        # the keys and the conditions of every subject
        mappings: dict[str, list[str]] = {}
        conditions: dict[str, set[tuple]] = {}
        groups = False
        for key, fit_mapping in experiment._fit_mappings.items():
            if named(AGGREGATE_MAPPINGS, key, fit_mapping):
                continue
            name = individual(fit_mapping)
            if name is None:
                groups = True
                break
            mappings.setdefault(name, []).append(key)
            conditions.setdefault(name, set()).add(_condition(fit_mapping))
        if groups:
            continue
        # the subjects in the training per condition
        training: dict[tuple, int] = {}
        for subject_conditions in conditions.values():
            for condition in subject_conditions:
                training[condition] = training.get(condition, 0) + 1
        held_out: list[str] = []
        for name in sorted(mappings, key=_natural):
            if len(held_out) >= len(mappings) // 2:
                break
            if all(training[condition] > 1 for condition in conditions[name]):
                held_out.append(name)
                for condition in conditions[name]:
                    training[condition] -= 1
        for name in held_out:
            keys.setdefault(sid, set()).update(mappings[name])
    return keys


def mapping_collections(
    filters: MappingFilter | list[MappingFilter],
    validation: NamedMappings = VALIDATION_MAPPINGS,
    split_individuals: bool = True,
) -> dict[str, list[FitMappingCollection]]:
    """Select the data of a fit from the fit mappings of the studies.

    The filters select the training data, the mappings which fail them are
    excluded, and so are the summaries of data which is fitted one by one
    (`AGGREGATE_MAPPINGS`). The outliers are `OUTLIER_MAPPINGS`, and the
    validation data is `VALIDATION_MAPPINGS` with the held-out subjects by
    default (`validation_individuals`). Neither kind enters the cost; both are
    simulated and evaluated with the training data, so a report says how the
    fitted parameters describe data they were not fitted on and how far the
    data a fit dropped is from the model.

    Args:
        filters: filters of the training data.
        validation: the keys of the validation data by study.
        split_individuals: add the held-out subjects to the validation data,
            see `validation_individuals`.

    Returns:
        The fit mapping collections of all kinds by experiment id.
    """
    fit_mappings = FitMappings(
        experiment_classes=EXPERIMENT_CLASSES,
        base_path=HCTZ_PATH,
        data_path=DATA_PATHS,
    )
    subjects = validation_individuals(fit_mappings) if split_individuals else {}
    for mappings in [OUTLIER_MAPPINGS, AGGREGATE_MAPPINGS, validation, subjects]:
        check_named(mappings, fit_mappings)
    validation_keys: NamedMappings = {
        sid: validation.get(sid, set()) | subjects.get(sid, set())
        for sid in validation | subjects
    }
    # sbmlsim selects the outliers by their keys alone, which must name one
    # mapping of all studies
    outliers = {key for keys in OUTLIER_MAPPINGS.values() for key in keys}
    for key in outliers:
        studies = [
            sid
            for sid, experiment in fit_mappings.experiments.items()
            if key in experiment._fit_mappings
        ]
        if len(studies) != 1:
            raise ValueError(f"The outlier '{key}' is a mapping of {studies}.")
    selection = fit_mappings.select(
        filters=[
            *(filters if isinstance(filters, list) else [filters]),
            filter_aggregates,
        ],
        outliers=outliers,
        validation=lambda key, fit_mapping: named(validation_keys, key, fit_mapping),
        print_info=False,
    )
    # the counts per experiment and kind, not the single mappings
    selection.print(detail=False)
    # the validation mappings by the question they answer
    selected = {
        (sid, key)
        for sid, kinds in selection.kinds.items()
        for key, kind in kinds.items()
        if kind is MappingKind.VALIDATION
    }

    def pairs(mappings: NamedMappings) -> set[tuple[str, str]]:
        return {(sid, key) for sid, keys in mappings.items() for key in keys}

    console.print(
        "validation: "
        + ", ".join(
            f"{len(selected & keys)} {question}"
            for question, keys in [
                ("interaction", pairs(INTERACTION_VALIDATION)),
                ("dose", pairs(DOSE_VALIDATION)),
                ("limitation", pairs(LIMITATION_VALIDATION)),
                ("subject", pairs(subjects)),
                ("other", pairs(validation) - pairs(VALIDATION_MAPPINGS)),
            ]
        )
    )
    return selection.collections


def filter_coadministration(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Only data without coadministration.

    The coadministration arms of `INTERACTION_VALIDATION` pass: the model has no
    interaction for their drugs, so they are the prediction that none is
    needed. Their kind keeps them out of the cost. The studies of
    `STABLE_COMEDICATION` pass, their comedication is a part of the baseline.
    """
    if named(INTERACTION_VALIDATION, fit_mapping_key, fit_mapping):
        return True
    if study(fit_mapping) in STABLE_COMEDICATION:
        return True
    return mapping_metadata(fit_mapping).coadministration == Coadministration.NONE


#: Only iv and po data.
filter_iv_po = metadata_filter(route={Route.IV, Route.PO})


#: Only fasted data, the model has no food effect.
filter_fasting = metadata_filter(fasting={Fasting.NR, Fasting.FASTED})


#: Only HCTZ PK data.
filter_pk = observable_filter(PK_OBSERVABLES)


def filter_pd(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Only HCTZ PD data."""
    return observable_id(fit_mapping) not in PK_OBSERVABLES


def f_collections_all() -> dict[str, list[FitMappingCollection]]:
    """All data."""
    return mapping_collections([])


def f_collections_pk() -> dict[str, list[FitMappingCollection]]:
    """HCTZ pharmacokinetics data."""
    return mapping_collections(
        [filter_coadministration, filter_iv_po, filter_fasting, filter_pk]
    )


def f_collections_pd() -> dict[str, list[FitMappingCollection]]:
    """HCTZ pharmacodynamics data."""
    return mapping_collections(
        [filter_coadministration, filter_iv_po, filter_fasting, filter_pd]
    )


if __name__ == "__main__":
    for f in [
        f_collections_all,
        f_collections_pk,
        f_collections_pd,
    ]:
        console.rule(title=f.__name__, align="left", style="white")
        f()
