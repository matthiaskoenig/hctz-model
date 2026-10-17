"""HCTZ parameter fitting.

The fit problems of the HCTZ model: which fit mapping collections enter a fit
and which parameters are adjusted, see `FIT_DEFINITIONS`. The commands
`run_fit`, `run_report` and `run_identifiability` of pkpdsim run them with the
package of the model, a fit is followed by the identifiability analysis of its
parameters (`--no-identifiability` skips it):

    run_fit pkdb_models.models.hctz --subset=PK --runs=10 --cores=10 --seed=1234 --method=LSQ --strategy=ALL --name=PK_LSQ_ALL
    run_fit pkdb_models.models.hctz --subset=PD --runs=10 --cores=10 --seed=1234 --method=LSQ --strategy=ALL --name=PD_LSQ_ALL

The identifiability analysis is the profile likelihood of every fitted
parameter around the best parameter set and the Fisher information of the same
set, which end up in the identifiability section of the report of the fit. The
profiles are the expensive part of the analysis - every point of a profile
optimizes the other parameters again - so they run on `--cores` cores:

    # fit and analysis, the profiles resolved with at most 30 points per side
    run_fit pkdb_models.models.hctz --subset=PK --runs=10 --cores=10 --max-points=30

    # the fit alone
    run_fit pkdb_models.models.hctz --subset=PK --runs=10 --cores=10 --no-identifiability

The results, figures and the HTML report are written into the fit folder of the
model (`MODEL.fit_dir`), unless `--output_dir` is given. The identifiability of
parameters which were fitted earlier is analysed without fitting again with the
`run_identifiability` command, a report of stored parameters is created with
the `run_report` command:

    run_identifiability pkdb_models.models.hctz --subset=PK results/fit/PK_<fit id>/parameters.json
    run_report pkdb_models.models.hctz --subset=PK results/fit/PK_<fit id>/parameters.json
"""

from pkpdsim.fit import default_fit_settings
from sbmlsim.fit.cli import FitDefinition

from pkdb_models.models.hctz import DATA_PATHS, HCTZ_PATH
from pkdb_models.models.hctz.fitting.mapping_collections import (
    f_collections_pd,
    f_collections_pk,
)
from pkdb_models.models.hctz.fitting.parameters import parameters_pd, parameters_pk

#: settings of the fits, stored with the result and read back by the report
FIT_SETTINGS = default_fit_settings(absolute_tolerance=1e-6)

#: the fit problems of the HCTZ model, the keys are the `--subset` argument
FIT_DEFINITIONS: dict[str, FitDefinition] = {
    # all pharmacokinetics data
    "PK": FitDefinition(
        mapping_collections=f_collections_pk,
        parameters=parameters_pk,
        base_path=HCTZ_PATH,
        data_path=DATA_PATHS,
        settings=FIT_SETTINGS,
    ),
    # pharmacodynamics data
    "PD": FitDefinition(
        mapping_collections=f_collections_pd,
        parameters=parameters_pd,
        base_path=HCTZ_PATH,
        data_path=DATA_PATHS,
        settings=FIT_SETTINGS,
    ),
}
