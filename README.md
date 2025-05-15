[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15427418.svg)](https://doi.org/10.5281/zenodo.15427418)

# hctz model
This repository provides the hydrochlorothiazide physiologically based pharmacokinetics (PBPK) model.

The model is distributed as [SBML](http://sbml.org) available from [`hctz_body_flat.xml`](./models/hctz_body_flat.xml) with 
corresponding SBML4humans model report at [https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_body_flat.xml](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_body_flat.xml) and equations from [`hctz_body_flat.md`](./models/hctz_body_flat.md).

The COMBINE archive is available from [`hctz_model.omex`](./hctz_model.omex).

![model overview](./figures/hctz_model.png)

### Comp submodels
The liver submodel is available from [`hctz_liver.xml`](./models/hctz_liver.xml) with corresponding SBML4humans report at
[https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_liver.xml](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_liver.xml) and equations from [`hctz_liver.md`](./models/hctz_liver.md).

The kidney submodel is available from [`hctz_kidney.xml`](./models/hctz_kidney.xml) with corresponding SBML4humans report at
[https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_kidney.xml](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_kidney.xml) and equations from [`hctz_kidney.md`](./models/hctz_kidney.md).

The intestine submodel is available from [`hctz_intestine.xml`](./models/hctz_intestine.xml) with corresponding SBML4humans report at
[https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_intestine.xml](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_intestine.xml) and equations from [`hctz_intestine.md`](./models/hctz_intestine.md).

The whole-body submodel is available from [`hctz_body.xml`](./models/hctz_body.xml) with corresponding SBML4humans report at
[https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_body.xml](https://sbml4humans.de/model_url?url=https://raw.githubusercontent.com/matthiaskoenig/hctz-model/main/models/hctz_body.xml) and equations from [`hctz_body.md`](./models/hctz_body.md).

## How to cite
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15427418.svg)](https://doi.org/10.5281/zenodo.15427418)

> Lim, A., & König, M. (2025).
> *Physiologically based pharmacokinetic (PBPK) model of hydrochlorothiazide.*   
> Zenodo. [https://doi.org/10.5281/zenodo.15427418](https://doi.org/10.5281/zenodo.15427418)

## License

* Source Code: [MIT](https://opensource.org/license/MIT)
* Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.

Funding
=======
Matthias König was supported by the Federal Ministry of Education and Research (BMBF, Germany) within LiSyM by grant number 031L0054 and ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA). This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B). 

© 2024-2025 Amanda Lim & Matthias König, [Systems Medicine of the Liver](https://livermetabolism.com)
