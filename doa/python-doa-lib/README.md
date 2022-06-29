# Dev Container for DOA Library

This Dev Container is for development of `python-doa-lib` library using `poetry` package manager.

## Dev Container Configuration

This is actually "Dev Containers", consists of a Python container (`app`) and a PostgreSQL container (`db`).
- (`tr`,) `nkf` and `psql` is installed on `app`.
- Environment variables are set in `app`, so you can access the DB just by `psql`.

## Install

`poetry install` (already done in the Dev Container)
No venv is created, all dependencies are directly installed.

## Install Check

Run `make -C tests test-install` and check if a help message is shown.

## Usage
 
See the document of `poetry`. Typical commands are:

- `poetry list [-t] [-l]`
- `poetry add`
- `poetry update`
- `poetry version [<version>]`

## Test

- Run `pytest`. (you do not need to run `poetry run pytest`)
- Run `make test` (if you need logs run `test-v` or `test-vv`).
  - Generated files will be in [/tmp/a.results/](/tmp/a.results/).
  - If you want the generated directory be in this directory,
  run `make test-local` and so on. Files are generated in [./output](./output)

## For developer

PL/SQL Parser is developed under `java-env` directory.
If you change the grammar definition, you need to build the (Python binding of) parser and copy the generated directory as `./doa/plsql`.
