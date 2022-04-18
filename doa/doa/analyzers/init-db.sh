#!/bin/bash

# Runs in init-db container.
# This script executes all SQL files in ${SQL_ROOT} directory, without considering execution order.

# If necessary, log output to cwd.
OUT_DIR=$(readlink -f .)
OUT_FILE=${OUT_DIR}/log.txt

shopt -s globstar  # enable use of ** in filename patterns

function main() {
    for sqlfile in ${SQL_ROOT}/**/*.sql; do
        echo "executing ${sqlfile}..."
        psql -h ${DB_HOST} -U postgres -f "${sqlfile}"
    done
}

main
