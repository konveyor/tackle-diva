#!/bin/bash
#
# build diva-doa docker image.
# usage:
#   bash [-f] util/build.sh
#
# if "-f" is specified, run "docker build" with "--no-cache".
#
set -eu  # abort on error or undefined variable reference

# idiom to use the common.sh utilities.

WORK_DIR=$(readlink -f $(dirname $0)) # this script's directory
. ${WORK_DIR}/common.sh

echo "-----------------------"
echo "DiVA-DOA image builder "
echo "-----------------------"

# If you want detailed build log, uncomment the following line.
# DOCKER_BUILD_OPT="--progress=plain"
DOCKER_BUILD_OPT=

# process optional arguments
while getopts f OPT
do
    case $OPT in
        f) force=1 ;;
        \?) exit 1 ;;
    esac
done

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

if [[ -n ${force+x} ]]; then
    DOCKER_BUILD_OPT+=" --no-cache"
fi

echo
info "building DiVA-DOA docker image: ${IMAGE_NAME}:${IMAGE_VER}..."

docker build ${DOCKER_BUILD_OPT} \
    -t ${IMAGE_NAME}:${IMAGE_VER} \
    --build-arg IMAGE_VER=${IMAGE_VER} \
    --target doa \
    -f ${DOCKERFILE} \
    ${DOCKER_CONTEXT}
docker tag ${IMAGE_NAME}:${IMAGE_VER} ${IMAGE_NAME}:latest

echo
docker image ls ${IMAGE_NAME}

echo
ok "build completed."
