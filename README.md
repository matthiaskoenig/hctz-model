[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15427418.svg)](https://doi.org/10.5281/zenodo.15427418)
[![GitHub Action](https://github.com/matthiaskoenig/hctz-model/actions/workflows/python.yml/badge.svg)](https://github.com/matthiaskoenig/hctz-model/actions/workflows/python.yml)
[![GitHub Action](https://github.com/matthiaskoenig/hctz-model/actions/workflows/docker.yml/badge.svg)](https://github.com/matthiaskoenig/hctz-model/actions/workflows/docker.yml)

# hctz model
This repository provides the hctz physiologically based pharmacokinetics/ pharmacodynamics (PBPK/PD) model.

The model is distributed as [SBML](http://sbml.org) format available from [`hctz_body_flat.xml`](./models/hctz_body_flat.xml) with 
corresponding [SBML4humans model report](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_body_flat.xml) and [model equations](./models/hctz_body_flat.md).

The COMBINE archive is available from [`hctz_model.omex`](./hctz_model.omex).

![model overview](./figures/hctz_model.png)

### Comp submodels
* **kidney** submodel [`hctz_kidney.xml`](./models/hctz_kidney.xml) with [SBML4humans report](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_kidney.xml) and [equations](./models/hctz_kidney.md).
* **intestine** submodel [`hctz_intestine.xml`](./models/hctz_intestine.xml) with [SBML4humans report](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_intestine.xml) and [equations](./models/hctz_intestine.md).
* **whole-body** submodel [`hctz_body.xml`](./models/hctz_body.xml) with [SBML4humans report](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_body.xml) and [equations](./models/hctz_body.md).
* **raas** submodel [`hctz_raas.xml`](./models/hctz_raas.xml) with [SBML4humans report](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_raas.xml) and [equations](./models/hctz_raas.md).
* **fluid** submodel [`hctz_fluid.xml`](./models/hctz_fluid.xml) with [SBML4humans report](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_fluid.xml) and [equations](./models/hctz_fluid.md).

## How to cite
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15427418.svg)](https://doi.org/10.5281/zenodo.15427418)

> Schwaiger, A. & König, M. (2026).
> *Physiologically based pharmacokinetic/pharmacodynamic (PBPK) model of hctz.*   
> Zenodo. [https://doi.org/10.5281/zenodo.15427418](https://doi.org/10.5281/zenodo.15427418)

## License

* Source Code: [MIT](https://opensource.org/license/MIT)
* Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.


## Run simulations
### python
Clone the repository 
```bash
git clone https://github.com/matthiaskoenig/hctz-model.git
cd hctz-model
```

#### uv
Run the complete analysis with uv (https://docs.astral.sh/uv/getting-started/installation/):
```bash
uv run run_hctz -a all -r results
```

#### pip
If you use pip install the package via
```bash
pip install -e .
```
Run the complete analysis in the environment via:
```bash
run run_hctz -a all -r results
```

### docker
Simulations can also be run within a docker container:

```bash
docker run -v "${PWD}/results:/results" -it matthiaskoenig/hctz:latest /bin/bash
```

Run the complete analysis:
```bash
uv run run_hctz -a all -r /results
```
The results are written into the mounted `/results` folder on the host.

In case of permission issues with the mounted folder, adjust ownership and access rights with:
```bash
sudo chown $(id -u):$(id -g) -R "${PWD}/results"
sudo chmod 775 "${PWD}/results"
```

## Funding
Matthias König was supported by the Federal Ministry of Research, Technology and Space (BMFTR, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA). This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B).

© 2024-2026 Amanda Schwaiger and Matthias König, [Systems Medicine of the Liver](https://livermetabolism.com)
