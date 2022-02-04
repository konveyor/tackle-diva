#!/bin/bash
# generate files from templates.

set -eu

# idiom to use the common.sh utilities.

WORK_DIR=$(readlink -f $(dirname $0)) # this script's directory
. ${WORK_DIR}/common.sh

INPUT_DIR=$(readlink -f "${WORK_DIR}/../in")
ENV_FILE=$(readlink -f "${WORK_DIR}/../env.yaml")

show_vars() {
    if [[ -v debug ]]; then
        echo
        debug "[DEBUG] variables:"
        debug "  REPO_ROOT  = ${REPO_ROOT}"
        debug "  WORK_DIR   = ${WORK_DIR}"
        debug "  CUR_DIR    = ${CUR_DIR}"
        debug "  INPUT_DIR  = ${INPUT_DIR}"
        debug "  ENV_FILE   = ${ENV_FILE}"
    fi
}

show_vars

# main logic starts here.

echo 
info "generating files..."
mkdir -p "${REPO_ROOT}/out"  # for debug

info "generating Makefile..."
jinja2 --strict ${INPUT_DIR}/Makefile ${ENV_FILE} > "${REPO_ROOT}/Makefile"
info "written to ${REPO_ROOT}/Makefile"

info "generating migrate.sh..."
jinja2 --strict ${INPUT_DIR}/migrate.sh ${ENV_FILE} > "${REPO_ROOT}/doa/migrate.sh"
info "written to ${REPO_ROOT}/doa/migrate.sh"

info "generating __init__.py..."
jinja2 --strict ${INPUT_DIR}/__init__.py ${ENV_FILE} > "${REPO_ROOT}/doa/analyzers/__init__.py"
info "written to ${REPO_ROOT}/doa/analyzers/__init__.py"

info "generation completed."