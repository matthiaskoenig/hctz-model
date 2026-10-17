# HCTZ

Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model of the diuretic hydrochlorothiazide (HCTZ): its absorption in the intestine, its distribution, its renal excretion and its effect on the sodium, chloride and water balance and on the blood pressure.

## Structure

- `models/`: the tissue models (`model_intestine.py`, `model_kidney.py`), the fluid and blood pressure model (`model_fluid.py`) and the whole-body model (`model_body.py`). `models/factory.py` creates the SBML models, the flattened whole-body model which is simulated, the ODEs and the COMBINE archive in `models/output/`.
- `experiments/`: the simulation experiments of the clinical studies (`studies/`), the dose dependency and the test of the blood pressure model (`misc/`) and the parameter scans (`scans/`). The fit mappings are described with the vocabulary of `pkpdsim.metadata`.
- `fitting/`: the fit problems of the pharmacokinetics (`PK`) and the pharmacodynamics (`PD`), the report, the identifiability analysis and the PEtab export of a fit.
- `sensitivity/`: the sensitivity analysis of the pharmacokinetic and pharmacodynamic parameters.
- `thesis/`: the supplementary figures of the thesis.
- `data/`: the data of the studies, a subset of the PK-DB studies (`data/collect_data.py`).

## Commands

```bash
# models, simulations
run_simulation pkdb_models.models.hctz --action factory
run_simulation pkdb_models.models.hctz --action list_experiments
run_simulation pkdb_models.models.hctz --action simulate --experiments all
run_simulation pkdb_models.models.hctz --action simulate --experiments all --uncertainty

# fits, adoption of a fit, reports of stored parameters, identifiability, PEtab
run_fit pkdb_models.models.hctz --subset=PK --runs=10 --cores=10
run_fit pkdb_models.models.hctz --adopt PK_<fit id>
run_report pkdb_models.models.hctz --subset=PK results/fit/PK_<fit id>/parameters.json
run_identifiability pkdb_models.models.hctz --subset=PK results/fit/PK_<fit id>/parameters.json
python -m pkdb_models.models.hctz.fitting.petab_problem --subset=PK

# sensitivity analysis (local by default) and the supplementary figures
python -m pkdb_models.models.hctz.sensitivity.sensitivity_analysis
python -m pkdb_models.models.hctz.thesis.supplementary_figures
```

The results are written into `results/` of the model.

## Adopted fits and uncertainty

The values of the fitted parameters come from the adopted fits of the model,
not from numbers in the code. `run_fit pkdb_models.models.hctz --adopt <fit id>`
copies the record of a finished fit (its parameters, problem, profile
likelihood and Fisher information) into `models/output/fits/<fit id>/`, which is
tracked; the ids of the adopted fits are listed in `fits` of the model object
(`__init__.py`). The factory takes the fitted values and their uncertainty from
the records (`models/fits.py`) and writes the uncertainty into the SBML
(`distrib:uncertainty`). `run_simulation ... --uncertainty` runs the
experiments over draws of these distributions and draws the simulations as the
median with a band of quantiles into `results/simulation_uncertainty`. A refit
is: fit, adopt, replace the id in `fits`, rebuild the model. See the
documentation of the repository on fitting (`docs/fitting.md`).
