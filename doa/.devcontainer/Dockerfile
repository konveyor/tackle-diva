# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.209.6/containers/python-3/.devcontainer/base.Dockerfile

# Dockerfile for dev container. At this point, there is another Dockerfile for building app container.
# Build context is supposed to be "../doa" (= tackle-diva/doa/doa) -> changing to ".." (= tackle-diva/doa). 

# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT="3.10-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT} AS base

ARG IMAGE_VER=unknown
LABEL project=diva name=doa version=${IMAGE_VER}

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# mandatory: nkf
# useful for development: bash-completion, tree, nmon
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends nkf bash-completion tree nmon

# install docker client only
RUN sudo mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends docker-ce-cli
RUN groupadd docker
RUN usermod -aG docker vscode # does not work?

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1

# install kubectl
RUN curl -LO "https://dl.k8s.io/release/v1.22.3/bin/linux/amd64/kubectl" \
    && curl -LO "https://dl.k8s.io/v1.22.3/bin/linux/amd64/kubectl.sha256" \
    # && echo "$(<kubectl.sha256) kubectl" | sha256sum --check \
    && echo " kubectl" | cat kubectl.sha256 - | sha256sum --check \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm kubectl

# install Python libraries
# RUN su vscode -c "pip3 install --user colorama typer wasabi lark pyyaml==5.4.1 jinja2-cli antlr4-python3-runtime more-itertools rich"

ENV POETRY_VIRTUALENVS_CREATE=false

# installing poetry, Python tool for package developers
RUN su vscode -c "curl -sSL https://install.python-poetry.org | python3 -"
RUN /home/vscode/.local/bin/poetry completions bash > /etc/bash_completion.d/poetry.bash-completion

# multi-stage build for packaging
FROM base AS doa
# copy context directory (tackle-diva/doa/doa) to /work
COPY . /work
WORKDIR /work

USER vscode 
RUN pip3 install --user -e ./sqal
RUN pip3 install --user -r ./requirements.txt
