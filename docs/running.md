# Running the model

Clone the repository:

```bash
git clone https://github.com/matthiaskoenig/hctz-model.git
cd hctz-model
```

The analyses of the release are commands of the run layer of [sbmlsim](https://github.com/matthiaskoenig/sbmlsim), `python -m sbmlsim.run <kind> <spec> --out <directory>`, with the specs in `specs/` with which the release was built; every command writes into its own empty output directory. The analyses of the model are listed with:

```bash
uv run python -m sbmlsim.run list pkdb_models.models.hctz:MODEL
```

## uv

Run the analyses with [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
uv sync
uv run python -m sbmlsim.run factory specs/factory.json --out results/factory
uv run python -m sbmlsim.run simulate specs/simulate.json --out results/simulate
uv run python -m sbmlsim.run simulate specs/uncertainty.json --out results/uncertainty
uv run python -m sbmlsim.run report specs/report.json --out results/report
uv run python -m sbmlsim.run credibility specs/credibility.json --out results/credibility
```

The simulations with the confidence interval of the adopted fits are `specs/uncertainty.json`.

The reports of the adopted fits are recreated from their records, one folder per fit in `results/report` (`specs/report.json`).

## pip

If you use pip install the package via

```bash
pip install -e .
```

and run the analyses in the environment, e.g.:

```bash
python -m sbmlsim.run factory specs/factory.json --out results/factory
python -m sbmlsim.run simulate specs/simulate.json --out results/simulate
python -m sbmlsim.run simulate specs/uncertainty.json --out results/uncertainty
python -m sbmlsim.run report specs/report.json --out results/report
python -m sbmlsim.run credibility specs/credibility.json --out results/credibility
```

## docker

Simulations can also be run within a docker container:

```bash
docker run -v "${PWD}/results:/results" -it matthiaskoenig/hctz:latest /bin/bash
```

Run the analyses:

```bash
uv run python -m sbmlsim.run factory specs/factory.json --out /results/factory
uv run python -m sbmlsim.run simulate specs/simulate.json --out /results/simulate
uv run python -m sbmlsim.run simulate specs/uncertainty.json --out /results/uncertainty
uv run python -m sbmlsim.run report specs/report.json --out /results/report
uv run python -m sbmlsim.run credibility specs/credibility.json --out /results/credibility
```

The results are written into the mounted `/results` folder on the host.

In case of permission issues with the mounted folder, adjust ownership and access rights with:

```bash
sudo chown $(id -u):$(id -g) -R "${PWD}/results"
sudo chmod 775 "${PWD}/results"
```
