# Build script for diva-doa image.
# experimental at this point.
SHELL=/bin/bash

CONTAINER_COMMAND=docker
COMPOSE=docker compose
PROGRESS=auto # or "plain" or "tty"
IMAGE_NAME=
IMAGE_VERSION=


all: build-image

build: get-vars init-context
	$(CONTAINER_COMMAND) build -t $(IMAGE_NAME):$(IMAGE_VERSION) -f ./Dockerfile ./context --progress=$(PROGRESS)
	$(CONTAINER_COMMAND) tag $(IMAGE_NAME):$(IMAGE_VERSION) $(IMAGE_NAME):latest
	$(CONTAINER_COMMAND) tag $(IMAGE_NAME):$(IMAGE_VERSION) quay.io/konveyor/tackle-diva-doa:$(IMAGE_VERSION)

# push image to quay.io using robot account
# only admins of the tacke-diva-doa repo know credential and are allowed to push. 
push: get-vars
	docker push quay.io/konveyor/tackle-diva-doa:$(IMAGE_VERSION)

init-context:
	cp -r ../python-doa-lib ./context/

# create venv ".venv" to get configs from pyproject.toml
prep-venv:
	rm -rf .venv
	python -m venv .venv
	source .venv/bin/activate && pip install -U pip tomlkit typer

get-vars: prep-venv
	$(eval IMAGE_NAME := $(shell source .venv/bin/activate && python ./get-configs.py image-name))
	$(eval IMAGE_VERSION := $(shell source .venv/bin/activate && python ./get-configs.py version))

# test for the image built; show usage of DOA
test-build:
	$(CONTAINER_COMMAND) run --rm -it diva-doa:latest python -m doa.cli --help

# run a testcase (Northwind) using docker compose
test-run:
	rm -rf ./output
	mkdir -p ./output
	$(COMPOSE) run --rm \
		-v $(shell readlink -f ../devcontainer-container/0.in-oracle):/opt/in \
		-v $(shell readlink -f ./output):/opt/out \
		app \
		python -m doa.cli -n northwind -i /opt/in -o /opt/out
	$(COMPOSE) stop

clean:
	rm -rf ./context/python-doa-lib .venv ./output
