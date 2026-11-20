[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15427418.svg)](https://doi.org/10.5281/zenodo.15427418)
[![Release](https://img.shields.io/github/v/release/matthiaskoenig/hctz-model)](https://github.com/matthiaskoenig/hctz-model/releases)
[![Documentation](https://github.com/matthiaskoenig/hctz-model/actions/workflows/docs.yml/badge.svg)](https://matthiaskoenig.github.io/hctz-model/)
[![CI](https://github.com/matthiaskoenig/hctz-model/actions/workflows/ci.yml/badge.svg)](https://github.com/matthiaskoenig/hctz-model/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/docker/v/matthiaskoenig/hctz?sort=semver&label=docker)](https://hub.docker.com/r/matthiaskoenig/hctz)
[![Python](https://img.shields.io/badge/python-3.14%20%7C%203.15-blue)](https://www.python.org)
[![Code license: MIT](https://img.shields.io/badge/code%20license-MIT-blue)](https://opensource.org/license/MIT)
[![Model license: CC BY-SA 4.0](https://img.shields.io/badge/model%20license-CC%20BY--SA%204.0-lightgrey)](https://creativecommons.org/licenses/by-sa/4.0/)

# Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model of hydrochlorothiazide

This repository provides the hydrochlorothiazide (hctz) physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model.

Open the app of the model in your browser, every simulation runs there: <https://matthiaskoenig.github.io/hctz-model/hctz_app.html> (one file, also [`models/hctz_app.html`](models/hctz_app.html))

Documentation: <https://matthiaskoenig.github.io/hctz-model/>

Credibility of the model for its contexts of use: [https://matthiaskoenig.github.io/hctz-model/credibility.html](https://matthiaskoenig.github.io/hctz-model/credibility.html)

## Model

![hctz_body_body](models/hctz_body_body.svg)

![hctz_body](models/hctz_body.svg)

## Quick start

```bash
git clone https://github.com/matthiaskoenig/hctz-model.git && cd hctz-model
uv sync
uv run python -m sbmlsim.run simulate specs/simulate.json --out results/simulate
```

## How to cite

> Schwaiger, A. & König, M. (2026). *Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model of hydrochlorothiazide*. Zenodo. https://doi.org/10.5281/zenodo.15427418

## License

* Source Code: [MIT](https://opensource.org/license/MIT)
* Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

&copy; 2024-2026 Amanda Schwaiger and Matthias König
