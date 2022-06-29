# common utilities.
# Do not execute this script directory.
# Intead, source this file from another script by `. common.sh`

# Assumes that ${WORK_DIR} is defined in the caller script.

which tput >/dev/null && tput_found=1

# yellow
debug() {
    if [[ -v tput_found ]]; then
        tput setaf 11; echo "$1"; tput sgr0
    else
        echo "$1"
    fi
}

# cyan
info() {
    if [[ -v tput_found ]]; then
        tput setaf 14; echo "$1"; tput sgr0
    else
        echo "$1"
    fi
}

# green
ok() {
    tput setaf 10 ; echo "$1" ; tput sgr0
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

DOA_VERSION={{version}}
IMAGE_NAME={{image_name}}
IMAGE_VER={{version}}
RUN_IMAGE=${IMAGE_NAME}:latest
DOCKERFILE=${REPO_ROOT}/.devcontainer/Dockerfile
DOCKER_CONTEXT=${REPO_ROOT}/doa

SAMPLE_REPO_URL=https://github.com/saud-aslam/trading-app

debug=1
# show_vars
