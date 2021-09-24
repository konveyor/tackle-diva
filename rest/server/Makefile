build.base: Dockerfile.base
	docker build -t diva-rest-base:latest -f Dockerfile.base .

build: Dockerfile
	docker build -t diva-rest:latest . 

run:
	docker run --rm -p "8080:8080" --name=diva-rest diva-rest:latest

run.shell:
	docker run --rm -it diva-rest:latest bash

run.base:
	docker run --rm -it diva-rest-base:latest bash

run.local:
	poetry run connexion run -p 8080 --mock=notimplemented --strict-validation --validate-responses \
	--debug spec/openapi.yaml

# remove python caches under source code dir.
# it does not remove them under the virtual env (= ".venv/")
clean:
	find src -name '__pycache__' -type d | xargs rm -r
