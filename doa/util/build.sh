#!/bin/bash
# build diva-doa docker image.

set -eu  # abort on error or undefined variable reference

# idiom to use the common.sh utilities.

WORK_DIR=$(readlink -f $(dirname $0)) # this script's directory
. ${WORK_DIR}/common.sh

# DOCKER_BUILD_OPT="--progress=plain"
DOCKER_BUILD_OPT=""

show_vars() {
    if [[ -v debug ]]; then
        echo
        debug "[DEBUG] variables:"
        debug "  REPO_ROOT        = ${REPO_ROOT}"
        debug "  WORK_DIR         = ${WORK_DIR}"
        debug "  CUR_DIR          = ${CUR_DIR}"
        debug "  IMAGE_NAME       = ${IMAGE_NAME}"
        debug "  IMAGE_VER        = ${IMAGE_VER}"
        debug "  RUN_IMAGE        = ${RUN_IMAGE}"
        debug "  DOCKERFILE       = ${DOCKERFILE}"
        debug "  DOCKER_CONTEXT   = ${DOCKER_CONTEXT}"
        debug "  DOCKER_BUILD_OPT = ${DOCKER_BUILD_OPT}"
    fi
}

show_vars

echo
info "building DiVA-DOA docker image: ${IMAGE_NAME}:${IMAGE_VER}..."

docker build ${DOCKER_BUILD_OPT} \
    -t ${IMAGE_NAME}:${IMAGE_VER} \
    --build-arg IMAGE_VER=${IMAGE_VER} \
    -f ${DOCKERFILE} \
    ${DOCKER_CONTEXT}
docker tag ${IMAGE_NAME}:${IMAGE_VER} ${IMAGE_NAME}:latest

echo
docker image ls ${IMAGE_NAME}

echo
info "build completed."
