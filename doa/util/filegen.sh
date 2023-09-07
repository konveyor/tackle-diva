#!/bin/bash
# generate files from templates.
# This script should be ran in the dev container.

set -e  # abort on error
set -u  # error on undefined variables

# idiom to use the common.sh utilities.

WORK_DIR=$(readlink -f $(dirname $0)) # this script's directory
. ${WORK_DIR}/common.sh

echo "-----------------------"
echo "DiVA-DOA file generator"
echo "-----------------------"

INPUT_DIR=$(readlink -f "${WORK_DIR}/../in")
ENV_FILE=$(readlink -f "${WORK_DIR}/../env.yaml")

show_vars() {
    if [[ -v debug ]]; then
        echo
        debug "[DEBUG] variables:"
        debug "  DOA_VERSION = ${DOA_VERSION}"
        debug "  REPO_ROOT   = ${REPO_ROOT}"
        debug "  WORK_DIR    = ${WORK_DIR}"
        debug "  CUR_DIR     = ${CUR_DIR}"
        debug "  INPUT_DIR   = ${INPUT_DIR}"
        debug "  ENV_FILE    = ${ENV_FILE}"
    fi
}

show_vars

# main logic starts here.

mkdir -p "${REPO_ROOT}/out"  # for debug

echo
echo "generating Makefile..."
jinja2 --strict ${INPUT_DIR}/Makefile ${ENV_FILE} > "${REPO_ROOT}/Makefile"
info "written to ${REPO_ROOT}/Makefile"

echo "generating migrate.sh..."
jinja2 --strict ${INPUT_DIR}/migrate.sh ${ENV_FILE} > "${REPO_ROOT}/doa/migrate.sh"
info "written to ${REPO_ROOT}/doa/migrate.sh"

echo "generating translate.sh..."
jinja2 --strict ${INPUT_DIR}/translate.sh ${ENV_FILE} > "${REPO_ROOT}/doa/translate.sh"
info "written to ${REPO_ROOT}/doa/translate.sh"

echo "generating common.sh..."
jinja2 --strict ${INPUT_DIR}/common.sh ${ENV_FILE} > "${REPO_ROOT}/util/common.sh"
info "written to ${REPO_ROOT}/util/common.sh"

echo "generating __init__.py..."
jinja2 --strict ${INPUT_DIR}/__init__.py ${ENV_FILE} > "${REPO_ROOT}/doa/analyzers/__init__.py"
info "written to ${REPO_ROOT}/doa/analyzers/__init__.py"

echo
ok "[OK] all file generation completed."
