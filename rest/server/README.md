# REST Server Docker Image of Tackle-DiVA

## Quickstart

### Build and start the server

At project root, build `diva` image:

```bash
git clone https://github.com/shinsa82-sgi-2021/tackle-diva.git
cd tackle-diva
docker build -t diva .
```

Then build the server image, `diva-server` at this directory:

```bash
cd rest/server
docker build -t diva-server .
```

Run server container (by default, the server listens on port 8080):

```bash
docker run --rm -p "8080:8080" --name=diva-server diva-server:latest
```

### Play with Swagger UI

You can play with the API from Swagger UI webpage (http://localhost:8080/ui).

### Using other OpenAPI client tools

You can get OpenAPI speciication file from http://localhost:8080/openapi.yaml or http://localhost:8080/openapi.json.

### Using CLI tools

Alternatively, CLI tools like `curl` and `wget` can be used.

```bash
$ curl localhost:8080/healthz # invoke the health check API
{
  "detail": "Server is working",
  "status_code": 0,
  "version": "1.0.0rc1"
}
```

See bash scripts in [scripts](scripts) for other APIs.

----
## Further details

See [docs/README.md](docs/README.md) for more detail (also for developers).
