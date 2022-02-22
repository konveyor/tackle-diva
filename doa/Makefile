base_dir=$(abspath $(dir $(lastword $(MAKEFILE_LIST))))

IMAGE_NAME=diva-doa
IMAGE_VER=2.0.0
RUN_IMAGE=$(IMAGE_NAME):latest
DOCKERFILE=$(base_dir)/.devcontainer/Dockerfile
DOCKER_CONTEXT=$(base_dir)/doa
# DOCKER_BUILD_OPT=--progress=plain
DOCKER_BUILD_OPT=

SAMPLE_REPO_URL=https://github.com/saud-aslam/trading-app
OUT_DIR=/tmp/out

# executing run-doa.sh with a debug flag
run:
	rm -rf $(OUT_DIR)
	bash $(base_dir)/run-doa.sh -d -o $(OUT_DIR) -i start_up.sh $(SAMPLE_REPO_URL)
	@echo
	@echo "listing generated files..."
	ls -lFR --color $(OUT_DIR)/trading-app

run-direct:
	rm -rf $(OUT_DIR)
	@echo "[CONFIG] base dir = $(base_dir)"
	bash $(base_dir)/doa/migrate.sh -o $(OUT_DIR) -i start_up.sh $(SAMPLE_REPO_URL)
	@echo
	@echo "listing generated files..."
	ls -lFR --color $(OUT_DIR)/trading-app

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

# for dev and debug: run diva-doa container and run bash
bash:
	docker run -it --rm --entrypoint=/bin/bash $(RUN_IMAGE)

# dev utilities
build:
	@echo "build by 'make build' is deprecated."
	@echo "execute 'bash util/build.sh' instead."
	@exit 1
