## From https://raw.githubusercontent.com/astral-sh/uv-docker-example/refs/heads/main/multistage.Dockerfile

################################################################################
#                 Multi stage docker, for Streamlit INSEL App                  #
################################################################################

################################################################################
#                         Stage 1 : UV + dependencies                          #
################################################################################

# An example using multi-stage image builds to create a final image without uv.

# First, build the application in the `/app` directory.
# See `Dockerfile` for details.
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Disable Python downloads, because we want to use the system interpreter
# across both images. If using a managed Python version, it needs to be
# copied from the build image into the final image; see `standalone.Dockerfile`
# for an example.
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

################################################################################
#                                 INSEL + App                                  #
################################################################################

# It is important to use the image that matches the builder, as the path to the
# Python executable must be the same, e.g., using `python:3.11-slim-bookworm`
# will fail.
FROM python:3.12-slim-bookworm

########################
#  INSEL, without GUI  #
########################
ARG INSEL_VERSION=8.3.2.0b
ARG DEBIAN_FRONTEND=noninteractive

ARG INSEL_DEB="insel_${INSEL_VERSION}_x64_mini.deb"
ARG INSEL_URL=https://insel.eu/download/${INSEL_DEB}

RUN apt-get update && \
    apt-get install curl \
      gnuplot \
      --no-install-recommends -y && \
    curl ${INSEL_URL} -o /tmp/${INSEL_DEB} -k && \
    apt-get install /tmp/${INSEL_DEB} --no-install-recommends -y && \
    apt-get remove curl -y && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    rm /tmp/${INSEL_DEB}

########################
#         App          #
########################

# Setup a non-root user
RUN groupadd --system --gid 1234 nonroot \
 && useradd --system --gid 1234 --uid 1234 --create-home nonroot

# Copy the application from the builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Use the non-root user to run our application
USER nonroot

# Use `/app` as the working directory
WORKDIR /app

CMD ["streamlit", "run", "pv_invest.py", "--browser.gatherUsageStats", "false"]
