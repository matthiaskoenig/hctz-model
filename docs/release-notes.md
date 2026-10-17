# Release notes

## Release notes for hctz-model 0.9.1

Made from pkdb_models 1bdb95b16f with pkpdsim 0.9.2.

The changes since 0.9.0.

### Core libraries

pkpdsim 0.9.1 → 0.9.2:

- The CI workflow of a release puts `libpython` on the library search path before the dependencies are installed.

### Libraries

| Package | Previous | New |
| --- | --- | --- |
| `pkpdsim` | 0.9.1 | 0.9.2 |

<details>
<summary>All changed packages</summary>

| Package | Previous | New |
| --- | --- | --- |
| `pkpdsim` | 0.9.1 | 0.9.2 |

</details>

### Data

No changes.

### Analysis

#### Models

- `hctz_body.xml`: changed, with the same species, reactions and parameter values
- `hctz_body_flat.xml`: changed, with the same species, reactions and parameter values
- `hctz_fluid.xml`: changed, with the same species, reactions and parameter values
- `hctz_intestine.xml`: changed, with the same species, reactions and parameter values
- `hctz_kidney.xml`: changed, with the same species, reactions and parameter values

#### Experiments

No changes.

#### Fits

No changes.

## Release notes for hctz-model 0.9.0

Made from pkdb_models d5a099d3c5 with pkpdsim 0.9.1.

The changes since 0.7.1.

### Core libraries

pkpdsim 0.9.1: not used by the previous release.

sbmlsim 0.4.0 → 0.10.0 (latest 5 of 386):

