FROM ubuntu@sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852
LABEL org.opencontainers.image.source="https://github.com/VOC-Experiments/ci-coordinator"
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash ca-certificates coreutils findutils sed tar gzip \
    git openssl gnupg gpgv apt-utils dpkg rpm createrepo-c python3 python3-venv libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m venv /opt/core-ci/python \
    && /opt/core-ci/python/bin/pip install --no-cache-dir --require-hashes --only-binary=:all: -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt
RUN useradd --uid 1001 --create-home publisher
USER 1001:1001
