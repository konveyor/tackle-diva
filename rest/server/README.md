# REST server for Tackle-DiVA

# Build a server image `diva-rest`

```shell
make build.base  # build diva-rest-base
make build       # build diva-rest
```

## For developer

Since `diva-rest-base` does not change so frequently, so you need not rebuild it every time when you build the server image `diva-rest`.

# Run a server container

Run this command to run a server container on port 8080:

```
make run
```

Alternatively, if you just want to enter a sever container with bash:

```
make run.shell
```

# Test server


## Deprecated: If you want to test at low-level 

> These will be moved to [../client](../client) later

```shell
curl localhost:8080                  # to access root, which causes an error
curl localhost:8080/transaction/foo  # to access TXs, which returns an warning text
curl -L localhost:8080/ui            # to access swagger UI
```

# Dev and test locally

Note that Java part is not involved in the local development.

## Prereq

- `Python 3.7.x`
- `poetry` 

At this directory, activate `Python 3.7.x` (e.g. like `pyenv local 3.7`) and run `poetry install` to setup.

## Build

No need to build.

## (Unit) test

This test runs an web server locally (which does not involve Java part) and tests.

```shell
poetry run pytest test
# poetry run pytest test/test_local_server.py
```

## Run

You can run web server locally (with debug mode):

```bash
make run.local
```

Then you can test the server using curl in another terminal, like this:

```bash
curl localhost:8080                  # to access root, which causes a 404 error
curl localhost:8080/transaction/foo  # to access TXs, which returns an warning text
curl -L localhost:8080/ui            # to access swagger UI
curl -L localhost:8080/openapi.json  # to access openapi.json
```
