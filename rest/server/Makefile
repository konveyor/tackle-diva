build: Dockerfile
	poetry export --without-hashes -o ./requirements.txt
	poetry build
	docker build -t diva-server:latest . 

run:
	docker run --rm -p "8080:8080" --name=diva-server diva-server:latest

run.shell:
	docker run --rm -it diva-server:latest bash

run.local:
	poetry run connexion run -p 8080 --mock=notimplemented --strict-validation --validate-responses \
	--debug spec/openapi.yaml

# remove python caches under source code dir.
# it does not remove them under the virtual env (= ".venv/")
clean:
	find src test -name '__pycache__' -type d | xargs rm -r
	rm -rf ./.pytest_cache
