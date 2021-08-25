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

Or you can run the server locally (with debug mode):

```
make run.local
```

Alternatively, if you just want to enter a sever container with bash:

```
make run.shell
```

# Test server

## Unit test

This test runs an web server locally (which does not involve Java part) and tests.

If you use poetry,

```
poetry run pytest test // or test/test_local_server.py
```

## Deprecated: If you want to test at low-level 

> These will be moved to [../client](../client) later

```shell
curl localhost:8080                  # to access root, which causes an error
curl localhost:8080/transaction/foo  # to access TXs, which returns an warning text
curl -L localhost:8080/ui            # to access swagger UI
```
