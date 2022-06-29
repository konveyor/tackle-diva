base_dir=$(abspath $(dir $(lastword $(MAKEFILE_LIST))))

IMAGE_NAME=diva-doa
IMAGE_VER=2.4.0
QUAY_IMAGE=quay.io/konveyor/tackle-diva-doa:latest
RUN_IMAGE=$(IMAGE_NAME):latest
DOCKERFILE=$(base_dir)/.devcontainer/Dockerfile
DOCKER_CONTEXT=$(base_dir)/doa
# DOCKER_BUILD_OPT=--progress=plain
DOCKER_BUILD_OPT=

SAMPLE_REPO_URL=https://github.com/saud-aslam/trading-app
SAMPLE_DIR=$(base_dir)/plsql-example

OUT_DIR=/tmp/out
STAT_DIR=/tmp/stats


# execute this in devcontainer-cli
test-build-local:
	make -C container-image build test-build

test-northwind-local:
	doa convert -i devcontainer-container/0.in-oracle -o ./out -v

test-build:
	docker run --rm -it $(QUAY_IMAGE) python -m doa.cli --help

test-northwind:
	doa convert -i devcontainer-container/0.in-oracle -o ./out -v

# executing run-doa.sh with a debug flag
run:
	rm -rf $(OUT_DIR)
	bash $(base_dir)/run-doa.sh -d -o $(OUT_DIR) -i start_up.sh $(SAMPLE_REPO_URL)
	@echo
	@echo "listing generated files..."
	ls -lFR --color $(OUT_DIR)

# executing PL/SQL conversion sample
run-plsql:
	rm -rf $(OUT_DIR)
	bash $(base_dir)/run-doa.sh -d -o $(OUT_DIR) -l oracle -f $(SAMPLE_DIR)
	@echo
	@echo "listing generated files..."
	ls -lFR --color $(OUT_DIR)

run-direct:
	rm -rf /tmp/out
	@echo "[CONFIG] base dir = $(base_dir)"
	bash $(base_dir)/doa/migrate.sh -o /tmp/out -i start_up.sh $(SAMPLE_REPO_URL)
	@echo
	@echo "listing generated files..."
	ls -lFR --color /tmp/out

# executing PL/SQL conversion sample in dev container.
run-plsql-direct:
	rm -rf $(OUT_DIR)
	bash $(base_dir)/doa/migrate.sh -o $(OUT_DIR) -l oracle -f $(SAMPLE_DIR)
	@echo
	@echo "listing generated files..."
	ls -lFR --color $(OUT_DIR)

# run-plsql-direct-debug:
# 	rm -rf $(OUT_DIR)
# 	bash $(base_dir)/doa/migrate.sh -o $(OUT_DIR) -i start_up.sh -l oracle -f $(SAMPLE_DIR)
# 	@echo
# 	@echo "listing generated files..."
# 	ls -lFR --color $(OUT_DIR)

# Script to list created database. Execute after the test Pod is deployed.
test-show-tables:
	kubectl exec app-test -it -- psql -h app-db -U postgres -c "\dt"

run-sqal-direct:
	rm -rf $(OUT_DIR) $(STAT_DIR)
	python -m sqal.doa -n foo-app -i $(SAMPLE_DIR) -o $(OUT_DIR) --stat-dir $(STAT_DIR) --use-debug-listener
	@echo
	@echo "listing generated files..."
	ls -lFR --color $(OUT_DIR)
	ls -lFR --color $(STAT_DIR)

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

# copy generated plsql library
copy-plsql:
	rm -r $(base_dir)/doa/sqal/sqal/plsql
	cp -r $(base_dir)/doa/sqal/java-env/plsql $(base_dir)/doa/sqal/sqal
	touch $(base_dir)/doa/sqal/sqal/plsql/__init__.py

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

# clean cache files
clean:
	find $(base_dir) -name __pycache__ | xargs rm -rf 
	find $(base_dir) -name .pytest_cache | xargs rm -rf 

#
# tests.
#
test-normal:
	cd $(base_dir) && bash ./run-doa.sh -o /tmp/out -i start_up.sh https://github.com/saud-aslam/trading-app && ls -lFR --color /tmp/out/trading-app

test-oracle:
	cd $(base_dir) && bash ./run-doa.sh -o /tmp/out -l oracle -f "$(base_dir)/plsql-example" &&	ls -lFR --color /tmp/out/app

test: test-normal test-oracle

test-verify:
	docker run --rm -d \
		--name=doa-verify \
        -e POSTGRES_USER=postgres \
        -e POSTGRES_DB=postgres \
        -e POSTGRES_PASSWORD=postgres \
		-e PGHOST=localhost \
    	-e PGUSER=postgres \
    	-e PGDATABASE=postgres \
    	-e PGPASSWORD=postgres \
		-v "$(base_dir)/doa/verify.sh:/app/verify.sh" \
		postgres:13.5-alpine
	sleep 5
	docker exec -it doa-verify /app/verify.sh
	docker stop doa-verify
