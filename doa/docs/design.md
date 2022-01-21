# (Working draft) Development Policy, Design Document and Implementation

## Past Releases (Tags)

- `v1.0.0`: first release. (Nov., 2021)

## Branches

- `main`: the main branch (and dev branch for v2). See this branch for the latest revision.
  - You cannot directly push to `main` branch. Need to create a PR.
- `v1`: ver. 1 release branch.

## Overall: Development env.

Use dev-container of VS Code. 

- Start up VS Code in the repository root and select ReOpen in Container.
- In the dev container, repository directory `diva-doa` is mounted on `/workspace/diva-doa` and you are there.
- You can run `doa/migrate.sh` directly like:
    ```bash
    bash doa/migrate.sh -o /tmp/out https://github.com/saud-aslam/trading-app
    ls /tmp/out  # list generated files
    ```

## Overall: Python integration

- Use `poetry` (https://python-poetry.org/) for dependency management and installation.
    - It's fast.
    - It can resolve dependencies that pip cannot.
- Use `typer` (https://typer.tiangolo.com/) for CLI apps.
    - Type based: easy to read, code and test.
    - Automatically create shell-completion files.

----
# Architecture

## Overall

We write `${ROOT}` for the repository root of the `diva-doa`, that points to [..](..).
Files related to tool main logic is just as follows:

```
${ROOT}
├── doa/
└── run-doa.sh
```

- [${ROOT}/doa](../doa) contains main logic and mounted on `/work` in the Docker image.
  - [${ROOT}/doa/migrate.sh](../doa/migrate.sh) is the main script.
- [${ROOT}/run-doa.sh](../run-doa.sh) is a wrapper script, This starts a container of `diva-doa` image and run the main script. 

Hereafter, app directory in the container is denoted by `${WORK}`.

## Main Logic

A main script [${WORK}/migrate.sh](../doa/migrate.sh) will be executed.

## DBMS config. analysis

None

## SQL file analysis

Currently, logic is implemented in a main script.
To be moved to `${WORK}/analyzers/analyze-sqls.py`.

- Glob `*.sql` files using Python `iglob`.
- Genrate manifest(s) of ConfigMap resource(s).

### Possible Issues and limitations:

- to appear.

## Misc.

To be appear.
