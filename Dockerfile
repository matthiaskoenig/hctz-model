# The image is built and pushed by the publishing of the release (python -m sbmlsim.release publish).

FROM python:3.14-slim

# install uv
COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /bin/uv

# install git
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# copy code
WORKDIR /code
COPY .python-version /code/.python-version
COPY pyproject.toml /code/pyproject.toml
COPY uv.lock /code/uv.lock
COPY README.md /code/README.md
COPY src /code/src
COPY specs /code/specs

# install package
RUN uv sync --locked --no-dev
ENV PATH="/code/.venv/bin:$PATH"
