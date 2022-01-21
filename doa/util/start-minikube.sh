#!/bin/bash
# (set up and) start new minikube cluster and install Postgres Operator using Helm

set -e

usage() {
    echo "Usage: ${APPNAME} [OPTION]..."
    echo
    echo "Options:"
    echo "  -d  enable debug mode"
    echo "  -h  show this help and exit"
    echo 
    echo "Environment variables:"
    echo "  NODES   number of nodes used for the created K8s cluster (1)."
    echo "  CPUS    number of CPU cores used for the created K8s cluster (8)."
    echo "  MEMORY  memory size (in MB) used for the created K8s cluster (16384)."
}

debug() {
    if [[ -v tput_found ]]; then
        tput setaf 3; echo "$1"; tput sgr0
    else
        echo "$1"
    fi
}

# $1: (relative) path of directory
# returned: absolute path
# status: not used
# Note: vanilla macOS does not have "-f" option to "readlink".
#       this only works on directory; cannot be used to files.
function abspath() {
    (cd $1 && pwd)
}

APPNAME=$(basename $0)
WORKDIR=$(abspath $(dirname $0)) # this script's directory
PWD=$(pwd)
which -s tput && tput_found=1

# process optional arguments
while getopts dbho: OPT
do
    case $OPT in
        o) outdir=${OPTARG};;
        b) build=1;;
        d) debug=1;;
        h) usage ; exit 1;;
        \?) exit 1;;
    esac
done

# process positional argument
shift $((OPTIND-1))

# if (($#==0)); then
#     usage
#     exit 1
# fi

if [[ -v debug ]]; then
    debug "[DEBUG] variables:"
    debug "  APPNAME    = ${APPNAME}"
    debug "  WORKDIR    = ${WORKDIR}"
    debug "  PWD        = ${PWD}"
    debug "  tput_found = ${tput_found}"
fi

echo
debug "stop and delete minikube cluster currently running..."
set +e
minikube stop
minikube delete
set -e

echo
debug "start new cluster..."
minikube start --cpus ${CPUS:-8} --memory ${MEMORY:-16384} --driver docker --nodes ${NODES:-"1"}

bash ${WORKDIR}/setup-operators.sh

echo
debug "[OK] setup successfully completed."
