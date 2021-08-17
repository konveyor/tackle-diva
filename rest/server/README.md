# REST server for Tackle-DiVA

# Build a server image `diva-rest`

```shell
make build.base  # build diva-rest-base
make build       # build diva-rest
```

## For developer

Since `diva-rest-base` does not change so frequently, so you need not rebuild it every time when you build the server image `diva-rest`.

# Run a server container

Run this command to run the server on port 8080:

```
make run
```

Alternatively, if you just want to enter a sever container with bash:

```
make run.shell
```

# Test server

> These will be moved to [../client](../client) later

```shell
curl localhost:8080                  # to access root, which causes an error
curl localhost:8080/transaction/foo  # to access TXs, which returns an warning text
curl -L localhost:8080/ui            # to access swagger UI
```