- **Fit reports write the methods, the provenance and the references as HTML, Typst/PDF and LaTeX** ([#336](https://github.com/matthiaskoenig/sbmlsim/issues/336), [#342](https://github.com/matthiaskoenig/sbmlsim/pull/342)).
- **The building blocks of the reports** are public: `sbmlsim.report.document` and its renderers (sections, paragraphs with inline math, code, citations, equations, tables which break across pages, figures; HTML, Typst and LaTeX), `sbmlsim.report.references` (the bundled `references.bib` and the IEEE style `references.csl` of the CSL project, CC BY-SA 3.0, adapted to print the version note: the license of the package is `MIT AND CC-BY-SA-3.0`), `sbmlsim.fit.methods` (the methods text written from the settings, the optimizer, the analyses and the provenance; only what the fit used appears, an unknown setting raises `UnsupportedSetting`) and `sbmlsim.fit.report_document` (the tables of the results and the figures).
- **Callers describe their fits**: `FitParameter.description`, `FitDefinition.description` and `ReportContext` (title, description, descriptions of the parameters, notes), which `report_cli(context=...)` takes, and `report_from_records`, the report of stored fit records; `FisherInformation.from_dict`.
- **The provenance of a fit hashes the data files without the python files and the caches**, with checksum keys which do not depend on the platform (the provenance commit of the branch of #337 which #337 did not contain).
- **Fit results carry their provenance** ([#334](https://github.com/matthiaskoenig/sbmlsim/issues/334), [#337](https://github.com/matthiaskoenig/sbmlsim/pull/337)).

sbmlutils 0.9.6 → 0.16.0 (latest 5 of 236):

- `Interpolation.drive` drives a parameter, species or compartment of an existing model with the interpolated data, in place; x is the time or a quantity of the model, `targets` maps a column to the element it drives (#16, #500)
- `Interpolation.drive_comp` drives a model through a comp model which references the original, or embeds it with `embed=True`; flattened it simulates as the model driven in place (#16, #500)
- `Interpolation.assignment_rules` gives the interpolation as assignment rules of a model definition (#16, #500)
- linear and cubic spline interpolation hold the first value before and the last value after the data, instead of `0.0` (#16, #500)
- data which cannot be interpolated raises a `ValueError` instead of a warning: fewer than 2 columns or data points (3 for the cubic spline), column names which are not strings or repeat, a first column which is not an SBML id, a column which is not numeric, a missing or infinite value, x which repeats (#16, #500)

### Libraries

| Package | Previous | New |
| --- | --- | --- |
| `libsbgnpy` | - | 0.7.0 |
| `pkpdsim` | - | 0.9.1 |
| `pkpdutils` | - | 1.3.0 |
| `plotly` | 6.5.1 | 7.1.0 |
| `pymetadata` | 0.5.10 | 0.8.1 |
| `sbmlode` | - | 0.3.0 |
| `sbmlsim` | 0.4.0 | 0.10.0 |
| `sbmlutils` | 0.9.6 | 0.16.0 |
| `scikit-learn` | 1.8.0 | 1.9.1 |
| `typst` | 0.14.5 | 0.15.0 |

110 other packages changed.

<details>
<summary>All changed packages</summary>

| Package | Previous | New |
| --- | --- | --- |
| `altair` | 6.0.0 | - |
| `annotated-doc` | 0.0.4 | - |
| `annotated-types` | 0.7.0 | 0.8.0 |
| `antimony` | 3.1.1 | 3.1.3 |
| `anyio` | 4.12.1 | - |
| `asttokens` | 3.0.1 | - |
| `attrs` | 25.4.0 | 26.1.0 |
| `bottleneck` | 1.6.0 | - |
| `certifi` | 2026.1.4 | 2026.7.22 |
| `chardet` | 5.2.0 | 7.6.0 |
| `charset-normalizer` | 3.4.4 | 3.5.2 |
| `click` | 8.3.1 | 8.5.0 |
| `cloudpickle` | - | 3.1.2 |
| `coloredlogs` | 15.0.1 | - |
| `contourpy` | 1.3.3 | 1.4.0 |
| `decorator` | 5.2.1 | 5.3.1 |
| `deepmerge` | - | 3.0.1 |
| `depinfo` | 2.2.0 | - |
| `dill` | 0.4.0 | 0.4.1 |
| `elementpath` | 5.1.0 | - |
| `executing` | 2.2.1 | - |
| `fastapi` | 0.128.0 | - |
| `fastobo` | 0.14.1 | - |
| `fonttools` | 4.61.1 | 4.66.1 |
| `google-auth` | 2.47.0 | - |
| `google-auth-oauthlib` | 1.2.2 | - |
| `gspread` | 5.12.4 | - |
| `gspread-pandas` | 3.3.0 | - |
| `h11` | 0.16.0 | - |
| `h5netcdf` | - | 1.8.1 |
| `h5py` | - | 3.16.0 |
| `humanfriendly` | 10.0 | - |
| `idna` | 3.11 | 3.20 |
| `ipython` | 9.9.0 | - |
| `ipython-pygments-lexers` | 1.1.1 | - |
| `jedi` | 0.19.2 | - |
| `joblib` | 1.5.3 | 1.6.0 |
| `kiwisolver` | 1.4.9 | 1.5.1 |
| `latex2mathml` | - | 3.81.1 |
| `libroadrunner` | 2.9.2 | 2.10.0 |
| `libsbgnpy` | - | 0.7.0 |
| `lxml` | 6.0.2 | 6.1.3 |
| `markdown` | - | 3.11 |
| `markdown-it-py` | 4.0.0 | 4.2.0 |
| `markupsafe` | 3.0.3 | 3.0.4 |
| `matplotlib` | 3.10.8 | 3.11.2 |
| `matplotlib-inline` | 0.2.1 | - |
| `multiprocess` | 0.70.18 | 0.70.19 |
| `narwhals` | 2.15.0 | 2.26.0 |
| `networkx` | 3.6.1 | 3.7 |
| `numpy` | 2.4.1 | 2.5.3 |
| `oauthlib` | 3.3.1 | - |
| `packaging` | 25.0 | 26.3 |
| `pandas` | 2.3.3 | 3.0.6 |
| `parso` | 0.8.5 | - |
| `pathspec` | - | 1.1.1 |
| `patsy` | 1.0.2 | - |
| `petab` | 0.8.1 | 0.9.0 |
| `pexpect` | 4.9.0 | - |
| `pillow` | 12.1.0 | 12.3.0 |
| `pint` | 0.25.2 | 0.26.1 |
| `pkdb-analysis` | 0.3.1 | - |
| `pkpdsim` | - | 0.9.1 |
| `pkpdutils` | - | 1.3.0 |
| `platformdirs` | 4.5.1 | 4.12.4 |
| `plotly` | 6.5.1 | 7.1.0 |
| `prompt-toolkit` | 3.0.52 | - |
| `pronto` | 2.7.2 | - |
| `psutil` | 7.2.1 | - |
| `ptyprocess` | 0.7.0 | - |
| `pure-eval` | 0.2.3 | - |
| `py4cytoscape` | 1.12.0 | 1.13.0 |
| `pyasn1` | 0.6.1 | - |
| `pyasn1-modules` | 0.4.2 | - |
| `pydantic` | 2.12.5 | 2.14.0 |
| `pydantic-core` | 2.41.5 | 2.50.0 |
| `pydoe` | 0.3.8 | - |
| `pygments` | 2.19.2 | 2.21.0 |
| `pymdown-extensions` | - | 12.1 |
| `pymetadata` | 0.5.10 | 0.8.1 |
| `pyparsing` | 3.3.1 | 3.3.3 |
| `pyreadline3` | 3.5.4 | - |
| `python-libnuml` | 1.1.7 | - |
| `python-libsbml` | 5.21.0 | 5.21.2 |
| `python-libsedml` | 2.0.33 | - |
| `python-multipart` | 0.0.21 | - |
| `pytz` | 2025.2 | - |
| `requests` | 2.32.5 | 2.34.2 |
| `requests-oauthlib` | 2.0.0 | - |
| `rich` | 14.2.0 | 15.0.0 |
| `rpds-py` | 0.30.0 | 2026.9.1 |
| `rsa` | 4.9.1 | - |
| `salib` | 1.5.2 | 1.6.0 |
| `sbmlmath` | - | 0.4.1 |
| `sbmlode` | - | 0.3.0 |
| `sbmlsim` | 0.4.0 | 0.10.0 |
| `sbmlutils` | 0.9.6 | 0.16.0 |
| `scikit-learn` | 1.8.0 | 1.9.1 |
| `scipy` | 1.17.0 | 1.18.1 |
| `setproctitle` | 1.3.7 | - |
| `setuptools` | 80.9.0 | - |
| `stack-data` | 0.6.3 | - |
| `starlette` | 0.50.0 | - |
| `statsmodels` | 0.14.6 | - |
| `threadpoolctl` | 3.6.0 | 3.7.0 |
| `tomli` | - | 2.5.0 |
| `traitlets` | 5.14.3 | - |
| `typing-extensions` | 4.15.0 | 4.16.0 |
| `typing-inspection` | 0.4.2 | 0.4.4 |
| `typst` | 0.14.5 | 0.15.0 |
| `tzdata` | 2025.3 | 2026.5 |
| `urllib3` | 2.6.3 | 2.8.0 |
| `uvicorn` | 0.40.0 | - |
| `wcwidth` | 0.2.14 | - |
| `xarray` | 2025.12.0 | 2026.9.0 |
| `xlsxwriter` | 3.2.9 | - |
| `xmlschema` | 4.3.0 | - |
| `xmltodict` | 1.0.2 | 1.0.4 |
| `xsdata` | - | 26.2 |
| `zensical` | - | 0.0.69 |

</details>

### Data

- Added: `hydrochlorothiazide/Ernst2006`
- Removed: `hydrochlorothiazide/Beerman1976`
- Changed: `hydrochlorothiazide/Anderson1961`, `hydrochlorothiazide/Azumaya1990`, `hydrochlorothiazide/Barbhaiya1982`, `hydrochlorothiazide/Beermann1976`, `hydrochlorothiazide/Beermann1977a`, `hydrochlorothiazide/Dussol2005`, `hydrochlorothiazide/Hunninghake1986`, `hydrochlorothiazide/Januszewicz1959`, `hydrochlorothiazide/Jeon2012`, `hydrochlorothiazide/Jordo1979`, `hydrochlorothiazide/Knauf1995`, `hydrochlorothiazide/Nilsen1989`, `hydrochlorothiazide/Patel1984`, `hydrochlorothiazide/Ripley2000`, `hydrochlorothiazide/Weir1998`, `hydrochlorothiazide/Williams1982`

### Analysis

#### Models

- `hctz_body.xml`: added 5 parameters; removed 6 parameters; changed values `E50_hctz_nacl` 0.000157686 → 8.61825e-05, `Emax_hctz_cl` 1.0073 → 0.45749, `Emax_hctz_na` 1.85461 → 1.72545, `Ka_dis_hctz` 0.351813 → 1.30141, `Kp_hctz` 0.999728 → 2.36426, `f_GFR_Qki` 151 → 76.3105, `ftissue_hctz` 0.246144 → 0.0637161, `k_cl` 0.00300248 → 0.00370717, `k_na` 0.000645997 → 0.00067665
- `hctz_body_flat.xml`: added 1 reaction, 7 parameters; removed 1 species, 1 reaction, 8 parameters; changed values `E50_hctz_nacl` 0.000157686 → 8.61825e-05, `Emax_hctz_cl` 1.0073 → 0.45749, `Emax_hctz_na` 1.85461 → 1.72545, `GU__F_hctz_abs` 0.612131 → 0.7, `GU__HCTZABS_k` 0.0204138 → 0.00507166, `Ka_dis_hctz` 0.351813 → 1.30141, `Kp_hctz` 0.999728 → 2.36426, `f_GFR_Qki` 151 → 76.3105, `ftissue_hctz` 0.246144 → 0.0637161, `k_cl` 0.00300248 → 0.00370717, `k_na` 0.000645997 → 0.00067665
- `hctz_fluid.xml`: added 3 parameters; removed 1 parameter; changed values `E50_hctz_nacl` 0.000157686 → 8.61825e-05, `Emax_hctz_cl` 1.0073 → 0.45749, `Emax_hctz_na` 1.85461 → 1.72545, `k_cl` 0.00300248 → 0.00370717, `k_na` 0.000645997 → 0.00067665
- `hctz_intestine.xml`: added 1 reaction, 2 parameters; removed 1 species, 1 reaction; changed values `F_hctz_abs` 0.612131 → 0.7, `HCTZABS_k` 0.0204138 → 0.00507166
- `hctz_kidney.xml`: added 1 parameter; removed 2 parameters

#### Experiments

- Added: `BloodPressureExperiment`

#### Fits

- `PD`: `PD_20261017_030352__10c1d`, no fit record in the previous release
- `PK`: `PK_20261017_025702__4167a`, no fit record in the previous release

## Release notes for hctz-model v0.7.1

We are pleased to release a new version of the hctz-model including the following changes:

- consistent color assignment in figures
- fixes for running code

Your hctz-model team

## Release notes for hctz-model v0.7.0

We are pleased to release a new version of the hctz-model including the 
following changes:

- model changes for preprint
- updated parameter optimization

Your hctz-model team

## Release notes for hctz-model v0.6.0

We are pleased to release a new version of the hctz-model including the 
following changes:

- major model improvements

Your hctz-model team

## Release notes for hctz-model v0.5.1

We are pleased to release a new version of the hctz-model including the 
following changes:

- initial model release
- fixed dois

Your hctz-model team

## Release notes for hctz-model v0.5.0

We are pleased to release a new version of the hctz-model including the 
following changes:

- initial model release

Your hctz-model team

