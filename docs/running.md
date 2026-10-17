# Running the model

Clone the repository:

```bash
git clone https://github.com/matthiaskoenig/hctz-model.git
cd hctz-model
```

## uv

Run the complete analysis with [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
uv sync
uv run run_simulation pkdb_models.models.hctz --action all -r results
```

The simulations with the confidence interval of the adopted fits:

```bash
uv run run_simulation pkdb_models.models.hctz --action all --uncertainty -r results
```

The reports of the adopted fits are recreated from their records, one folder per fit in `results/fit_reports`:

```bash
uv run run_report pkdb_models.models.hctz --adopted -o results/fit_reports
```

## pip

If you use pip install the package via

```bash
pip install -e .
```

and run the complete analysis in the environment via:

```bash
run_simulation pkdb_models.models.hctz --action all -r results
```

## docker

Simulations can also be run within a docker container:

```bash
docker run -v "${PWD}/results:/results" -it matthiaskoenig/hctz:latest /bin/bash
```

Run the complete analysis:

```bash
uv run run_simulation pkdb_models.models.hctz --action all -r /results
```

The results are written into the mounted `/results` folder on the host.

In case of permission issues with the mounted folder, adjust ownership and access rights with:

```bash
sudo chown $(id -u):$(id -g) -R "${PWD}/results"
sudo chmod 775 "${PWD}/results"
```
