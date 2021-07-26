#!/bin/bash

function usage() {
    echo $1
    cat <<_EOT_
Usage:
    `basename $0` <application github url>
    -h help
_EOT_
    exit 1
}

while getopts "c:h" OPT
do
    case $OPT in
        h) usage "[Help]";;
        \?) usage;;
    esac
done

if [ $# -ne 1 ]; then
    echo "[Error] Application github url is not specified."
    usage
fi

rm -rf ${TCD_APPLICATION_PATH}
git clone $1 ${TCD_APPLICATION_PATH}

${MTA_CLI_PATH}/bin/mta-cli --input ${TCD_APPLICATION_PATH} --sourceMode --target java-ee

${JANUSGRAPH_PATH}/bin/gremlin-server.sh start

until [ -f ${JANUSGRAPH_PATH}/log/gremlin-server.log ]
do
    sleep 1
done

tail -f ${JANUSGRAPH_PATH}/log/gremlin-server.log

