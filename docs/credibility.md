# Credibility

[Credibility report](https://matthiaskoenig.github.io/hctz-model/credibility/index.html)

The assessment of the contexts of use of the model against its adopted fits. A context of use is decided on its validation evidence; a description (C1) is decided on its calibration evidence, the data the model was fitted to.

| Context of use | Title | Level | Risk | Verdict | Decided on |
| --- | --- | --- | --- | --- | --- |
| `describe` | Describe the data of the fits | C1 | low | supported | calibration |
| `dose` | Oral doses in healthy adults | C2 | low | supported | validation |
| `renal` | Impaired renal function | C3 | medium | insufficient evidence | validation |
| `interaction` | Coadministration without an interaction | C3 | medium | supported | validation |
| `pd` | Natriuresis and chloruresis in healthy adults | C5 | low | insufficient evidence | validation |

## describe: Describe the data of the fits

**Question:** Does the model describe the pharmacokinetic and pharmacodynamic data of HCTZ it was fitted to?

**Verdict:** supported, decided on the calibration evidence, level C1, model risk low (influence low, consequence low), 676 of 688 decisive points evaluable (minimum 5).

| Quantity of interest | Description | Kind | Coverage | Points |
| --- | --- | --- | --- | --- |
| `Carm_hctz` | the plasma concentration of HCTZ | absolute | covered | 298 |
| `Aurine_hctz` | the cumulative amount of HCTZ in urine | absolute | covered | 205 |
| `Rurine_hctz` | the urinary excretion rate of HCTZ | absolute | covered | 10 |
| `Afeces_hctz` | the cumulative amount of HCTZ in feces | absolute | covered | 2 |
| `FLUID__na_urine` | the cumulative amount of sodium in urine | absolute | covered | 69 |
| `FLUID__cl_urine` | the cumulative amount of chloride in urine | absolute | covered | 51 |
| `FLUID__Vurine` | the cumulative urine volume | absolute | covered | 29 |
| `FLUID__bp_systolic` | the systolic blood pressure | absolute | covered | 6 |
| `FLUID__bp_diastolic` | the diastolic blood pressure | absolute | covered | 6 |

**Claimed domain:**

| Field | Value | Coverage | Points |
| --- | --- | --- | --- |
| `route` | `PO` | calibrated | 667 |
| `route` | `IV` | calibrated | 9 |
| `health` | `HEALTHY` | calibrated | 570 |
| `health` | `HYPERTENSION` | calibrated | 35 |
| `health` | `RENAL_IMPAIRMENT` | calibrated | 57 |
| `health` | `T2DM` | calibrated | 14 |

Beyond the metadata: the training data of the fits PK and PD: oral doses of 5 to 200 mg and intravenous doses of 1 to 65 mg, single and multiple dosing; type 2 diabetes is PK data only. The patients with an impaired renal function are training data as well, by decision, so the renal behaviour of the model (the GFR and the activity of SLC22A6, both scaled by `f_renal_function`) is calibrated here and validated nowhere, see `renal` (statement, not assessed)

| Acceptance criterion | Value | Limit | Met |
| --- | --- | --- | --- |
| `within_2fold` | 91.57 | >= 70 | yes |

Inputs, the simulated covariates of the subjects and the doses of 173 of the 173 decisive mappings against the ones their studies report:

| Input | Mappings | Simulated | Equivalent | In range | Differ | Not reported |
| --- | --- | --- | --- | --- | --- | --- |
| `BW` | 173 | 73 kg | 39 | 14 | 2 | 118 |
| `HEIGHT` | 173 | 176 cm | 8 | 0 | 0 | 165 |
| `IVDOSE_hctz` (dose) | 4 | 1 to 65 mg | 4 | 0 | 0 | 0 |
| `PODOSE_hctz` (dose) | 153 | 12.5 to 200 mg | 153 | 0 | 0 | 0 |
| `SOLDOSE_hctz` (dose) | 13 | 5 to 25 mg | 13 | 0 | 0 | 0 |

| Mapping | Input | Simulated | Reported | Reported by |
| --- | --- | --- | --- | --- |
| Niemeyer1983/fm_Fig1_hctz50_C | `BW` | 73 kg | 96.3 kg | individual C |
| Niemeyer1983/fm_Fig1_hctz50_W | `BW` | 73 kg | 55 kg | individual W |

| Verification | Factor | Points | Largest difference | Result |
| --- | --- | --- | --- | --- |
| tolerances | `discretization_error` | 688 | 0.0008 | passed |
| second integration method | `numerical_solver_error` | 688 | 0.00078 | passed |
| setup of the simulations | `use_error` | 688 |  | passed |

## dose: Oral doses in healthy adults

**Question:** Which plasma concentration and cumulative urinary and fecal excretion of HCTZ follow from a single oral dose within the range of the data in healthy adults?

**Verdict:** supported, decided on the validation evidence, level C2, model risk low (influence medium, consequence low), 66 of 66 decisive points evaluable (minimum 5).

| Quantity of interest | Description | Kind | Coverage | Points |
| --- | --- | --- | --- | --- |
| `Carm_hctz` | the plasma concentration of HCTZ | absolute | covered | 35 |
| `Aurine_hctz` | the cumulative amount of HCTZ in urine | absolute | covered | 29 |
| `Afeces_hctz` | the cumulative amount of HCTZ in feces | absolute | covered | 2 |

**Claimed domain:**

| Field | Value | Coverage | Points |
| --- | --- | --- | --- |
| `route` | `PO` | validated | 66 |
| `health` | `HEALTHY` | validated | 66 |
| `coadministration` | `NONE` | validated | 66 |
| `dosing` | `SINGLE` | validated | 66 |

Beyond the metadata: single oral doses of 5 to 200 mg as tablet, capsule or solution, fasted or not reported; validated on 5, 12.5, 50 and 65 mg (5 to 65 mg), the doses of 75 to 200 mg are calibration only; the urinary excretion rate is not claimed, it has training data only (`describe`) (statement, not assessed)

| Acceptance criterion | Value | Limit | Met |
| --- | --- | --- | --- |
| `within_2fold` | 93.94 | >= 70 | yes |

Temporal validation: no decisive study was collected after its fit (5 collected before).

Inputs, the simulated covariates of the subjects and the doses of 20 of the 20 decisive mappings against the ones their studies report:

| Input | Mappings | Simulated | Equivalent | In range | Differ | Not reported |
| --- | --- | --- | --- | --- | --- | --- |
| `BW` | 20 | 73 kg | 2 | 0 | 0 | 18 |
| `HEIGHT` | 20 | 176 cm | 0 | 0 | 0 | 20 |
| `PODOSE_hctz` (dose) | 9 | 12.5 to 65 mg | 9 | 0 | 0 | 0 |
| `SOLDOSE_hctz` (dose) | 11 | 5 to 12.5 mg | 11 | 0 | 0 | 0 |

| Verification | Factor | Points | Largest difference | Result |
| --- | --- | --- | --- | --- |
| tolerances | `discretization_error` | 66 | 8.9e-06 | passed |
| second integration method | `numerical_solver_error` | 66 | 1.1e-05 | passed |
| setup of the simulations | `use_error` | 66 |  | passed |

## renal: Impaired renal function

**Question:** Which plasma concentration and urinary excretion of HCTZ, and which urinary excretion of sodium, follow from an oral dose in patients with an impaired renal function?

**Verdict:** insufficient evidence, decided on the validation evidence, level C3, model risk medium (influence medium, consequence medium), 10 of 10 decisive points evaluable (minimum 10).

| Quantity of interest | Description | Kind | Coverage | Points |
| --- | --- | --- | --- | --- |
| `Carm_hctz` | the plasma concentration of HCTZ | absolute | covered | 10 |
| `Aurine_hctz` | the cumulative amount of HCTZ in urine | absolute | uncovered | 0 |
| `FLUID__na_urine` | the cumulative amount of sodium in urine | absolute | uncovered | 0 |

**Claimed domain:**

| Field | Value | Coverage | Points |
| --- | --- | --- | --- |
| `route` | `PO` | validated | 10 |
| `health` | `RENAL_IMPAIRMENT` | validated | 10 |

Beyond the metadata: single oral doses of 25 mg (Knauf1995, 19 patients with a chronic renal insufficiency, creatinine clearance 1 to 153 ml/min with the controls) and 50 mg (Niemeyer1983, patients S and W, creatinine clearance 30 and 10 ml/min); the renal function enters a simulation as `f_renal_function`, which scales the GFR and, since the PBPK library of pkpdsim 0.21, the activity of the tubular transporter SLC22A6 as well (`fimp_ki_slc22a6`) (statement, not assessed)

| Acceptance criterion | Value | Limit | Met |
| --- | --- | --- | --- |
| `within_2fold` | 80 | >= 80 | yes |
| `GMFE` | 1.456 | <= 1.5 | yes |

Temporal validation: no decisive study was collected after its fit (1 collected before).

Inputs, the simulated covariates of the subjects and the doses of 1 of the 1 decisive mappings against the ones their studies report:

| Input | Mappings | Simulated | Equivalent | In range | Differ | Not reported |
| --- | --- | --- | --- | --- | --- | --- |
| `BW` | 1 | 73 kg | 0 | 0 | 1 | 0 |
| `HEIGHT` | 1 | 176 cm | 0 | 0 | 0 | 1 |
| `PODOSE_hctz` (dose) | 1 | 50 mg | 1 | 0 | 0 | 0 |

| Mapping | Input | Simulated | Reported | Reported by |
| --- | --- | --- | --- | --- |
| Niemeyer1983/fm_Fig1_hctz50_S | `BW` | 73 kg | 57.6 kg | individual S |

| Verification | Factor | Points | Largest difference | Result |
| --- | --- | --- | --- | --- |
| tolerances | `discretization_error` | 10 | 6.6e-06 | passed |
| second integration method | `numerical_solver_error` | 10 | 4.5e-06 | passed |
| setup of the simulations | `use_error` | 10 |  | passed |

## interaction: Coadministration without an interaction

**Question:** Does the model predict the pharmacokinetics of HCTZ with coadministered aliskiren, diltiazem, enalapril or lisinopril without an interaction?

**Verdict:** supported, decided on the validation evidence, level C3, model risk medium (influence medium, consequence medium), 116 of 117 decisive points evaluable (minimum 10).

| Quantity of interest | Description | Kind | Coverage | Points |
| --- | --- | --- | --- | --- |
| `Carm_hctz` | the plasma concentration of HCTZ | absolute | covered | 108 |
| `Aurine_hctz` | the cumulative amount of HCTZ in urine | absolute | covered | 8 |
| `hctz_auc_ratio` | the AUC of HCTZ with the coadministered drug over the AUC without it | ratio, no pairing declared | n/a | n/a |

**Claimed domain:**

| Field | Value | Coverage | Points |
| --- | --- | --- | --- |
| `route` | `PO` | validated | 116 |
| `health` | `HEALTHY` | validated | 116 |
| `coadministration` | `ALISKIREN` | validated | 13 |
| `coadministration` | `DILTIAZEM` | validated | 19 |
| `coadministration` | `ENALAPRIL` | validated | 54 |
| `coadministration` | `LISINOPRIL` | validated | 30 |

Beyond the metadata: 12.5 and 25 mg of HCTZ with the doses of the coadministered drugs of the arms, single and multiple dosing, as separate tablets and as combination tablets (statement, not assessed)

| Acceptance criterion | Value | Limit | Met |
| --- | --- | --- | --- |
| `within_2fold` | 100 | >= 80 | yes |
| `GMFE` | 1.162 | <= 1.5 | yes |

Temporal validation: no decisive study was collected after its fit (5 collected before).

Inputs, the simulated covariates of the subjects and the doses of 11 of the 11 decisive mappings against the ones their studies report:

| Input | Mappings | Simulated | Equivalent | In range | Differ | Not reported |
| --- | --- | --- | --- | --- | --- | --- |
| `BW` | 11 | 73 kg | 5 | 0 | 0 | 6 |
| `HEIGHT` | 11 | 176 cm | 3 | 0 | 0 | 8 |
| `PODOSE_hctz` (dose) | 11 | 12.5 to 25 mg | 11 | 0 | 0 | 0 |

| Verification | Factor | Points | Largest difference | Result |
| --- | --- | --- | --- | --- |
| tolerances | `discretization_error` | 117 | 1.8e-05 | passed |
| second integration method | `numerical_solver_error` | 117 | 1.5e-05 | passed |
| setup of the simulations | `use_error` | 117 |  | passed |

## pd: Natriuresis and chloruresis in healthy adults

**Question:** Which urinary excretion of sodium and chloride follows from a single oral dose of HCTZ within the range of the data in healthy adults?

**Verdict:** insufficient evidence, decided on the validation evidence, level C5, model risk low (influence medium, consequence low), 2 of 2 decisive points evaluable (minimum 5).

| Quantity of interest | Description | Kind | Coverage | Points |
| --- | --- | --- | --- | --- |
| `FLUID__na_urine` | the cumulative amount of sodium in urine | absolute | covered | 1 |
| `FLUID__cl_urine` | the cumulative amount of chloride in urine | absolute | covered | 1 |

**Claimed domain:**

| Field | Value | Coverage | Points |
| --- | --- | --- | --- |
| `route` | `PO` | validated | 2 |
| `health` | `HEALTHY` | validated | 2 |
| `coadministration` | `NONE` | validated | 2 |
| `dosing` | `SINGLE` | validated | 2 |

Beyond the metadata: single oral doses of 12.5 to 100 mg, the cumulative excretion after the dose; validated on the 50 mg tablet of Patel1984 only (2 points, one sodium and one chloride value), the other doses are calibration only; the urine volume and the blood pressure are not claimed (statement, not assessed)

| Acceptance criterion | Value | Limit | Met |
| --- | --- | --- | --- |
| `within_2fold` | 100 | >= 70 | yes |

Temporal validation: no decisive study was collected after its fit (1 collected before).

Inputs, the simulated covariates of the subjects and the doses of 2 of the 2 decisive mappings against the ones their studies report:

| Input | Mappings | Simulated | Equivalent | In range | Differ | Not reported |
| --- | --- | --- | --- | --- | --- | --- |
| `BW` | 2 | 73 kg | 2 | 0 | 0 | 0 |
| `HEIGHT` | 2 | 176 cm | 0 | 0 | 0 | 2 |
| `PODOSE_hctz` (dose) | 2 | 50 mg | 2 | 0 | 0 | 0 |

| Verification | Factor | Points | Largest difference | Result |
| --- | --- | --- | --- | --- |
| tolerances | `discretization_error` | 2 | 1e-06 | passed |
| second integration method | `numerical_solver_error` | 2 | 1.3e-06 | passed |
| setup of the simulations | `use_error` | 2 |  | passed |

## Study data

The data of every study with points in the adopted fits, as the simulations read it, and the record of its collection from pkdb_data.

| Study | Points | First collected | Latest collection | Released | pkdb_data | Tables |
| --- | --- | --- | --- | --- | --- | --- |
| Anderson1961 | 76 | 2026-02-10 (git) | 2026-10-25 | 2025-11-18 `PKDB01102` | unknown | 6 as collected |
| Azumaya1990 | 19 | 2026-02-10 (git) | 2026-10-25 | 2025-11-18 `PKDB01103` | unknown | 4 as collected |
| Barbhaiya1982 | 34 | 2026-02-10 (git) | 2026-10-25 | 2024-03-26 `PKDB00751` | unknown | 8 as collected |
| Barbhaiya1982a | 36 | 2026-02-10 (git) | 2026-10-25 | 2025-11-18 `PKDB01104` | unknown | 6 as collected |
| Beermann1976 | 68 | 2026-02-10 (git) | 2026-10-25 | 2024-03-26 `PKDB00752` | unknown | 6 as collected |
| Beermann1977a | 87 | 2026-02-10 (git) | 2026-10-25 | 2025-03-06 `PKDB00821` | unknown | 11 as collected |
| Devineni2014 | 14 | 2026-02-10 (git) | 2026-10-25 | 2024-09-13 `PKDB00879` | unknown | 8 as collected |
| Giudicelli1987 | 18 | 2026-02-10 (git) | 2026-10-25 | 2024-03-26 `PKDB00753` | unknown | 11 as collected |
| Heise2015 | 14 | 2026-02-10 (git) | 2026-10-25 | 2024-07-08 `PKDB00852` | unknown | 9 as collected |
| Howes1991 | 33 | 2026-02-10 (git) | 2026-10-25 | 2024-04-24 `PKDB00777` | unknown | 7 as collected |
| Hsiao2015 | 11 | 2026-02-10 (git) | 2026-10-25 | 2024-03-26 `PKDB00754` | unknown | 5 as collected |
| Hunninghake1986 | 25 | 2026-02-10 (git) | 2026-10-25 | 2024-03-26 `PKDB00755` | unknown | 7 as collected |
| Jeon2012 | 30 | 2026-02-10 (git) | 2026-10-25 | 2024-03-26 `PKDB00756` | unknown | 8 as collected |
| Jordo1979 | 36 | 2026-02-10 (git) | 2026-10-25 | 2024-03-26 `PKDB00757` | unknown | 7 as collected |
| Knauf1995 | 62 | 2026-02-10 (git) | 2026-10-25 | not released | unknown | 9 as collected |
| Koytchev2004 | 30 | 2026-02-10 (git) | 2026-10-25 | 2024-07-08 `PKDB00853` | unknown | 7 as collected |
| Niemeyer1983 | 24 | 2026-02-10 (git) | 2026-10-25 | 2024-03-26 `PKDB00758` | unknown | 7 as collected |
| Nilsen1989 | 6 | 2026-02-10 (git) | 2026-10-25 | 2025-11-18 `PKDB01107` | unknown | 8 as collected |
| Niopas2004 | 33 | 2026-02-10 (git) | 2026-10-25 | 2024-04-24 `PKDB00789` | unknown | 7 as collected |
| Patel1984 | 150 | 2026-02-10 (git) | 2026-10-25 | 2024-03-26 `PKDB00759` | unknown | 8 as collected |
| Ripley2000 | 10 | 2026-02-10 (git) | 2026-10-25 | 2025-11-18 `PKDB01108` | unknown | 8 as collected |
| Vaidyanathan2006 | 26 | 2026-02-10 (git) | 2026-10-25 | 2023-03-19 `PKDB00681` | unknown | 8 as collected |
| Weir1998 | 38 | 2026-02-10 (git) | 2026-10-25 | 2024-03-26 `PKDB00760` | unknown | 7 as collected |
| Williams1982 | 84 | 2026-02-10 (git) | 2026-10-25 | 2025-11-18 `PKDB01109` | unknown | 7 as collected |

## Battery of the variants

The variants of the model are checked without data, the same for every context of use; a failed check makes every context not verified.

| Check | Factor | Cases | Largest deviation | Result |
| --- | --- | --- | --- | --- |
| dose states of the model | `use_error` | 1 |  | passed |
| mass balance | `numerical_code_verification` | 5 | 3.5e-15 | passed |
| non-negativity | `numerical_code_verification` | 64 | 6.3e-31 | passed |
| zero dose | `numerical_code_verification` | 58 | 0 | passed |
| steady state | `numerical_code_verification` | 65 | 6.9e-15 | passed |
| superposition | `numerical_code_verification` | 4 | 3.4e-09 | passed |
| second simulator | `numerical_code_verification` |  |  | not applicable: AMICI is not installed, install sbmlsim with the extra 'amici'. |
| plausibility of the values | `use_error` | 495 |  | passed |
| rebuild | `software_quality_assurance` | 13 |  | passed |
