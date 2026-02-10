# -----------------------
# Dockerfile
# -----------------------
# Build and push image
#   docker build -f Dockerfile -t matthiaskoenig/hctz:0.6.0 -t matthiaskoenig/hctz:latest .
#   docker login
#   docker push --all-tags matthiaskoenig/hctz

FROM python:3.14-slim

# install uv
COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /bin/uv
ENV UV_SYSTEM_PYTHON=1

# install git
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# copy code
WORKDIR /code
COPY .python-version /code/.python-version
COPY pyproject.toml /code/pyproject.toml
COPY README.md /code/README.md
COPY src /code/src

# install package
RUN uv pip install -e .
