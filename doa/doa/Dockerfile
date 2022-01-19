#
# Dockerfile for 
#   diva-doa Docker image.
#
# Note:
#   Build-time variable (--build-arg) named "IMAGE_VER" to be specified when built.
#   If omitted, this is set to the default value "unknown".
# 
FROM python:3.10-slim
ARG IMAGE_VER=unknown
LABEL project=diva name=doa version=${IMAGE_VER}

SHELL ["/bin/bash", "-c"]

COPY . /work
# COPY migrate.sh /work/
# COPY manifests /work/
WORKDIR /work

# install dependencies.
# git is used by migrate.sh to get from app repo,
# curl is used to get kubectl binary.
RUN apt update \
    && apt upgrade -y --no-install-recommends \
    && apt install -y git curl \
    && apt autoremove -y \
    && apt clean \
    && rm -r /var/lib/apt/lists/*
RUN curl -LO "https://dl.k8s.io/release/v1.22.3/bin/linux/amd64/kubectl" \
    && curl -LO "https://dl.k8s.io/v1.22.3/bin/linux/amd64/kubectl.sha256" \
    && echo "$(<kubectl.sha256) kubectl" | sha256sum --check \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm kubectl

RUN pip3 install --user colorama typer

ENTRYPOINT ["/bin/bash", "/work/migrate.sh"]
