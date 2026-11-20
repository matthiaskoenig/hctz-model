"""The fitted parameters of the HCTZ model, from the records of its adopted fits.

The value of a fitted parameter, its uncertainty and the provenance of both come
from the record of its fit in `models/output/fits` (`MODEL.adopted_fits()`), see
`sbmlsim.fit.records.AdoptedRecords`; the factory takes them with
`FITS.parameter(pid, unit=...)`.
"""

from pkdb_models.models.hctz import MODEL

FITS = MODEL.fit_records()
