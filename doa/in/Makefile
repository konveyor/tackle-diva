base_dir=$(abspath $(dir $(lastword $(MAKEFILE_LIST))))

IMAGE_NAME={{image_name}}
IMAGE_VER={{version}}
RUN_IMAGE=$(IMAGE_NAME):latest
DOCKERFILE=$(base_dir)/.devcontainer/Dockerfile
DOCKER_CONTEXT=$(base_dir)/doa
# DOCKER_BUILD_OPT=--progress=plain
DOCKER_BUILD_OPT=

SAMPLE_REPO_URL=https://github.com/saud-aslam/trading-app

run:
	# executing run-doa.sh with a debug flag
	rm -rf ./_out
	bash $(base_dir)/run-doa.sh -d -o ./_out -i start_up.sh $(SAMPLE_REPO_URL)
	@echo
	@echo "listing generated files..."
	ls -lFR --color ./_out

run-direct:
	rm -rf /tmp/out
	@echo "[CONFIG] base dir = $(base_dir)"
	bash $(base_dir)/doa/migrate.sh -o /tmp/out -i start_up.sh $(SAMPLE_REPO_URL)
	@echo
	@echo "listing generated files..."
	ls -lFR --color /tmp/out

# test for starting docker container
docker:
	-rm -rf ./_out
	docker run -it --rm -v $(abspath ./_out):/out $(RUN_IMAGE) -o /out $(REPO_URL)
	ls -lF --color ./_out

# for dev and debug: no need to rebuild the image
docker-dev:
	-rm -rf ./_out
	docker run -it --rm -v $(abspath ./_out):/out \
		-v $(abspath ./doa):/work $(RUN_IMAGE) -o /out $(REPO_URL)
	ls -lF --color ./_out

# for dev and debug: run {{image_name}} container and run bash
bash:
	docker run -it --rm --entrypoint=/bin/bash $(RUN_IMAGE)

# dev utilities
build:
	@echo "building Docker image of DiVA migrator..."
	@echo "base dir = $(base_dir)"
	docker build $(DOCKER_BUILD_OPT) \
		-t $(IMAGE_NAME):$(IMAGE_VER) \
		--build-arg IMAGE_VER=$(IMAGE_VER) \
		-f $(DOCKERFILE) \
		$(DOCKER_CONTEXT)
	docker tag $(IMAGE_NAME):$(IMAGE_VER) $(IMAGE_NAME):latest
	@echo
	docker image ls $(IMAGE_NAME)
	@echo
	@echo "build completed."
