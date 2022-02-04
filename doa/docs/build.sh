#!/bin/bash
# script to build images from .dot files.

set -eu

# ensure the given command sequence exists.
function ensure_command() {
    "$@" &> /dev/null && return 0
    echo -e "command \"$1\" not found. abort."
    exit 1
}

# need graphviz 
if which dot >/dev/null; then
    :
else
    echo -e "dot not found. you need to install graphviz. abort."
    exit 1
fi

dot -Tpng -Gbgcolor="#00000000" -Gdpi=600 -O *dot
dot -Tsvg -O *dot
