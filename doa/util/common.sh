# common utilities.
# Do not execute this script directory.
# Intead, source this file from another script by `. common.sh`

# Assumes that ${WORK_DIR} is defined in the caller script.

which tput >/dev/null && tput_found=1

debug() {
    if [[ -v tput_found ]]; then
        tput setaf 11; echo "$1"; tput sgr0
    else
        echo "$1"
    fi
}

info() {
    if [[ -v tput_found ]]; then
        tput setaf 14; echo "$1"; tput sgr0
    else
        echo "$1"
    fi
}

show_vars() {
    if [[ -v debug ]]; then
        echo
        debug "[DEBUG] variables:"
        debug "  REPO_ROOT  = ${REPO_ROOT}"
        debug "  WORK_DIR   = ${WORK_DIR}"
        debug "  CUR_DIR    = ${CUR_DIR}"
        debug "  debug      = ${debug}"
        debug "  tput_found = ${tput_found}"
    fi
}

info "loading commnon utilities..."

CUR_DIR=$(pwd)
REPO_ROOT=$(readlink -f "${WORK_DIR}/..")

# constants 

IMAGE_NAME=diva-doa
IMAGE_VER=2.0.0
RUN_IMAGE=${IMAGE_NAME}:latest
DOCKERFILE=${REPO_ROOT}/.devcontainer/Dockerfile
DOCKER_CONTEXT=${REPO_ROOT}/doa

SAMPLE_REPO_URL=https://github.com/saud-aslam/trading-app

debug=1
# show_vars
